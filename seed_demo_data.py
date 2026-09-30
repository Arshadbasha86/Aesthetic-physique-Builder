"""
seed_demo_data.py - Aesthetic Physique Developer Sandbox & Demo Seeder
Architectural Role: Injects 14 days of realistic training history, recovery habits
(water, sleep, protein), active workout streaks, and unlocked badges into the local
SQLite WAL database for instant evaluation, UI demoing, and live presentations.

Usage:
  python seed_demo_data.py
"""

import sys
import os
import uuid
from datetime import datetime, timedelta

# Add frontend_app to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "frontend_app"))

from frontend_app.database.db_manager import DatabaseManager


def seed_demo_database():
    print("\n" + "=" * 70)
    print("      AESTHETIC PHYSIQUE -- DEMO DATASET SEEDER")
    print("=" * 70 + "\n")

    db = DatabaseManager()

    with db.get_connection() as conn:
        # 1. Complete First-Time Onboarding
        print("  [1/6] Configuring Athlete Onboarding & Profile...")
        db.set_onboarding_completed()
        conn.execute(
            """
            INSERT INTO user_profile (
                user_id, username, full_name, email,
                current_weight_kg, height_cm, tier, equipped_title, updated_at
            )
            VALUES (
                'local_athlete_001', 'chloe_bennett', 'Chloe Bennett', 'chloe.b@gmail.com',
                62.5, 168.0, 'silver', 'Disciplined', datetime('now')
            )
            ON CONFLICT(user_id) DO UPDATE SET
                full_name = excluded.full_name,
                tier = excluded.tier,
                equipped_title = excluded.equipped_title,
                current_weight_kg = excluded.current_weight_kg,
                height_cm = excluded.height_cm,
                updated_at = datetime('now');
            """
        )

        # 2. Daily Streaks
        print("  [2/6] Setting 14-Day Consistent Workout Streak...")
        today_str = datetime.now().strftime("%Y-%m-%d")
        conn.execute(
            """
            INSERT INTO daily_streaks (
                user_id, current_streak_days, longest_streak_days,
                last_completed_date, updated_at
            )
            VALUES ('local_athlete_001', 14, 14, ?, datetime('now'))
            ON CONFLICT(user_id) DO UPDATE SET
                current_streak_days = 14,
                longest_streak_days = 14,
                last_completed_date = excluded.last_completed_date,
                updated_at = datetime('now');
            """,
            (today_str,)
        )

        # 3. 14 Days of Workout History
        print("  [3/6] Generating 14 Days of Completed Workout Sessions...")
        splits = ["DAY-A", "DAY-B", "DAY-C", "DAY-D", "DAY-E", "DAY-F", "DAY-G"]
        for i in range(14, 0, -1):
            past_date = datetime.now() - timedelta(days=i)
            date_str = past_date.strftime("%Y-%m-%d")
            split_day = splits[i % 7]
            session_id = f"SES-DEMO-{i:03d}"

            # Insert activity session
            conn.execute(
                """
                INSERT OR IGNORE INTO activity_sessions (
                    session_id, user_id, activity_type, session_title,
                    started_at, completed_at, duration_seconds,
                    sync_state, total_tonnage_kg
                )
                VALUES (?, 'local_athlete_001', 'resistance', ?, ?, ?, 2400, 'synced', 1850.0);
                """,
                (session_id, f"Evening Routine {split_day}", f"{date_str} 18:00:00", f"{date_str} 18:40:00")
            )

        # 4. Daily Recovery: Water Hydration
        print("  [4/6] Populating Water Hydration Ledger (3,200 - 3,600 ml/day)...")
        for i in range(14, -1, -1):
            date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            consumed_ml = 3200 + ((i * 70) % 400)
            conn.execute(
                """
                INSERT INTO water_logs (log_date, amount_ml)
                VALUES (?, ?);
                """,
                (date_str, consumed_ml)
            )

        # 5. Daily Recovery: Sleep & Protein
        print("  [5/6] Populating Sleep (7.8h) and Protein (140g) Ledgers...")
        for i in range(14, -1, -1):
            date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            conn.execute(
                """
                INSERT INTO sleep_logs (
                    log_date, in_time, out_time,
                    duration_minutes, quality_tier
                )
                VALUES (
                    ?, '22:30', '06:18', 468, 'Excellent Sleep'
                );
                """,
                (date_str,)
            )

            conn.execute(
                """
                INSERT INTO protein_logs (
                    log_date, timing_window, amount_gm
                )
                VALUES (
                    ?, 'daily_total', 142.0
                );
                """,
                (date_str,)
            )

        # 6. Unlocked Achievements & Vanity Badges
        print("  [6/6] Unlocking Canonical Badges ('Steel Grit', 'Hydration Master')...")
        conn.execute(
            """
            INSERT OR IGNORE INTO user_badges (id, user_id, badge_id, assigned_by, awarded_at)
            VALUES
                ('ub_demo_01', 'local_athlete_001', 'steel_grit_14', 'automated_rule', datetime('now', '-7 days')),
                ('ub_demo_02', 'local_athlete_001', 'hydration_master', 'automated_rule', datetime('now', '-3 days'));
            """
        )

        conn.commit()

    print("\n" + "=" * 70)
    print("  SEEDING COMPLETE! Athlete profile 'Chloe Bennett' is fully initialized.")
    print("  Streak: 14 Days | Tier: Silver | Title: 'Disciplined'")
    print("  Run 'python run_ecosystem.py --mobile' or '--web' to inspect live!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    seed_demo_database()
