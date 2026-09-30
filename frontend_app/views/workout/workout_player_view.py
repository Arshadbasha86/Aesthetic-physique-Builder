"""
Aesthetic Physique Builder - Active Workout Player Screen
Relative Path: frontend_app/views/workout/workout_player_view.py
Architectural Role: Core in-workout execution screen (Slide 11). Displays 16:9
looping exercise demonstration GIFs, live wall-clock timers, unilateral limb tags,
touch-lock suppressor mask, and Done checkmark with Until-Failure keypad integration.
"""

import os
import flet as ft
from typing import Optional, Dict, Any

from config.exercise_catalog import EXERCISE_DIRECTORY
from config.default_config import WORKOUTS_MEDIA_DIR, COLOR_LOCK_OVERLAY
from engine.workout_engine import workout_engine
from views.components.numeric_keypad_modal import NumericKeypadModal
from views.responsive_wrapper import create_responsive_view


def create_workout_player_view(page: ft.Page) -> ft.View:
    """
    Renders the active in-workout execution player.
    """
    # Reactive UI Controls
    progress_bar = ft.ProgressBar(
        value=0.0,
        color=ft.colors.LIGHT_BLUE_400,
        bgcolor="#1E293B",
        height=6,
    )

    exercise_name_text = ft.Text(
        value="Exercise Name",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )

    set_counter_text = ft.Text(
        value="Set 1 of 1",
        size=13,
        color=ft.colors.GREY_400,
        text_align=ft.TextAlign.CENTER,
    )

    unilateral_tag = ft.Container(
        content=ft.Text(
            value="",
            size=11,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.AMBER_300,
        ),
        bgcolor="#78350F44",
        border=ft.border.all(1, ft.colors.AMBER_600),
        border_radius=6,
        padding=ft.padding.symmetric(horizontal=8, vertical=2),
        visible=False,
    )

    gif_image = ft.Image(
        src="",
        width=380,
        height=240,
        fit=ft.ImageFit.CONTAIN,
        border_radius=12,
    )

    timer_metric_text = ft.Text(
        value="00:00",
        size=46,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.LIGHT_BLUE_400,
        text_align=ft.TextAlign.CENTER,
    )

    metric_sublabel = ft.Text(
        value="Remaining Hold",
        size=12,
        color=ft.colors.GREY_400,
    )

    lock_icon_button = ft.IconButton(
        icon=ft.icons.LOCK_OPEN_ROUNDED,
        icon_color=ft.colors.GREY_400,
        icon_size=24,
        tooltip="Lock Screen Controls",
    )

    # Transparent touch-lock suppressor overlay
    touch_lock_overlay = ft.Container(
        bgcolor=COLOR_LOCK_OVERLAY,
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Icon(ft.icons.LOCK_ROUNDED, size=54, color=ft.colors.LIGHT_BLUE_400),
                ft.Text("SCREEN LOCKED", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Text("Tap lock icon above to unlock controls", size=12, color=ft.colors.GREY_300),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        expand=True,
        visible=False,
    )

    # --------------------------------------------------------------------------
    # Engine Event Subscriptions
    # --------------------------------------------------------------------------
    def _on_engine_tick(remaining_seconds: int, fraction: float):
        try:
            if workout_engine.current_sub_phase == "ACTIVE_SET":
                mins = remaining_seconds // 60
                secs = remaining_seconds % 60
                timer_metric_text.value = f"{mins:02d}:{secs:02d}"
                progress_bar.value = fraction
                page.update()
        except Exception:
            pass

    def _on_engine_state_change(sub_phase: str, data: Dict[str, Any]):
        try:
            if sub_phase == "ACTIVE_SET":
                _refresh_player_state()
            elif sub_phase in ("INTRA_SET_REST", "INTER_SET_REST"):
                page.go("/workout/rest")
            elif sub_phase == "COMPLETED":
                page.go("/workouts")
        except Exception:
            pass

    def _on_request_reps_input(ex_name: str, target_val: int):
        modal = NumericKeypadModal(
            page=page,
            exercise_name=ex_name,
            initial_reps=target_val,
            on_confirm=lambda reps: workout_engine.complete_current_set(actual_reps=reps),
        )
        modal.show()

    workout_engine.on_tick_callback = _on_engine_tick
    workout_engine.on_state_change_callback = _on_engine_state_change
    workout_engine.on_request_reps_input_callback = _on_request_reps_input

    def _refresh_player_state():
        if workout_engine.current_exercise_index >= len(workout_engine.exercises):
            return

        current_item = workout_engine.exercises[workout_engine.current_exercise_index]
        ex_meta = EXERCISE_DIRECTORY.get(current_item["exercise_id"], {})
        name = ex_meta.get("name", "Exercise")
        mode = ex_meta.get("execution_mode", "repetition_count")
        sets_total = current_item.get("sets", 1)
        current_set = workout_engine.current_set_index + 1

        exercise_name_text.value = name
        set_counter_text.value = f"Set {current_set} of {sets_total}"

        # Unilateral limb tag
        if ex_meta.get("unilateral", False):
            unilateral_tag.visible = True
            unilateral_tag.content.value = f"{workout_engine.active_side} SIDE"
        else:
            unilateral_tag.visible = False

        # Load animated GIF asset
        asset_file = ex_meta.get("animation_asset", "hang1.gif")
        full_asset_path = str(WORKOUTS_MEDIA_DIR / asset_file)
        if os.path.exists(full_asset_path):
            gif_image.src = full_asset_path
        else:
            gif_image.src = ""

        # Update metric labels
        if mode == "timed_hold":
            metric_sublabel.value = "Hold Duration (Seconds)"
            timer_metric_text.value = f"00:{workout_engine.total_phase_duration:02d}"
        elif mode == "until_failure":
            metric_sublabel.value = "Burnout Target: Until Failure"
            timer_metric_text.value = f"{current_item.get('target', 15)}"
        else:
            metric_sublabel.value = "Target Repetitions"
            timer_metric_text.value = f"{current_item.get('target', 15)}"

        lock_icon_button.icon = ft.icons.LOCK_ROUNDED if workout_engine.is_screen_locked else ft.icons.LOCK_OPEN_ROUNDED
        touch_lock_overlay.visible = workout_engine.is_screen_locked
        page.update()

    # --------------------------------------------------------------------------
    # Handlers
    # --------------------------------------------------------------------------
    def _toggle_lock(e):
        locked = workout_engine.toggle_screen_lock()
        lock_icon_button.icon = ft.icons.LOCK_ROUNDED if locked else ft.icons.LOCK_OPEN_ROUNDED
        touch_lock_overlay.visible = locked
        page.update()

    def _on_done_tapped(e):
        if not workout_engine.is_screen_locked:
            workout_engine.complete_current_set()

    def _show_exit_confirmation(e):
        def _confirm_exit(ce):
            dialog.open = False
            workout_engine.pause_session()
            page.update()
            page.go("/workouts")

        def _cancel_exit(ce):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#0F172A",
            title=ft.Text("Quit Workout?", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            content=ft.Text("Your completed sets are safely saved. You can continue anytime.", size=13, color=ft.colors.GREY_300),
            actions=[
                ft.TextButton("Resume", on_click=_cancel_exit),
                ft.ElevatedButton("Save & Exit", bgcolor=ft.colors.RED_700, color=ft.colors.WHITE, on_click=_confirm_exit),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    lock_icon_button.on_click = _toggle_lock

    # Top Header Row
    top_header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=ft.colors.WHITE,
                icon_size=20,
                on_click=_show_exit_confirmation,
            ),
            ft.Column(
                controls=[
                    exercise_name_text,
                    ft.Row(
                        controls=[set_counter_text, unilateral_tag],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2,
                expand=True,
            ),
            lock_icon_button,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # GIF Viewport Container (16:9 fixed ratio)
    gif_container = ft.Container(
        content=gif_image,
        width=380,
        height=240,
        bgcolor="#0F172A",
        border=ft.border.all(1, "#1E293B"),
        border_radius=16,
        alignment=ft.alignment.center,
        margin=ft.margin.symmetric(vertical=10),
    )

    # Target & Timer Section
    metrics_section = ft.Column(
        controls=[
            timer_metric_text,
            metric_sublabel,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4,
    )

    # Primary Action Button ("Done" Checkmark)
    done_button = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.CHECK_CIRCLE_ROUNDED, size=24, color=ft.colors.WHITE),
                    ft.Text("DONE SET", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ],
                tight=True,
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.LIGHT_BLUE_600,
            width=380,
            height=54,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=16)),
            on_click=_on_done_tapped,
        ),
        padding=ft.padding.only(top=16, bottom=10),
    )

    # Main Stack wrapping controls and touch-lock barrier
    main_stack = ft.Stack(
        controls=[
            ft.Column(
                controls=[
                    progress_bar,
                    top_header,
                    gif_container,
                    metrics_section,
                    done_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                spacing=8,
            ),
            touch_lock_overlay,
        ],
        expand=True,
    )

    # Initial state mount trigger
    workout_engine.start_workout()
    _refresh_player_state()

    return create_responsive_view(
        route="/workout/player",
        controls=[main_stack],
        page=page,
        scroll=False,
        bg_color="#020617",
    )
