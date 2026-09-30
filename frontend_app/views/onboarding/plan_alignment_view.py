"""
Aesthetic Physique Builder - Week Plan Alignment Wizard
Relative Path: frontend_app/views/onboarding/plan_alignment_view.py
Architectural Role: Phase 4 of Startup Lifecycle (Slide 6) & Workouts Plan Update (Slide 23).
Allows trainees to map 7 calendar days (Monday - Sunday) to custom workout routines
(DAY-A through DAY-G) or apply the default split with a single tap.
"""

import flet as ft
from typing import Dict

from config.default_config import DEFAULT_WEEK_SCHEDULE, DAY_ROUTINE_NAMES
from database.db_manager import db
from views.responsive_wrapper import create_responsive_view


def create_plan_alignment_view(page: ft.Page, from_settings: bool = False) -> ft.View:
    """
    Renders the Week Plan Alignment Wizard or Profile Settings Plan Update view.
    """
    current_schedule: Dict[str, str] = db.get_week_schedule()
    selected_mappings: Dict[str, str] = dict(current_schedule)

    dropdown_options = [
        ft.dropdown.Option(
            key=routine_id,
            text=f"{routine_id}: {DAY_ROUTINE_NAMES.get(routine_id, '')}"
        )
        for routine_id in ["DAY-A", "DAY-B", "DAY-C", "DAY-D", "DAY-E", "DAY-F", "DAY-G"]
    ]

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Handlers
    def _on_plan_selected(day: str, new_val: str):
        selected_mappings[day] = new_val

    def _save_and_finish(e=None):
        db.update_week_schedule(selected_mappings)
        db.set_onboarding_completed()
        if from_settings:
            page.go("/settings")
        else:
            page.go("/workouts")

    def _apply_default_split(e=None):
        db.update_week_schedule(DEFAULT_WEEK_SCHEDULE)
        db.set_onboarding_completed()
        if from_settings:
            page.go("/settings")
        else:
            page.go("/workouts")

    # Header Card
    header = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                            icon_color=ft.colors.WHITE,
                            icon_size=18,
                            visible=from_settings,
                            on_click=lambda e: page.go("/settings"),
                        ),
                        ft.Text(
                            value="Workouts Plan Update" if from_settings else "Week Plan Alignment",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE,
                        ),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Text(
                    value="Assign a routine to each calendar day or use the proven default split.",
                    size=12,
                    color=ft.colors.GREY_400,
                ),
            ],
            spacing=4,
        ),
        padding=ft.padding.only(bottom=10),
    )

    # 7-Day Calendar Cards
    day_cards = []
    for day in days_order:
        current_routine = selected_mappings.get(day, "DAY-A")

        dd = ft.Dropdown(
            value=current_routine,
            options=dropdown_options,
            dense=True,
            border_color="#334155",
            focused_border_color=ft.colors.LIGHT_BLUE_400,
            text_size=12,
            bgcolor="#0B132B",
            color=ft.colors.WHITE,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=4),
            on_change=lambda e, d=day: _on_plan_selected(d, e.control.value),
        )

        card = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            value=day[:3].upper(),
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.LIGHT_BLUE_400,
                        ),
                        width=45,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=dd,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=8,
            ),
            bgcolor="#0F172A",
            border=ft.border.all(1, "#1E293B"),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            margin=ft.margin.only(bottom=8),
        )
        day_cards.append(card)

    calendar_list = ft.ListView(
        controls=day_cards,
        spacing=0,
        expand=True,
    )

    # Bottom Actions
    actions_row = ft.Container(
        content=ft.Column(
            controls=[
                ft.ElevatedButton(
                    text="Confirm Workout Split",
                    icon=ft.icons.CHECK_CIRCLE_ROUNDED,
                    bgcolor=ft.colors.LIGHT_BLUE_600,
                    color=ft.colors.WHITE,
                    width=420,
                    height=46,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                    on_click=_save_and_finish,
                ),
                ft.TextButton(
                    content=ft.Text(
                        value="skip -> (Apply Default Split)",
                        size=13,
                        color=ft.colors.GREY_400,
                        weight=ft.FontWeight.W_600,
                    ),
                    visible=not from_settings,
                    on_click=_apply_default_split,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        padding=ft.padding.only(top=10, bottom=6),
    )

    return create_responsive_view(
        route="/onboarding/plan_alignment" if not from_settings else "/settings/plan_update",
        controls=[
            header,
            calendar_list,
            actions_row,
        ],
        page=page,
        scroll=False,
        bg_color="#020617",
    )
