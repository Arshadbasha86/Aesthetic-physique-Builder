"""
cloud_sync_bridge.py - Aesthetic Physique Offline-First Cloud Sync Bridge
Architectural Role: Bridges the local SQLite WAL mutation queue (sync_outbox)
with the remote Supabase cloud database, coordinating FIFO push dispatches and inbound
remote sync for badges, ticket responses, and app version checks.
"""

import json
import logging
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from frontend_app.database.db_manager import DatabaseManager
from backend_cloud.client.supabase_client import SupabaseClient

logger = logging.getLogger("CloudSyncBridge")


class CloudSyncBridge:
    """
    Coordinates bi-directional synchronization between the offline-first SQLite WAL database
    and the remote Supabase cloud backend.
    """

    def __init__(
        self,
        db_manager: DatabaseManager,
        supabase_client: Optional[SupabaseClient] = None,
    ):
        self.db = db_manager
        self.supabase = supabase_client or SupabaseClient()
        self._lock = threading.Lock()
        self._is_syncing = False

    def is_cloud_reachable(self) -> bool:
        """Quick healthcheck to verify if Supabase API is reachable."""
        res = self.supabase.fetch_app_version_config()
        return not res.get("is_offline", False) and res.get("success", False)

    # ----------------------------------------------------------------
    # 1. Outbound Sync: FIFO Mutation Dispatcher (Push to Cloud)
    # ----------------------------------------------------------------

    def flush_mutation_outbox(self) -> Dict[str, Any]:
        """
        Processes pending mutations in strict FIFO sequence and pushes them to Supabase.
        """
        with self._lock:
            if self._is_syncing:
                return {"status": "ALREADY_SYNCING", "processed": 0, "failed": 0}
            self._is_syncing = True

        processed_count = 0
        failed_count = 0

        try:
            pending_items = self.db.get_pending_outbox_items(limit=50)
            if not pending_items:
                return {"status": "IDLE", "processed": 0, "failed": 0}

            for item in pending_items:
                outbox_id = item["outbox_id"]
                table_name = item["entity_table"]
                entity_id = item["entity_id"]
                payload_str = item.get("payload_json", "{}")

                try:
                    payload = json.loads(payload_str) if payload_str else {}
                except Exception:
                    payload = {}

                # Dispatch mutation to corresponding Supabase method
                dispatch_success = self._dispatch_single_mutation(table_name, entity_id, payload)

                if dispatch_success:
                    self.db.mark_outbox_item_synced(outbox_id)
                    processed_count += 1
                else:
                    failed_count += 1
                    # Break sequence on network disconnection to preserve strict FIFO ordering
                    break

            return {
                "status": "COMPLETED",
                "processed": processed_count,
                "failed": failed_count,
            }
        finally:
            with self._lock:
                self._is_syncing = False

    def _dispatch_single_mutation(
        self,
        entity_table: str,
        entity_id: str,
        payload: Dict[str, Any],
    ) -> bool:
        """Dispatches an individual mutation record to Supabase."""
        try:
            if entity_table in ("activity_sessions", "workout_sessions"):
                session_data = payload.get("session", {})
                sets_data = payload.get("sets", [])
                res = self.supabase.sync_workout_session(session_data, sets_data)
                return res.get("success", False)

            elif entity_table in ("water_logs", "recovery_water"):
                ath_id = payload.get("athlete_id", "local_athlete_001")
                log_date = payload.get("log_date", datetime.now().strftime("%Y-%m-%d"))
                consumed = payload.get("total_consumed_ml", 0)
                target = payload.get("target_ml", 3500)
                res = self.supabase.sync_recovery_water(ath_id, log_date, consumed, target)
                return res.get("success", False)

            elif entity_table in ("sleep_logs", "recovery_sleep"):
                ath_id = payload.get("athlete_id", "local_athlete_001")
                log_date = payload.get("log_date", datetime.now().strftime("%Y-%m-%d"))
                res = self.supabase.sync_recovery_sleep(
                    ath_id,
                    log_date,
                    payload.get("in_time", ""),
                    payload.get("out_time", ""),
                    payload.get("duration_hours", 0.0),
                    payload.get("quality_tier", "Good"),
                )
                return res.get("success", False)

            elif entity_table in ("protein_logs", "recovery_protein"):
                ath_id = payload.get("athlete_id", "local_athlete_001")
                log_date = payload.get("log_date", datetime.now().strftime("%Y-%m-%d"))
                res = self.supabase.sync_recovery_protein(
                    ath_id,
                    log_date,
                    payload.get("total_consumed_g", 0),
                    payload.get("target_g", 150),
                    payload.get("pre_workout_taken", False),
                    payload.get("post_workout_taken", False),
                )
                return res.get("success", False)

            elif entity_table in ("user_profile", "athletes"):
                ath_id = entity_id
                res = self.supabase.update_athlete_biometrics(ath_id, payload)
                return res.get("success", False)

            else:
                logger.warning(f"Unhandled mutation entity table: {entity_table}")
                return True  # Avoid deadlocks on unhandled telemetry
        except Exception as e:
            logger.error(f"Error dispatching mutation {entity_table}:{entity_id} - {e}")
            return False

    # ----------------------------------------------------------------
    # 2. Inbound Sync: Remote Updates Puller (Pull from Cloud)
    # ----------------------------------------------------------------

    def pull_remote_state(self, athlete_id: str = "local_athlete_001") -> Dict[str, Any]:
        """
        Pulls remote state from Supabase to sync back to local SQLite:
        - Admin-granted badges / titles
        - App version configuration & force update status
        """
        results = {"badges_synced": 0, "version_checked": False, "force_update": False}

        # 1. Pull Badges
        b_res = self.supabase.fetch_athlete_badges(athlete_id)
        if b_res.get("success") and b_res.get("unlocked"):
            with self.db.get_connection() as conn:
                for item in b_res["unlocked"]:
                    badge_id = item.get("badge_id")
                    awarded_at = item.get("unlocked_at", datetime.now(timezone.utc).isoformat())

                    # Check if local user_badges has this award
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT badge_id FROM user_badges WHERE user_id = ? AND badge_id = ?",
                        (athlete_id, badge_id),
                    )
                    if not cursor.fetchone():
                        conn.execute(
                            "INSERT INTO user_badges (user_id, badge_id, awarded_at) VALUES (?, ?, ?)",
                            (athlete_id, badge_id, awarded_at),
                        )
                        results["badges_synced"] += 1
                conn.commit()

        # 2. Check Version Config
        v_res = self.supabase.fetch_app_version_config()
        if v_res.get("success") and v_res.get("config"):
            results["version_checked"] = True
            results["force_update"] = v_res["config"].get("force_update_flag", False)
            results["latest_version"] = v_res["config"].get("latest_mobile_version")
            results["min_version"] = v_res["config"].get("min_required_mobile_version")

        return results

    # ----------------------------------------------------------------
    # 3. Unified Full Sync Trigger
    # ----------------------------------------------------------------

    def trigger_full_sync(self, athlete_id: str = "local_athlete_001") -> Dict[str, Any]:
        """
        Executes a complete sync cycle: flushes outbound mutations, then pulls inbound updates.
        """
        outbound_report = self.flush_mutation_outbox()
        inbound_report = self.pull_remote_state(athlete_id)

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "outbound": outbound_report,
            "inbound": inbound_report,
        }
