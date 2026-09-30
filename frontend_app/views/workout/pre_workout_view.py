"""
Aesthetic Physique Builder - Pre-Workout Session Overview
Relative Path: frontend_app/views/workout/pre_workout_view.py
Architectural Role: Previews workout routine details (Slides 8, 9 & 10),
renders the dynamic Requirements Shelf, previews exercises and GIFs,
and resolves Session Recovery states: 'Start' vs 'Continue (X%)' & 'Restart'.
"""

import flet as ft
from typing import Optional, Dict, Any, List

from config.exercise_catalog import (
    get_routine, get_exercise_details, EXERCISE_DIRECTORY
)
from config.default_config import WORKOUTS_MEDIA_DIR, DAY_ROUTINE_NAMES
from database.db_manager import db
from engine.workout_engine import workout_engine
from views.components.requirements_shelf import create_requirements_shelf
from views.responsive_wrapper import create_responsive_view


def create_pre_workout_view(
    page: ft.Page,
    day_id: str = "DAY-A",
    session_type: str = "evening"
) -> ft.View:
    """
    Constructs the Pre-Workout overview view with exercise previews,
    gear prerequisites, and state interruption recovery buttons.
    """
    routine = get_routine(day_id, session_type)
    if not routine:
        routine = {"name": f"{day_id} Routine", "expected_time_mins": 0, "exercises": []}

    routine_exercises: List[Dict[str, Any]] = routine.get("exercises", [])
    expected_time: int = routine.get("expected_time_mins", 30)

    # Check for cached session progress in SQLite
    cached_session = db.get_active_session()
    has_resumable_progress = False
    saved_progress_pct = 0

    if cached_session and cached_session.get("day_id") == day_id and cached_session.get("session_type") == session_type:
        saved_progress_pct = cached_session.get("completion_percentage", 0)
        has_resumable_progress = saved_progress_pct > 0

    # Handlers
    def _start_clean_workout(e=None):
        db.clear_active_session()
        workout_engine.load_routine(day_id, session_type)
        page.go("/workout/player")

    def _continue_saved_workout(e=None):
        if cached_session:
            workout_engine.resume_from_saved_state(cached_session)
            page.go("/workout/player")
        else:
            _start_clean_workout()

    def _restart_workout(e=None):
        db.clear_active_session()
        _start_clean_workout()

    # Header Row with Back Button & Session Title
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                    icon_color=ft.colors.WHITE,
                    icon_size=20,
                    tooltip="Back to Workouts",
                    on_click=lambda e: page.go("/workouts"),
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            value=f"{day_id} • {session_type.capitalize()} Session",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE,
                        ),
                        ft.Text(
                            value=DAY_ROUTINE_NAMES.get(day_id, routine.get("name", "")),
                            size=12,
                            color=ft.colors.LIGHT_BLUE_300,
                            no_wrap=True,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(bottom=10),
    )

    # Routine Summary Strip (No. of Exercises | Expected Time)
    summary_strip = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.FORMAT_LIST_NUMBERED_ROUNDED, size=16, color=ft.colors.LIGHT_BLUE_400),
                        ft.Text(f"Exercises: {len(routine_exercises)}", size=13, weight=ft.FontWeight.W_600, color=ft.colors.WHITE),
                    ],
                    spacing=6,
                ),
                ft.Text("•", color=ft.colors.GREY_600),
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.TIMER_OUTLINED, size=16, color=ft.colors.AMBER_400),
                        ft.Text(f"Expected time: {expected_time} mins", size=13, weight=ft.FontWeight.W_600, color=ft.colors.WHITE),
                    ],
                    spacing=6,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor="#0B132B",
        border=ft.border.all(1, "#1E293B"),
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=14, vertical=10),
    )

    # Dynamic Requirements Shelf
    requirements_shelf = create_requirements_shelf(day_id, session_type)

    # Exercise Cards List
    exercise_cards = []
    for idx, item in enumerate(routine_exercises, start=1):
        ex_meta = EXERCISE_DIRECTORY.get(item["exercise_id"], {})
        name = ex_meta.get("name", item["exercise_id"])
        sets_count = item.get("sets", 1)
        mode = ex_meta.get("execution_mode", "repetition_count")
        target_val = item.get("target", ex_meta.get("default_target_value", 15))
        asset_file = ex_meta.get("animation_asset", "hang1.gif")
        asset_path = str(WORKOUTS_MEDIA_DIR / asset_file)

        target_desc = f"{sets_count} sets • {target_val}s hold" if mode == "timed_hold" else f"{sets_count} sets • {target_val} reps"
        if mode == "until_failure":
            target_desc = f"{sets_count} sets • Until Failure"

        card = ft.Container(
            content=ft.Row(
                controls=[
                    # Thumbnail Image Preview
                    ft.Container(
                        content=ft.Image(
                            src=asset_path,
                            width=70,
                            height=55,
                            fit=ft.ImageFit.COVER,
                            border_radius=8,
                            error_content=ft.Icon(ft.icons.FITNESS_CENTER, color=ft.colors.GREY_500, size=24),
                        ),
                        bgcolor="#020617",
                        border_radius=8,
                        border=ft.border.all(1, "#334155"),
                    ),
                    # Exercise Details Column
                    ft.Column(
                        controls=[
                            ft.Text(
                                value=f"{idx}. {name}",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                value=target_desc,
                                size=12,
                                color=ft.colors.LIGHT_BLUE_400,
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                        spacing=3,
                        expand=True,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#0F172A",
            border=ft.border.all(1, "#1E293B"),
            border_radius=12,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=8),
        )
        exercise_cards.append(card)

    exercise_list_view = ft.ListView(
        controls=exercise_cards,
        spacing=0,
        expand=True,
    )

    # Action Button Bar (Clean Run vs Interrupted State Recovery)
    if has_resumable_progress:
        action_bar = ft.Container(
            content=ft.Row(
                controls=[
                    ft.OutlinedButton(
                        text="Restart",
                        icon=ft.icons.REPLAY_ROUNDED,
                        style=ft.ButtonStyle(
                            color=ft.colors.RED_400,
                            side=ft.BorderSide(1, ft.colors.RED_500),
                            shape=ft.RoundedRectangleBorder(radius=12),
                        ),
                        height=48,
                        expand=1,
                        on_click=_restart_workout,
                    ),
                    ft.ElevatedButton(
                        text=f"Continue ({saved_progress_pct}%)",
                        icon=ft.icons.PLAY_ARROW_ROUNDED,
                        bgcolor=ft.colors.LIGHT_BLUE_600,
                        color=ft.colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                        height=48,
                        expand=2,
                        on_click=_continue_saved_workout,
                    ),
                ],
                spacing=12,
            ),
            padding=ft.padding.only(top=10, bottom=6),
        )
    else:
        action_bar = ft.Container(
            content=ft.ElevatedButton(
                text="Start Workout",
                icon=ft.icons.PLAY_ARROW_ROUNDED,
                bgcolor=ft.colors.LIGHT_BLUE_600,
                color=ft.colors.WHITE,
                width=420,
                height=48,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                on_click=_start_clean_workout,
            ),
            padding=ft.padding.only(top=10, bottom=6),
        )

    return create_responsive_view(
        route=f"/workout/preview?day={day_id}&session={session_type}",
        controls=[
            header,
            summary_strip,
            requirements_shelf,
            exercise_list_view,
            action_bar,
        ],
        page=page,
        scroll=False,
        bg_color="#020617",
    )
