"""
Aesthetic Physique Builder - Application Entry Point & Navigation Orchestrator
Relative Path: frontend_app/main.py
Architectural Role: Master entry point and routing coordinator.
Initializes background services (Audio Coordinator, SQLite WAL mode, Sync Worker),
configures strict 460px portrait window bounds, and manages route transitions
across Onboarding, Home Dashboard, Workout Player, Recovery, and Settings.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add root folder to module search path
sys.path.append(str(Path(__file__).resolve().parent))

import flet as ft
from typing import Dict, Any, List

from config.default_config import (
    APP_NAME, MOBILE_VIEWPORT_WIDTH, MOBILE_VIEWPORT_HEIGHT,
    DEFAULT_WEEK_SCHEDULE, DAY_ROUTINE_NAMES
)
from config.exercise_catalog import get_routine
from database.db_manager import db
from engine.audio_coordinator import audio_coordinator
from engine.sync_worker import sync_worker

# View imports
from views.responsive_wrapper import create_responsive_view
from views.splash_view import create_splash_view
from views.onboarding.disclaimer_view import create_disclaimer_view
from views.onboarding.warning_view import create_warning_view
from views.onboarding.plan_alignment_view import create_plan_alignment_view
from views.workout.pre_workout_view import create_pre_workout_view
from views.workout.workout_player_view import create_workout_player_view
from views.workout.rest_panel_view import create_rest_panel_view
from views.activity.activity_ledger_view import create_activity_ledger_view
from views.profile.profile_view import create_profile_view
from views.profile.badge_showcase_view import create_badge_showcase_view
from views.settings.settings_view import create_settings_view
from views.support.support_desk_view import create_support_desk_view


def build_home_workouts_view(page: ft.Page) -> ft.View:
    """
    Renders the Home Workouts Dashboard (Slide 7 & 8).
    Displays the week cycle selector, streak indicator, and Morning/Evening session cards.
    """
    week_schedule = db.get_week_schedule()
    streak_data = db.get_streak()
    current_streak = streak_data.get("current_streak_days", 1)

    # Determine today's day of the week
    today_name = datetime.now().strftime("%A")  # 'Monday', 'Tuesday', etc.
    active_selected_day = [today_name]          # State holder in list for closure access

    session_cards_column = ft.Column(spacing=12, expand=True)

    def _render_session_cards(day: str):
        routine_day_id = week_schedule.get(day, "DAY-A")
        routine_name = DAY_ROUTINE_NAMES.get(routine_day_id, routine_day_id)

        morning_data = get_routine(routine_day_id, "morning") or {}
        evening_data = get_routine(routine_day_id, "evening") or {}

        morning_ex_count = len(morning_data.get("exercises", []))
        evening_ex_count = len(evening_data.get("exercises", []))

        def _make_session_tile(title: str, name: str, ex_count: int, time_mins: int, session_key: str):
            is_rest = (ex_count == 0)
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(
                                            ft.icons.WB_SUNNY_ROUNDED if session_key == "morning" else ft.icons.NIGHTLIGHT_ROUNDED,
                                            color=ft.colors.AMBER_400 if session_key == "morning" else ft.colors.LIGHT_BLUE_400,
                                            size=20,
                                        ),
                                        ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                    ],
                                    spacing=8,
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        "REST DAY" if is_rest else f"{time_mins} mins",
                                        size=11,
                                        weight=ft.FontWeight.BOLD,
                                        color="#10B981" if is_rest else ft.colors.LIGHT_BLUE_300,
                                    ),
                                    bgcolor="#020617",
                                    border=ft.border.all(1, "#1E293B"),
                                    border_radius=8,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(name, size=13, color=ft.colors.GREY_300, weight=ft.FontWeight.W_500),
                        ft.Row(
                            controls=[
                                ft.Row([ft.Icon(ft.icons.FITNESS_CENTER, size=14, color=ft.colors.GREY_400), ft.Text(f"{ex_count} Exercises", size=12, color=ft.colors.GREY_400)], spacing=4),
                                ft.Text("•", color=ft.colors.GREY_600),
                                ft.Text("Tap to preview session", size=12, color=ft.colors.LIGHT_BLUE_400),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ) if not is_rest else ft.Text("Full recovery & muscle protein synthesis.", size=12, color=ft.colors.GREY_400),
                    ],
                    spacing=8,
                ),
                bgcolor="#0F172A",
                border=ft.border.all(1, "#1E293B"),
                border_radius=14,
                padding=ft.padding.all(16),
                margin=ft.margin.only(bottom=8),
                on_click=None if is_rest else (lambda e, d=routine_day_id, s=session_key: page.go(f"/workout/preview?day={d}&session={s}")),
            )

        session_cards_column.controls = [
            ft.Text(f"{day} • {routine_day_id}", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_400),
            _make_session_tile("Morning Workout", morning_data.get("name", "Stretching & Mobility"), morning_ex_count, morning_data.get("expected_time_mins", 20), "morning"),
            _make_session_tile("Evening Workout", evening_data.get("name", "Resistance Training"), evening_ex_count, evening_data.get("expected_time_mins", 45), "evening"),
        ]

    # Top Brand Bar & Streak
    top_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(APP_NAME, size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ft.Text("In Workouts Dashboard", size=11, color=ft.colors.GREY_400),
                    ],
                    spacing=1,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, color=ft.colors.ORANGE_400, size=20),
                            ft.Text(f"{current_streak}", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ],
                        spacing=4,
                    ),
                    bgcolor="#0F172A",
                    border=ft.border.all(1, "#F59E0B66"),
                    border_radius=12,
                    padding=ft.padding.symmetric(horizontal=10, vertical=6),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(bottom=10),
    )

    # 7-Day Horizontal Calendar Day Tabs
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_chips = []

    def _select_day(day_name: str):
        active_selected_day[0] = day_name
        _update_calendar_chips()
        _render_session_cards(day_name)
        page.update()

    calendar_row = ft.Row(
        scroll=ft.ScrollMode.AUTO,
        spacing=8,
    )

    def _update_calendar_chips():
        chips = []
        for day in days_order:
            is_active = (day == active_selected_day[0])
            routine_day_id = week_schedule.get(day, "DAY-A")
            chip = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(day[:3].upper(), size=11, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE if is_active else ft.colors.GREY_400),
                        ft.Text(routine_day_id[-1], size=14, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_400 if is_active else ft.colors.GREY_500),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
                width=52,
                height=56,
                bgcolor="#1E293B" if is_active else "#0F172A",
                border=ft.border.all(1.5 if is_active else 1, ft.colors.LIGHT_BLUE_500 if is_active else "#1E293B"),
                border_radius=12,
                alignment=ft.alignment.center,
                on_click=lambda e, d=day: _select_day(d),
            )
            chips.append(chip)
        calendar_row.controls = chips

    _update_calendar_chips()
    _render_session_cards(today_name)

    # Bottom Navigation Bar
    bottom_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    content=ft.Column([ft.Icon(ft.icons.FITNESS_CENTER_ROUNDED, color=ft.colors.LIGHT_BLUE_400, size=20), ft.Text("Workouts", size=10, color=ft.colors.LIGHT_BLUE_400, weight=ft.FontWeight.BOLD)], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    on_click=lambda e: page.go("/workouts"),
                ),
                ft.TextButton(
                    content=ft.Column([ft.Icon(ft.icons.MONITOR_HEART_ROUNDED, color=ft.colors.GREY_400, size=20), ft.Text("Activity", size=10, color=ft.colors.GREY_400)], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    on_click=lambda e: page.go("/activity"),
                ),
                ft.TextButton(
                    content=ft.Column([ft.Icon(ft.icons.PERSON_ROUNDED, color=ft.colors.GREY_400, size=20), ft.Text("Profile", size=10, color=ft.colors.GREY_400)], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    on_click=lambda e: page.go("/profile"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor="#0F172A",
        border=ft.border.all(1, "#1E293B"),
        border_radius=16,
        padding=ft.padding.symmetric(vertical=6),
        margin=ft.margin.only(top=6),
    )

    main_column = ft.Column(
        controls=[
            top_bar,
            calendar_row,
            ft.Divider(color="#1E293B", height=16),
            session_cards_column,
            bottom_bar,
        ],
        spacing=8,
        expand=True,
    )

    return create_responsive_view(
        route="/workouts",
        controls=[main_column],
        page=page,
        scroll=False,
        bg_color="#020617",
    )


def main(page: ft.Page):
    """
    Main Application Routing and Lifecycle Controller.
    """
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0

    # Configure desktop bounds
    try:
        page.window_width = MOBILE_VIEWPORT_WIDTH
        page.window_height = MOBILE_VIEWPORT_HEIGHT
        page.window_resizable = True
    except Exception:
        pass

    # Attach audio engine
    audio_coordinator.attach_page(page)

    # Start background sync worker
    sync_worker.start()

    def route_change(route_event):
        page.views.clear()
        route = page.route or "/"

        if route == "/" or route == "":
            page.views.append(create_splash_view(page))

        elif route == "/onboarding/disclaimer":
            page.views.append(create_disclaimer_view(page, from_settings=False))

        elif route == "/onboarding/warning":
            page.views.append(create_warning_view(page, from_settings=False))

        elif route == "/onboarding/plan_alignment":
            page.views.append(create_plan_alignment_view(page, from_settings=False))

        elif route == "/workouts":
            page.views.append(build_home_workouts_view(page))

        elif route.startswith("/workout/preview"):
            # Parse query parameters if present
            day_id = "DAY-A"
            session_type = "evening"
            if "?" in route:
                params_str = route.split("?")[1]
                params = dict(p.split("=") for p in params_str.split("&") if "=" in p)
                day_id = params.get("day", "DAY-A")
                session_type = params.get("session", "evening")
            page.views.append(create_pre_workout_view(page, day_id=day_id, session_type=session_type))

        elif route == "/workout/player":
            page.views.append(create_workout_player_view(page))

        elif route == "/workout/rest":
            page.views.append(create_rest_panel_view(page))

        elif route == "/activity":
            page.views.append(create_activity_ledger_view(page))

        elif route == "/profile":
            page.views.append(create_profile_view(page))

        elif route == "/profile/badges":
            page.views.append(create_badge_showcase_view(page))

        elif route == "/settings":
            page.views.append(create_settings_view(page))

        elif route == "/settings/disclaimer":
            page.views.append(create_disclaimer_view(page, from_settings=True))

        elif route == "/settings/warning":
            page.views.append(create_warning_view(page, from_settings=True))

        elif route == "/settings/plan_update":
            page.views.append(create_plan_alignment_view(page, from_settings=True))

        elif route == "/support":
            page.views.append(create_support_desk_view(page))

        else:
            page.views.append(build_home_workouts_view(page))

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Initial route trigger
    page.go(page.route or "/")


if __name__ == "__main__":
    assets_dir_path = str(Path(__file__).parent / "assets")
    ft.app(target=main, assets_dir=assets_dir_path)
