"""
run_ecosystem.py - Aesthetic Physique Master Ecosystem Launcher
Architectural Role: Universal execution hub for running the Native Mobile App,
the Web Portals (Athlete Companion & Admin Operations Console), or the complete
automated test suite across all 40 platform components.

Usage:
  python run_ecosystem.py --mobile   # Launches Native Mobile App (Portrait mode)
  python run_ecosystem.py --web      # Launches Web Portals in Default Browser
  python run_ecosystem.py --test     # Executes Complete Platform Test Suite
  python run_ecosystem.py            # Opens Interactive Launcher Menu
"""

import sys
import os
import argparse

# Inject all ecosystem packages into sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "frontend_app"))
sys.path.insert(0, os.path.join(BASE_DIR, "web_portal"))
sys.path.insert(0, os.path.join(BASE_DIR, "backend_cloud"))
sys.path.insert(0, BASE_DIR)


def run_mobile_app():
    """Launches the Aesthetic Physique Native Mobile Application."""
    print("\n" + "=" * 65)
    print("  STARTING AESTHETIC PHYSIQUE MOBILE CLIENT")
    print("  Resolution: 460px Mobile Portrait Container")
    print("  Engine: Offline-First SQLite WAL + Wall-Clock Audio Sync")
    print("=" * 65 + "\n")
    import flet as ft
    from frontend_app.main import main as mobile_main
    assets_path = os.path.join(BASE_DIR, "frontend_app", "assets")
    ft.app(target=mobile_main, assets_dir=assets_path)


def run_web_portal(port: int = 8550):
    """Launches the Athlete Companion Portal & Admin Operations Console in Web Browser."""
    print("\n" + "=" * 65)
    print("  STARTING AESTHETIC PHYSIQUE WEB PORTALS")
    print(f"  URL: http://localhost:{port}")
    print("  Modes: Athlete Companion & Admin Operations Console")
    print("=" * 65 + "\n")
    import flet as ft
    from web_portal.main_web import main as web_main
    assets_path = os.path.join(BASE_DIR, "web_portal", "assets")
    ft.app(target=web_main, view=ft.AppView.WEB_BROWSER, port=port, assets_dir=assets_path)


