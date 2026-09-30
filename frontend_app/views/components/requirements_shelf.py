"""
Aesthetic Physique Builder - Workout Requirements Shelf Component
Relative Path: frontend_app/views/components/requirements_shelf.py
Architectural Role: Reusable dynamic equipment banner displayed on the
Pre-Workout screen (Slides 9 & 10) to preview required physical gear
before session launch, eliminating mid-workout interruptions.
"""

import flet as ft
from typing import List
from config.exercise_catalog import get_routine_equipment


def create_requirements_shelf(day_id: str, session_type: str = "evening") -> ft.Container:
    """
    Constructs a responsive equipment badge shelf for the specified day and session.
    Dynamically maps equipment types to athletic icons and styled pill capsules.
    """
    equipment_items: List[str] = get_routine_equipment(day_id, session_type)

    # Icon mapping for equipment taxonomy
    icon_map = {
        "Dumbbells": ft.icons.FITNESS_CENTER,
        "Mat": ft.icons.SELF_IMPROVEMENT,
        "Chair": ft.icons.CHAIR,
        "Pull-Up Bar": ft.icons.ACCESSIBILITY_NEW,
        "Exercise Bench": ft.icons.BED,
        "None (Rest Day)": ft.icons.BEDTIME,
        "Bodyweight Only (No Equipment)": ft.icons.CHECK_CIRCLE_OUTLINE,
    }

    chips = []
    for item in equipment_items:
        icon = icon_map.get(item, ft.icons.FITNESS_CENTER)
        is_empty_or_rest = item in ("None (Rest Day)", "Bodyweight Only (No Equipment)")

        chip = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=icon,
                        size=15,
                        color=ft.colors.EMERALD_400 if is_empty_or_rest else ft.colors.LIGHT_BLUE_400,
                    ),
                    ft.Text(
                        value=item,
                        size=12,
                        weight=ft.FontWeight.W_600,
                        color=ft.colors.WHITE if not is_empty_or_rest else ft.colors.EMERALD_200,
                    ),
                ],
                tight=True,
                spacing=6,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor="#1E293B" if not is_empty_or_rest else "#064E3B",
            border=ft.border.all(1, "#334155" if not is_empty_or_rest else "#059669"),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        )
        chips.append(chip)

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.HANDYMAN_OUTLINED, size=16, color=ft.colors.GREY_400),
                        ft.Text(
                            value="Requirements / Equipment Needed",
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.GREY_300,
                        ),
                    ],
                    spacing=6,
                ),
                ft.Row(
                    controls=chips,
                    wrap=True,
                    spacing=8,
                    run_spacing=8,
                ),
            ],
            spacing=8,
        ),
        bgcolor="#0F172A",
        border=ft.border.all(1, "#1E293B"),
        border_radius=14,
        padding=ft.padding.all(12),
        margin=ft.margin.symmetric(vertical=8),
    )
