"""
Aesthetic Physique Builder - Local Database Manager
Relative Path: frontend_app/database/db_manager.py
Architectural Role: Thread-safe SQLite CRUD manager and transaction coordinator
operating in WAL mode. Manages offline state persistence, session caching,
habit ledgers, gamification records, and the sync outbox queue.
"""

import sqlite3
import json
import uuid
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from config.default_config import DB_FILE_PATH, DATABASE_DIR


class DatabaseManager:
    """Singleton Database Manager for offline SQLite access."""
    _instance: Optional["DatabaseManager"] = None

    def __new__(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.db_path = DB_FILE_PATH
        self.schema_path = DATABASE_DIR / "local_schema.sql"
        self._ensure_database_ready()
        self._initialized = True

    def get_connection(self) -> sqlite3.Connection:
        """Returns a configured SQLite connection with row factories and WAL mode."""
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _ensure_database_ready(self):
        """Initializes database schema from local_schema.sql if tables do not exist."""
        DATABASE_DIR.mkdir(parents=True, exist_ok=True)
        with self.get_connection() as conn:
            with open(self.schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            conn.executescript(schema_sql)
            conn.commit()

    # ==========================================================================
    # 1. Onboarding & App Lifecycle Configurations
    # ==========================================================================
    def get_config(self, key: str, default: Optional[str] = None) -> Optional[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT config_value FROM app_config WHERE config_key = ?", (key,))
            row = cursor.fetchone()
            return row["config_value"] if row else default

    def set_config(self, key: str, value: str):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO app_config (config_key, config_value, updated_at) VALUES (?, ?, datetime('now')) "
                "ON CONFLICT(config_key) DO UPDATE SET config_value = excluded.config_value, updated_at = datetime('now');",
                (key, str(value))
            )
            conn.commit()

    def is_onboarding_completed(self) -> bool:
        return self.get_config("is_onboarding_completed", "false").lower() == "true"

    def set_onboarding_completed(self):
        self.set_config("is_onboarding_completed", "true")
        self.set_config("first_time_user", "false")
        self.set_config("has_seen_disclaimer", "true")
        self.set_config("has_seen_warning", "true")

    def get_week_schedule(self) -> Dict[str, str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT day_of_week, routine_day_id FROM week_schedule")
            return {row["day_of_week"]: row["routine_day_id"] for row in cursor.fetchall()}

    def update_week_schedule(self, schedule_mapping: Dict[str, str]):
        with self.get_connection() as conn:
            for day, routine_id in schedule_mapping.items():
                conn.execute(
                    "INSERT INTO week_schedule (day_of_week, routine_day_id, updated_at) VALUES (?, ?, datetime('now')) "
                    "ON CONFLICT(day_of_week) DO UPDATE SET routine_day_id = excluded.routine_day_id, updated_at = datetime('now');",
                    (day, routine_id)
                )
            conn.commit()

    # ==========================================================================
    # 2. User Profile & Biometrics
    # ==========================================================================
    def get_user_profile(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_profile LIMIT 1")
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {}

    def update_user_biometrics(
        self,
        current_weight_kg: float,
        target_weight_kg: float,
        height_cm: float,
        age_years: int,
        biological_sex: str,
        activity_tier: str = "moderate"
    ):
        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE user_profile 
                SET current_weight_kg = ?, target_weight_kg = ?, height_cm = ?,
                    age_years = ?, biological_sex = ?, activity_tier = ?, 
                    is_synced = 0, updated_at = datetime('now')
                WHERE user_id = (SELECT user_id FROM user_profile LIMIT 1);
                """,
                (current_weight_kg, target_weight_kg, height_cm, age_years, biological_sex, activity_tier)
            )
            conn.commit()
        # Enqueue change in sync outbox
        self.enqueue_outbox("UPDATE", "user_profile", "local_athlete_001", {
            "current_weight_kg": current_weight_kg,
            "target_weight_kg": target_weight_kg,
            "height_cm": height_cm,
            "age_years": age_years,
            "biological_sex": biological_sex
        })

    def equip_title(self, title_name: str):
        with self.get_connection() as conn:
            conn.execute("UPDATE user_profile SET equipped_title = ?, updated_at = datetime('now');", (title_name,))
            conn.commit()

    # ==========================================================================
    # 3. User Settings & Hardware Config
    # ==========================================================================
    def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT setting_value FROM user_settings WHERE setting_key = ?", (key,))
            row = cursor.fetchone()
            return row["setting_value"] if row else default

    def set_setting(self, key: str, value: str):
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO user_settings (setting_key, setting_value, updated_at) VALUES (?, ?, datetime('now')) "
                "ON CONFLICT(setting_key) DO UPDATE SET setting_value = excluded.setting_value, updated_at = datetime('now');",
                (key, str(value))
            )
            conn.commit()

    def get_all_settings(self) -> Dict[str, str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT setting_key, setting_value FROM user_settings")
            return {row["setting_key"]: row["setting_value"] for row in cursor.fetchall()}

    # ==========================================================================
    # 4. In-Workout Session Cache (State Interruption Recovery)
    # ==========================================================================
    def get_active_session(self) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM active_session_state WHERE id = 1")
            row = cursor.fetchone()
            return dict(row) if row else None

    def save_active_session(
        self,
        day_id: str,
        session_type: str,
        current_exercise_index: int,
        current_set_index: int,
        active_side: str,
        current_sub_phase: str,
        completion_percentage: int,
        target_end_timestamp: float = 0,
        is_paused: int = 0,
        is_screen_locked: int = 0
    ):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO active_session_state (
                    id, day_id, session_type, current_exercise_index, current_set_index,
                    active_side, current_sub_phase, completion_percentage, target_end_timestamp,
                    is_paused, is_screen_locked, updated_at
                ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                ON CONFLICT(id) DO UPDATE SET 
                    day_id = excluded.day_id,
                    session_type = excluded.session_type,
                    current_exercise_index = excluded.current_exercise_index,
                    current_set_index = excluded.current_set_index,
                    active_side = excluded.active_side,
                    current_sub_phase = excluded.current_sub_phase,
                    completion_percentage = excluded.completion_percentage,
                    target_end_timestamp = excluded.target_end_timestamp,
                    is_paused = excluded.is_paused,
                    is_screen_locked = excluded.is_screen_locked,
                    updated_at = datetime('now');
                """,
                (day_id, session_type, current_exercise_index, current_set_index,
                 active_side, current_sub_phase, completion_percentage, target_end_timestamp,
                 is_paused, is_screen_locked)
            )
            conn.commit()

    def clear_active_session(self):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM active_session_state WHERE id = 1")
            conn.commit()

    # ==========================================================================
    # 5. Activity Logging (Sessions & Sets)
    # ==========================================================================
    def create_activity_session(
        self,
        activity_type: str,
        session_title: str,
        duration_seconds: int,
        total_tonnage_kg: float = 0.0,
        total_poses_completed: int = 0,
        average_intensity_rpe: Optional[float] = None
    ) -> str:
        session_id = str(uuid.uuid4())
        started_at = (datetime.datetime.now() - datetime.timedelta(seconds=duration_seconds)).isoformat()
        completed_at = datetime.datetime.now().isoformat()
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO activity_sessions (
                    session_id, user_id, activity_type, session_title, started_at,
                    completed_at, duration_seconds, total_tonnage_kg, total_poses_completed,
                    average_intensity_rpe, sync_state
                ) VALUES (?, 'local_athlete_001', ?, ?, ?, ?, ?, ?, ?, ?, 'pending_insert');
                """,
                (session_id, activity_type, session_title, started_at, completed_at,
                 duration_seconds, total_tonnage_kg, total_poses_completed, average_intensity_rpe)
            )
            conn.commit()

        self.enqueue_outbox("INSERT", "activity_sessions", session_id, {
            "session_id": session_id,
            "activity_type": activity_type,
            "session_title": session_title,
            "duration_seconds": duration_seconds,
            "total_tonnage_kg": total_tonnage_kg,
            "completed_at": completed_at
        })
        return session_id

    def add_activity_entry(
        self,
        session_id: str,
        movement_name: str,
        sequence_order: int,
        entry_type: str,
        weight_kg: Optional[float] = None,
        reps_completed: Optional[int] = None,
        hold_duration_sec: Optional[int] = None,
        is_unilateral: bool = False,
        limb_designation: str = "bilateral",
        rpe_rating: Optional[float] = None
    ):
        entry_id = str(uuid.uuid4())
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO activity_entries (
                    entry_id, session_id, movement_name, sequence_order, entry_type,
                    weight_kg, reps_completed, hold_duration_sec, is_unilateral,
                    limb_designation, rpe_rating
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (entry_id, session_id, movement_name, sequence_order, entry_type,
                 weight_kg, reps_completed, hold_duration_sec, 1 if is_unilateral else 0,
                 limb_designation, rpe_rating)
            )
            conn.commit()

    def get_recent_sessions(self, limit: int = 15) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM activity_sessions ORDER BY started_at DESC LIMIT ?", (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    # ==========================================================================
    # 6. Biological Habit Ledgers (Water, Sleep, Protein)
    # ==========================================================================
    def log_water_intake(self, amount_ml: int) -> int:
        today_str = datetime.date.today().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO water_logs (log_date, amount_ml) VALUES (?, ?);",
                (today_str, amount_ml)
            )
            conn.commit()
            log_id = cursor.lastrowid
        self.enqueue_outbox("INSERT", "water_logs", str(log_id), {"log_date": today_str, "amount_ml": amount_ml})
        return log_id

    def get_today_water_intake(self) -> int:
        today_str = datetime.date.today().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT SUM(amount_ml) as total FROM water_logs WHERE log_date = ?", (today_str,)
            )
            row = cursor.fetchone()
            return row["total"] or 0 if row else 0

    def log_sleep(self, in_time: str, out_time: str, duration_minutes: int, quality_tier: str) -> int:
        today_str = datetime.date.today().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO sleep_logs (log_date, in_time, out_time, duration_minutes, quality_tier)
                VALUES (?, ?, ?, ?, ?);
                """,
                (today_str, in_time, out_time, duration_minutes, quality_tier)
            )
            conn.commit()
            log_id = cursor.lastrowid
        self.enqueue_outbox("INSERT", "sleep_logs", str(log_id), {
            "log_date": today_str, "in_time": in_time, "out_time": out_time,
            "duration_minutes": duration_minutes, "quality_tier": quality_tier
        })
        return log_id

    def get_sleep_logs(self, limit: int = 7) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM sleep_logs ORDER BY log_date DESC, log_id DESC LIMIT ?", (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def log_protein(self, amount_gm: float, timing_window: str = "daily_total") -> int:
        today_str = datetime.date.today().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO protein_logs (log_date, timing_window, amount_gm) VALUES (?, ?, ?);",
                (today_str, timing_window, amount_gm)
            )
            conn.commit()
            log_id = cursor.lastrowid
        self.enqueue_outbox("INSERT", "protein_logs", str(log_id), {
            "log_date": today_str, "timing_window": timing_window, "amount_gm": amount_gm
        })
        return log_id

    def get_today_protein_intake(self) -> float:
        today_str = datetime.date.today().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT SUM(amount_gm) as total FROM protein_logs WHERE log_date = ?", (today_str,)
            )
            row = cursor.fetchone()
            return row["total"] or 0.0 if row else 0.0

    # ==========================================================================
    # 7. Gamification & Streaks
    # ==========================================================================
    def get_streak(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM daily_streaks WHERE user_id = 'local_athlete_001'")
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {"current_streak_days": 1, "longest_streak_days": 1}

    def record_day_completed(self):
        """Advances streak if completed on a new day."""
        today_str = datetime.date.today().isoformat()
        current = self.get_streak()
        last_date = current.get("last_completed_date")
        if last_date == today_str:
            return  # Already credited today

        streak = current.get("current_streak_days", 0) + 1
        longest = max(streak, current.get("longest_streak_days", 0))

        with self.get_connection() as conn:
            conn.execute(
                """
                UPDATE daily_streaks 
                SET current_streak_days = ?, longest_streak_days = ?, 
                    last_completed_date = ?, updated_at = datetime('now')
                WHERE user_id = 'local_athlete_001';
                """,
                (streak, longest, today_str)
            )
            conn.commit()

    def get_all_badges_with_status(self) -> List[Dict[str, Any]]:
        """Joins badge definitions with user earned status."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 
                    b.badge_id, b.badge_name, b.tier, b.associated_title,
                    b.artwork_url, b.assignment_criteria,
                    u.awarded_at,
                    CASE WHEN u.badge_id IS NOT NULL THEN 1 ELSE 0 END as is_unlocked
                FROM badge_definitions b
                LEFT JOIN user_badges u ON b.badge_id = u.badge_id AND u.user_id = 'local_athlete_001'
                ORDER BY b.rowid;
                """
            )
            return [dict(row) for row in cursor.fetchall()]

    # ==========================================================================
    # 8. Customer Support Desk Ledger
    # ==========================================================================
    def create_support_ticket(self, subject: str, category: str, message: str) -> str:
        ticket_id = str(uuid.uuid4())[:8]
        msg_id = str(uuid.uuid4())
        with self.get_connection() as conn:
            conn.execute(
                "INSERT INTO support_tickets (ticket_id, user_id, subject, category, status) VALUES (?, 'local_athlete_001', ?, ?, 'open');",
                (ticket_id, subject, category)
            )
            conn.execute(
                "INSERT INTO support_messages (message_id, ticket_id, sender_type, body) VALUES (?, ?, 'user', ?);",
                (msg_id, ticket_id, message)
            )
            conn.commit()
        self.enqueue_outbox("INSERT", "support_tickets", ticket_id, {
            "ticket_id": ticket_id, "subject": subject, "category": category, "initial_message": message
        })
        return ticket_id

    def get_support_tickets(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM support_tickets ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_support_messages(self, ticket_id: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM support_messages WHERE ticket_id = ? ORDER BY created_at ASC", (ticket_id,))
            return [dict(row) for row in cursor.fetchall()]

    # ==========================================================================
    # 9. Offline Mutation Journal (Sync Outbox)
    # ==========================================================================
    def enqueue_outbox(self, mutation_type: str, entity_table: str, entity_id: str, payload: Dict[str, Any]):
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO sync_outbox (mutation_type, entity_table, entity_id, payload_json, status)
                VALUES (?, ?, ?, ?, 'pending');
                """,
                (mutation_type, entity_table, entity_id, json.dumps(payload))
            )
            conn.commit()

    def get_pending_outbox_items(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sync_outbox WHERE status = 'pending' ORDER BY outbox_id ASC LIMIT ?", (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def mark_outbox_item_synced(self, outbox_id: int):
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE sync_outbox SET status = 'synced', synced_at = datetime('now') WHERE outbox_id = ?;",
                (outbox_id,)
            )
            conn.commit()

    # ==========================================================================
    # 10. Complete Local Account Wipe / Purge
    # ==========================================================================
    def purge_all_local_data(self):
        """Teardown of all trainee biometric, workout, and habit data for Account Deletion."""
        with self.get_connection() as conn:
            conn.execute("DELETE FROM activity_entries;")
            conn.execute("DELETE FROM activity_sessions;")
            conn.execute("DELETE FROM active_session_state;")
            conn.execute("DELETE FROM water_logs;")
            conn.execute("DELETE FROM sleep_logs;")
            conn.execute("DELETE FROM protein_logs;")
            conn.execute("DELETE FROM support_messages;")
            conn.execute("DELETE FROM support_tickets;")
            conn.execute("DELETE FROM sync_outbox;")
            conn.execute("DELETE FROM user_badges;")
            conn.execute("UPDATE daily_streaks SET current_streak_days = 0, longest_streak_days = 0;")
            conn.execute("UPDATE user_profile SET equipped_title = 'Novice Trainee';")
            conn.execute("UPDATE app_config SET config_value = 'false' WHERE config_key = 'is_onboarding_completed';")
            conn.commit()


# Convenient global singleton instance
db = DatabaseManager()
