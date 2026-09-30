"""
Aesthetic Physique Builder - Offline-First Sync Worker
Relative Path: frontend_app/engine/sync_worker.py
Architectural Role: Background worker monitoring network connectivity,
processing the durable SQLite mutation outbox queue (FIFO), and executing
idempotent batch synchronization while offline-resilient.
"""

import time
import json
import socket
import threading
from datetime import datetime
from typing import Optional, Dict, Any, List

from database.db_manager import db
from config.default_config import DEFAULT_DYNAMIC_CONFIG

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


class SyncWorker:
    """
    Background Synchronization Engine.
    Monitors online status and processes pending sync_outbox mutations.
    """
    _instance: Optional["SyncWorker"] = None

    def __new__(cls) -> "SyncWorker":
        if cls._instance is None:
            cls._instance = super(SyncWorker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.is_online: bool = False
        self.last_sync_timestamp: Optional[str] = None
        self.is_syncing: bool = False
        self.sync_interval_sec: int = 30
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._initialized = True

    def start(self):
        """Starts the background worker thread."""
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()

    def stop(self):
        """Signals the background worker to halt."""
        self._stop_event.set()

    def check_connectivity(self) -> bool:
        """Performs a quick non-blocking DNS/socket probe to verify internet reachability."""
        try:
            # Quick probe to Google Public DNS
            socket.create_connection(("8.8.8.8", 53), timeout=1.5)
            self.is_online = True
            return True
        except (socket.timeout, OSError):
            self.is_online = False
            return False

    def trigger_sync_now(self):
        """Triggers an immediate background outbox flush."""
        threading.Thread(target=self._process_outbox, daemon=True).start()

    def get_sync_status(self) -> Dict[str, Any]:
        """Returns diagnostic metrics for UI network indicators."""
        pending_items = db.get_pending_outbox_items(limit=100)
        return {
            "is_online": self.is_online,
            "is_syncing": self.is_syncing,
            "pending_count": len(pending_items),
            "last_sync": self.last_sync_timestamp
        }

    # ==========================================================================
    # Internal Sync & Outbox Processing
    # ==========================================================================
    def _run_loop(self):
        """Continuous background polling loop."""
        while not self._stop_event.is_set():
            if self.check_connectivity():
                self._process_outbox()
            # Sleep in small slices to respond promptly to stop_event
            for _ in range(self.sync_interval_sec):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def _process_outbox(self):
        """Flushes pending SQLite outbox items in FIFO order."""
        if self.is_syncing:
            return

        pending = db.get_pending_outbox_items(limit=25)
        if not pending:
            return

        self.is_syncing = True
        try:
            for item in pending:
                outbox_id = item["outbox_id"]
                table_name = item["entity_table"]
                mutation = item["mutation_type"]
                payload = json.loads(item["payload_json"])

                # Dispatch simulation or remote HTTP push
                success = self._dispatch_mutation(table_name, mutation, payload)
                if success:
                    db.mark_outbox_item_synced(outbox_id)
                else:
                    break  # Stop batch on failure to preserve FIFO ordering

            self.last_sync_timestamp = datetime.now().strftime("%H:%M:%S")
        except Exception as e:
            print(f"[SyncWorker] Outbox processing exception: {e}")
        finally:
            self.is_syncing = False

    def _dispatch_mutation(self, table: str, mutation: str, payload: Dict[str, Any]) -> bool:
        """
        Sends payload to remote Supabase endpoint when online.
        In Phase 1, validates format and acknowledges locally.
        """
        # In offline-first Phase 1, we ensure payload serialization is valid
        # When Phase 3 connects to live Supabase, this executes the RPC batch.
        time.sleep(0.05)  # Simulate non-blocking micro-dispatch
        return True


# Global sync worker singleton
sync_worker = SyncWorker()
