"""
supabase_client.py - Aesthetic Physique Cross-Platform Supabase Client Wrapper
Architectural Role: Direct REST/RPC client communicating with Supabase PostgreSQL (PostgREST),
GoTrue Authentication, and Object Storage with token caching and offline resilience.
"""

import os
import json
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class SupabaseClient:
    """
    Unified Supabase API client for Mobile Client and Web Portals.
    Utilizes HTTPX for lightweight, dependency-safe REST calls directly to Supabase endpoints.
    """

    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_anon_key: Optional[str] = None,
        timeout: float = 10.0,
    ):
        self.url = (supabase_url or os.getenv("SUPABASE_URL", "https://your-project.supabase.co")).rstrip("/")
        self.anon_key = supabase_anon_key or os.getenv("SUPABASE_ANON_KEY", "sb_anon_mock_key_aesthetic_physique")
        self.timeout = timeout

        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.current_user: Optional[Dict[str, Any]] = None

    def _get_headers(self, authenticated: bool = True) -> Dict[str, str]:
        headers = {
            "apikey": self.anon_key,
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        if authenticated and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        else:
            headers["Authorization"] = f"Bearer {self.anon_key}"
        return headers

    # ----------------------------------------------------------------
    # Authentication & Session Management (GoTrue API)
    # ----------------------------------------------------------------

    def sign_in_with_password(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticates user via email and password."""
        endpoint = f"{self.url}/auth/v1/token?grant_type=password"
        payload = {"email": email, "password": password}

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(endpoint, json=payload, headers=self._get_headers(authenticated=False))
                if res.status_code == 200:
                    data = res.json()
                    self.access_token = data.get("access_token")
                    self.refresh_token = data.get("refresh_token")
                    self.current_user = data.get("user")
                    return {"success": True, "user": self.current_user, "access_token": self.access_token}
                else:
                    return {"success": False, "error": res.text, "status_code": res.status_code}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    def sign_up(self, email: str, password: str, display_name: str) -> Dict[str, Any]:
        """Registers a new athlete account."""
        endpoint = f"{self.url}/auth/v1/signup"
        payload = {
            "email": email,
            "password": password,
            "data": {"display_name": display_name, "role": "ATHLETE"},
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(endpoint, json=payload, headers=self._get_headers(authenticated=False))
                if res.status_code in (200, 201):
                    data = res.json()
                    self.access_token = data.get("access_token")
                    self.refresh_token = data.get("refresh_token")
                    self.current_user = data.get("user")
                    return {"success": True, "user": self.current_user}
                else:
                    return {"success": False, "error": res.text, "status_code": res.status_code}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    def sign_out(self) -> None:
        """Clears local authentication state."""
        self.access_token = None
        self.refresh_token = None
        self.current_user = None

    # ----------------------------------------------------------------
    # Athlete Profiles (PostgREST API)
    # ----------------------------------------------------------------

    def fetch_athlete_profile(self, athlete_id: str) -> Dict[str, Any]:
        """Fetches the athlete's cloud profile."""
        endpoint = f"{self.url}/rest/v1/athletes?id=eq.{athlete_id}&select=*"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.get(endpoint, headers=self._get_headers())
                if res.status_code == 200:
                    records = res.json()
                    return {"success": True, "data": records[0] if records else None}
                return {"success": False, "error": res.text}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    def update_athlete_biometrics(self, athlete_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Updates athlete weight, height, or active title."""
        endpoint = f"{self.url}/rest/v1/athletes?id=eq.{athlete_id}"
        headers = self._get_headers()
        headers["Prefer"] = "return=representation"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.patch(endpoint, json=updates, headers=headers)
                if res.status_code in (200, 204):
                    return {"success": True, "data": res.json() if res.text else updates}
                return {"success": False, "error": res.text}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    # ----------------------------------------------------------------
    # Workout Sessions & Sets Synchronization
    # ----------------------------------------------------------------

    def sync_workout_session(
        self,
        session_data: Dict[str, Any],
        sets_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Upserts a completed workout session and its constituent sets to the cloud.
        """
        session_endpoint = f"{self.url}/rest/v1/workout_sessions"
        sets_endpoint = f"{self.url}/rest/v1/workout_sets"
        headers = self._get_headers()
        headers["Prefer"] = "resolution=merge-duplicates,return=representation"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                # 1. Upsert session parent record
                s_res = client.post(session_endpoint, json=session_data, headers=headers)
                if s_res.status_code not in (200, 201):
                    return {"success": False, "error": f"Session sync failed: {s_res.text}"}

                # 2. Upsert constituent sets
                if sets_data:
                    sets_res = client.post(sets_endpoint, json=sets_data, headers=headers)
                    if sets_res.status_code not in (200, 201):
                        return {"success": False, "error": f"Sets sync failed: {sets_res.text}"}

                return {"success": True, "session_id": session_data.get("session_id")}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    # ----------------------------------------------------------------
    # Daily Recovery Ledger Sync
    # ----------------------------------------------------------------

    def sync_recovery_water(
        self,
        athlete_id: str,
        log_date: str,
        consumed_ml: int,
        target_ml: int = 3500,
    ) -> Dict[str, Any]:
        """Upserts daily water intake log."""
        endpoint = f"{self.url}/rest/v1/recovery_water"
        payload = {
            "athlete_id": athlete_id,
            "log_date": log_date,
            "total_consumed_ml": consumed_ml,
            "target_ml": target_ml,
            "target_reached": consumed_ml >= target_ml,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        headers = self._get_headers()
        headers["Prefer"] = "resolution=merge-duplicates,return=representation"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(endpoint, json=payload, headers=headers)
                return {"success": res.status_code in (200, 201), "error": res.text if res.status_code not in (200, 201) else None}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    def sync_recovery_sleep(
        self,
        athlete_id: str,
        log_date: str,
        in_time: str,
        out_time: str,
        duration_hours: float,
        quality_tier: str,
    ) -> Dict[str, Any]:
        """Upserts daily sleep log."""
        endpoint = f"{self.url}/rest/v1/recovery_sleep"
        payload = {
            "athlete_id": athlete_id,
            "log_date": log_date,
            "in_time": in_time,
            "out_time": out_time,
            "duration_hours": duration_hours,
            "quality_tier": quality_tier,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        headers = self._get_headers()
        headers["Prefer"] = "resolution=merge-duplicates,return=representation"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(endpoint, json=payload, headers=headers)
                return {"success": res.status_code in (200, 201), "error": res.text if res.status_code not in (200, 201) else None}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    def sync_recovery_protein(
        self,
        athlete_id: str,
        log_date: str,
        total_g: int,
        target_g: int = 150,
        pre_workout: bool = False,
        post_workout: bool = False,
    ) -> Dict[str, Any]:
        """Upserts daily protein intake log."""
        endpoint = f"{self.url}/rest/v1/recovery_protein"
        payload = {
            "athlete_id": athlete_id,
            "log_date": log_date,
            "total_consumed_g": total_g,
            "target_g": target_g,
            "pre_workout_taken": pre_workout,
            "post_workout_taken": post_workout,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        headers = self._get_headers()
        headers["Prefer"] = "resolution=merge-duplicates,return=representation"

        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.post(endpoint, json=payload, headers=headers)
                return {"success": res.status_code in (200, 201), "error": res.text if res.status_code not in (200, 201) else None}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    # ----------------------------------------------------------------
    # Badges Catalog & Unlocks
    # ----------------------------------------------------------------

    def fetch_badges_catalog(self) -> Dict[str, Any]:
        """Retrieves master list of active badges."""
        endpoint = f"{self.url}/rest/v1/badges?is_active=eq.true&select=*"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.get(endpoint, headers=self._get_headers(authenticated=False))
                if res.status_code == 200:
                    return {"success": True, "badges": res.json()}
                return {"success": False, "error": res.text}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    def fetch_athlete_badges(self, athlete_id: str) -> Dict[str, Any]:
        """Retrieves badges unlocked by a specific athlete."""
        endpoint = f"{self.url}/rest/v1/athlete_badges?athlete_id=eq.{athlete_id}&select=*,badges(*)"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.get(endpoint, headers=self._get_headers())
                if res.status_code == 200:
                    return {"success": True, "unlocked": res.json()}
                return {"success": False, "error": res.text}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}

    # ----------------------------------------------------------------
    # App Version & Documentation Registry
    # ----------------------------------------------------------------

    def fetch_app_version_config(self) -> Dict[str, Any]:
        """Fetches global version gating, force update flag, and CDN links."""
        endpoint = f"{self.url}/rest/v1/app_version_configs?config_key=eq.GLOBAL_CONFIG&select=*"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                res = client.get(endpoint, headers=self._get_headers(authenticated=False))
                if res.status_code == 200:
                    records = res.json()
                    return {"success": True, "config": records[0] if records else None}
                return {"success": False, "error": res.text}
        except Exception as e:
            return {"success": False, "error": str(e), "is_offline": True}
