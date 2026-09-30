"""
Aesthetic Physique Builder - Rest Interval Panel Screen
Relative Path: frontend_app/views/workout/rest_panel_view.py
Architectural Role: Inter-set and intra-set recovery screen (Slide 12).
Displays countdown clock, upcoming exercise GIF preview, '+20s' rest extension,
and 'SKIP' button to immediately resume the workout.
"""

import os
import flet as ft
from typing import Dict, Any

from config.exercise_catalog import EXERCISE_DIRECTORY
from config.default_config import WORKOUTS_MEDIA_DIR
from engine.workout_engine import workout_engine
from views.responsive_wrapper import create_responsive_view


def create_rest_panel_view(page: ft.Page) -> ft.View:
    """
    Renders the Rest Countdown Screen with upcoming exercise previews.
    """
    # Top Progress Bar
    progress_bar = ft.ProgressBar(
        value=0.0,
        color="#10B981",
        bgcolor="#1E293B",
        height=6,
    )

    # Next exercise banner title
    next_banner_text = ft.Text(
        value="NEXT: Upcoming Exercise",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.LIGHT_BLUE_300,
        text_align=ft.TextAlign.CENTER,
    )

    # Upcoming exercise preview GIF
    upcoming_gif = ft.Image(
        src="",
        width=380,
        height=220,
        fit=ft.ImageFit.CONTAIN,
        border_radius=12,
        opacity=0.75,  # Subtle dimmed opacity during rest
    )

    # Central Countdown Clock Display
    rest_timer_text = ft.Text(
        value="00:00s",
        size=52,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )

    rest_subtitle_text = ft.Text(
        value="REST & RECOVER",
        size=13,
        weight=ft.FontWeight.BOLD,
        color="#34D399",
        style=ft.TextStyle(letter_spacing=2.0),
    )

    # --------------------------------------------------------------------------
    # Engine Event Subscriptions
    # --------------------------------------------------------------------------
    def _on_engine_tick(remaining_seconds: int, fraction: float):
        try:
            if workout_engine.current_sub_phase in ("INTRA_SET_REST", "INTER_SET_REST"):
                mins = remaining_seconds // 60
                secs = remaining_seconds % 60
                rest_timer_text.value = f"{mins:02d}:{secs:02d}s"
                progress_bar.value = fraction
                page.update()
        except Exception:
            pass

    def _on_engine_state_change(sub_phase: str, data: Dict[str, Any]):
        try:
            if sub_phase == "ACTIVE_SET":
                page.go("/workout/player")
            elif sub_phase == "COMPLETED":
                page.go("/workouts")
        except Exception:
            pass

    workout_engine.on_tick_callback = _on_engine_tick
    workout_engine.on_state_change_callback = _on_engine_state_change

    def _load_upcoming_preview():
        """Determines the upcoming exercise / limb side to preview."""
        if not workout_engine.exercises:
            workout_engine.load_routine("DAY-A", "evening")

        if workout_engine.current_exercise_index < len(workout_engine.exercises):
            current_item = workout_engine.exercises[workout_engine.current_exercise_index]
        else:
            current_item = {"exercise_id": "hang1"}

        ex_meta = EXERCISE_DIRECTORY.get(current_item["exercise_id"], {})
        name = ex_meta.get("name", "Exercise")
        asset_file = ex_meta.get("animation_asset", "hang1.gif")

        if workout_engine.current_sub_phase == "INTRA_SET_REST":
            next_banner_text.value = f"NEXT: {name} (Right Side)"
            rest_subtitle_text.value = "SWITCH SIDES RECOVERY"
        else:
            next_banner_text.value = f"NEXT: {name}"
            rest_subtitle_text.value = "INTER-SET REST & RECOVERY"

        full_asset_path = str(WORKOUTS_MEDIA_DIR / asset_file)
        if os.path.exists(full_asset_path):
            upcoming_gif.src = full_asset_path
        else:
            upcoming_gif.src = ""

        # Set initial timer display
        rest_timer_text.value = f"00:{workout_engine.total_phase_duration:02d}s"

    # --------------------------------------------------------------------------
    # Handlers
    # --------------------------------------------------------------------------
    def _add_20s_rest(e):
        workout_engine.add_rest_time(20)
        page.update()

    def _skip_rest_tapped(e):
        workout_engine.skip_rest()

    _load_upcoming_preview()

    # Upcoming Preview Media Container
    media_preview_container = ft.Container(
        content=ft.Stack(
            controls=[
                upcoming_gif,
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.FORWARD_ROUNDED, size=16, color=ft.colors.LIGHT_BLUE_400),
                            next_banner_text,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=6,
                    ),
                    bgcolor="#0F172AEE",
                    border_radius=8,
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    alignment=ft.alignment.center,
                ),
            ],
            alignment=ft.alignment.top_center,
        ),
        width=380,
        height=220,
        bgcolor="#0F172A",
        border=ft.border.all(1, "#1E293B"),
        border_radius=16,
        alignment=ft.alignment.center,
        margin=ft.margin.symmetric(vertical=8),
    )

    # Rest Countdown Section
    countdown_section = ft.Column(
        controls=[
            rest_subtitle_text,
            rest_timer_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4,
    )

    # Action Modifiers ("+20s" and "SKIP")
    actions_row = ft.Container(
        content=ft.Row(
            controls=[
                # +20s Button
                ft.OutlinedButton(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.MORE_TIME_ROUNDED, size=18, color=ft.colors.LIGHT_BLUE_400),
                            ft.Text("+20s", size=15, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        ],
                        tight=True,
                        spacing=6,
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=14),
                        side=ft.BorderSide(1, "#334155"),
                    ),
                    height=52,
                    expand=1,
                    on_click=_add_20s_rest,
                ),
                # SKIP Button
                ft.ElevatedButton(
                    content=ft.Row(
                        controls=[
                            ft.Text("SKIP", size=15, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Icon(ft.icons.FAST_FORWARD_ROUNDED, size=20, color=ft.colors.WHITE),
                        ],
                        tight=True,
                        spacing=6,
                    ),
                    bgcolor=ft.colors.LIGHT_BLUE_600,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14)),
                    height=52,
                    expand=1,
                    on_click=_skip_rest_tapped,
                ),
            ],
            spacing=14,
        ),
        padding=ft.padding.only(top=10, bottom=16),
    )

    content_column = ft.Column(
        controls=[
            progress_bar,
            media_preview_container,
            countdown_section,
            actions_row,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=10,
    )

    return create_responsive_view(
        route="/workout/rest",
        controls=[content_column],
        page=page,
        scroll=False,
        bg_color="#020617",
    )