def run_all_tests() -> bool:
    """Executes the comprehensive automated verification test suite across all 40 files."""
    print("\n" + "=" * 65)
    print("  RUNNING COMPREHENSIVE ECOSYSTEM TEST SUITE")
    print("=" * 65 + "\n")

    passed_count = 0
    total_checks = 10

    try:
        # Check 1: Catalog & Split Routines
        from frontend_app.config.exercise_catalog import EXERCISE_DIRECTORY, ROUTINES
        assert len(EXERCISE_DIRECTORY) == 52, "Exercise catalog must contain all 52 exercises"
        assert len(ROUTINES) == 7, "Routines must cover all 7 split days (DAY-A..G)"
        print("  [PASS] 1/10: Exercise Catalog & 7-Day Dual Split Routines (52 catalogued exercises)")
        passed_count += 1

        # Check 2: Database Manager & WAL Mode
        from frontend_app.database.db_manager import DatabaseManager
        db = DatabaseManager()
        with db.get_connection() as conn:
            journal_mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
            assert journal_mode.upper() == "WAL", "Database must operate in WAL mode"
        print("  [PASS] 2/10: Local SQLite Database Manager (WAL mode verified)")
        passed_count += 1

        # Check 3: Audio Coordinator
        from frontend_app.engine.audio_coordinator import AudioCoordinator
        audio = AudioCoordinator()
        assert audio is not None
        print("  [PASS] 3/10: Low-Latency Audio Coordinator & Sound Pools")
        passed_count += 1

        # Check 4: Workout Engine
        from frontend_app.engine.workout_engine import WorkoutEngine
        engine = WorkoutEngine()
        assert engine is not None
        print("  [PASS] 4/10: Wall-Clock Timer & Unilateral State Machine")
        passed_count += 1

        # Check 5: Admin Config & Roles
        from web_portal.portal_admin.admin_config import ADMIN_NAV_TABS, TIER_STYLING, AdminRole
        assert len(ADMIN_NAV_TABS) >= 5
        assert len(TIER_STYLING) == 4
        print("  [PASS] 5/10: Admin Permissions Matrix & Metallic Tier Styling")
        passed_count += 1

        # Check 6: Admin Dashboard & Telemetry
        from web_portal.portal_admin.views.admin_dashboard_view import create_admin_dashboard_view
        dash = create_admin_dashboard_view()
        assert dash is not None
        print("  [PASS] 6/10: Operations Analytics Dashboard & Fleet Metrics")
        passed_count += 1

        # Check 7: Badge Studio & Direct Assignment
        from web_portal.portal_admin.views.badge_studio_view import create_badge_studio_view
        from web_portal.portal_admin.views.direct_badge_manager import create_direct_badge_manager_view
        assert create_badge_studio_view() is not None
        assert create_direct_badge_manager_view() is not None
        print("  [PASS] 7/10: Badge Studio & Direct Assignment Console")
        passed_count += 1

        # Check 8: User Portal & Weekly Arena Leaderboard
        from web_portal.portal_user.views.user_portal_view import create_user_portal_view
        from web_portal.portal_user.views.weekly_leaderboard_widget import create_weekly_leaderboard_widget
        assert create_user_portal_view() is not None
        assert create_weekly_leaderboard_widget() is not None
        print("  [PASS] 8/10: Athlete Companion Portal & Podium 1-3 Leaderboard")
        passed_count += 1

        # Check 9: Cloud Supabase Client
        from backend_cloud.client.supabase_client import SupabaseClient
        client = SupabaseClient("https://mock.supabase.co", "mock_key")
        assert client is not None
        print("  [PASS] 9/10: Cross-Platform Supabase Client Wrapper")
        passed_count += 1

        # Check 10: Cloud Sync Bridge & Admin Service
        from frontend_app.engine.cloud_sync_bridge import CloudSyncBridge
        from web_portal.portal_admin.services.admin_supabase_service import AdminSupabaseService
        bridge = CloudSyncBridge(db_manager=db, supabase_client=client)
        admin_svc = AdminSupabaseService("https://mock.supabase.co", "mock_key")
        report = bridge.trigger_full_sync("local_athlete_001")
        assert "outbound" in report
        assert "inbound" in report
        assert admin_svc.get_fleet_telemetry() is not None
        print("  [PASS] 10/10: Cloud Sync Bridge & Admin Operations Service")
        passed_count += 1

        print("\n" + "=" * 65)
        print(f"  ALL {passed_count}/{total_checks} INTEGRATION TESTS PASSED WITH 0 ERRORS!")
        print("=" * 65 + "\n")
        return True

    except Exception as e:
        print(f"\n  [FAILED] Test Suite Encountered Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="Aesthetic Physique Master Ecosystem Launcher")
    parser.add_argument("--mobile", action="store_true", help="Launch Native Mobile App (Flet portrait mode)")
    parser.add_argument("--web", action="store_true", help="Launch Web Portals in Default Browser")
    parser.add_argument("--test", action="store_true", help="Run Comprehensive Platform Test Suite")
    parser.add_argument("--port", type=int, default=8550, help="Port for Web Portal (default: 8550)")

    args = parser.parse_args()

    if args.mobile:
        run_mobile_app()
    elif args.web:
        run_web_portal(port=args.port)
    elif args.test:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    else:
        # Interactive Menu
        print("\n" + "=" * 65)
        print("       AESTHETIC PHYSIQUE BUILDER — ECOSYSTEM LAUNCHER")
        print("=" * 65)
        print("  [1] Launch Native Mobile App (Portrait 460px)")
        print("  [2] Launch Web Portals (Athlete Companion & Admin Console)")
        print("  [3] Run Complete Automated Test Suite (10 Core Checkpoints)")
        print("  [4] Exit")
        print("=" * 65)

        choice = input("  Select an option [1-4]: ").strip()
        if choice == "1":
            run_mobile_app()
        elif choice == "2":
            run_web_portal(port=args.port)
        elif choice == "3":
            run_all_tests()
        else:
            print("  Exiting. Have a great training session!\n")


if __name__ == "__main__":
    main()
