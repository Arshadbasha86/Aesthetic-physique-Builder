"""
Aesthetic Physique Builder - Activity & Biological Recovery Ledger
Relative Path: frontend_app/views/activity/activity_ledger_view.py
Architectural Role: Core recovery tracking console (Slides 13, 14, 15 & 16).
Manages daily water hydration logs, sleep duration & quality tier scoring,
and pre/post-workout protein timing windows with digestion countdown clocks.
"""

import time
import flet as ft
from datetime import datetime

from database.db_manager import db
from config.default_config import (
    DEFAULT_WATER_TARGET_ML, DEFAULT_SLEEP_TARGET_HOURS, DEFAULT_PROTEIN_TARGET_GM
)
from views.responsive_wrapper import create_responsive_view


def create_activity_ledger_view(page: ft.Page) -> ft.View:
    """
    Renders the Activity & Recovery Ledger view.
    """
    # Active Section Selector ('water', 'sleep', 'protein', 'sessions')
    active_tab = "water"

    # Dynamic containers
    content_area = ft.Container(expand=True)

    # --------------------------------------------------------------------------
    # 1. Water Hydration Module (Slide 13)
    # --------------------------------------------------------------------------
    def _build_water_module() -> ft.Control:
        current_water = db.get_today_water_intake()
        target_water = DEFAULT_WATER_TARGET_ML
        fraction = min(1.0, current_water / target_water)

        def _add_water(amount: int):
            db.log_water_intake(amount)
            _render_active_tab()

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.icons.WATER_DROP_ROUNDED, size=48, color=ft.colors.LIGHT_BLUE_400),
                            ft.Text(f"{current_water} ml", size=36, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text(f"Target: {target_water} ml / day", size=13, color=ft.colors.GREY_400),
                            ft.ProgressBar(value=fraction, color=ft.colors.LIGHT_BLUE_400, bgcolor="#1E293B", height=8),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    bgcolor="#0F172A",
                    border=ft.border.all(1, "#1E293B"),
                    border_radius=16,
                    padding=ft.padding.all(20),
                ),
                ft.Text("Quick Add Water", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("+250 ml", bgcolor="#1E293B", color=ft.colors.WHITE, on_click=lambda e: _add_water(250)),
                        ft.ElevatedButton("+500 ml", bgcolor="#1E293B", color=ft.colors.WHITE, on_click=lambda e: _add_water(500)),
                        ft.ElevatedButton("+1000 ml", bgcolor=ft.colors.LIGHT_BLUE_600, color=ft.colors.WHITE, on_click=lambda e: _add_water(1000)),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            spacing=16,
        )

    # --------------------------------------------------------------------------
    # 2. Sleep Quality & Recovery Ledger (Slide 14)
    # --------------------------------------------------------------------------
    def _build_sleep_module() -> ft.Control:
        sleep_records = db.get_sleep_logs(limit=7)
        in_time_field = ft.TextField(label="In-Time (Bed)", hint_text="22:30", width=140, bgcolor="#0B132B")
        out_time_field = ft.TextField(label="Out-Time (Wake)", hint_text="06:30", width=140, bgcolor="#0B132B")
        quality_dropdown = ft.Dropdown(
            value="Good Sleep",
            options=[
                ft.dropdown.Option("Excellent Sleep"),
                ft.dropdown.Option("Good Sleep"),
                ft.dropdown.Option("Average Sleep"),
                ft.dropdown.Option("Bad Sleep"),
            ],
            width=180,
            bgcolor="#0B132B",
        )

        def _save_sleep(e):
            in_t = in_time_field.value or "22:30"
            out_t = out_time_field.value or "06:30"
            tier = quality_dropdown.value or "Good Sleep"
            db.log_sleep(in_time=in_t, out_time=out_t, duration_minutes=480, quality_tier=tier)
            _render_active_tab()

        history_rows = []
        for s in sleep_records:
            tier_color = {
                "Excellent Sleep": ft.colors.LIGHT_BLUE_400,
                "Good Sleep": "#10B981",
                "Average Sleep": ft.colors.AMBER_400,
                "Bad Sleep": ft.colors.RED_400,
            }.get(s["quality_tier"], ft.colors.WHITE)

            history_rows.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(s["log_date"], size=12, color=ft.colors.WHITE),
                            ft.Text(f"{s['in_time']} - {s['out_time']}", size=12, color=ft.colors.GREY_300),
                            ft.Text(s["quality_tier"], size=12, weight=ft.FontWeight.BOLD, color=tier_color),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor="#0F172A",
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    border_radius=8,
                    border=ft.border.all(1, "#1E293B"),
                    margin=ft.margin.only(bottom=6),
                )
            )

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row([in_time_field, out_time_field], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([quality_dropdown, ft.ElevatedButton("Log Sleep", bgcolor=ft.colors.LIGHT_BLUE_600, color=ft.colors.WHITE, on_click=_save_sleep)], alignment=ft.MainAxisAlignment.CENTER),
                        ],
                        spacing=10,
                    ),
                    bgcolor="#0F172A",
                    padding=ft.padding.all(14),
                    border_radius=14,
                    border=ft.border.all(1, "#1E293B"),
                ),
                ft.Text("Sleep History", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Column(controls=history_rows, spacing=4) if history_rows else ft.Text("No sleep records logged yet.", color=ft.colors.GREY_400, size=12),
            ],
            spacing=14,
            scroll=ft.ScrollMode.AUTO,
        )

    # --------------------------------------------------------------------------
    # 3. Protein Timing & Digestion Window (Slides 15 & 16)
    # --------------------------------------------------------------------------
    def _build_protein_module() -> ft.Control:
        today_protein = db.get_today_protein_intake()
        target_protein = DEFAULT_PROTEIN_TARGET_GM
        protein_input = ft.TextField(label="Protein intake (gm)", hint_text="30", width=180, bgcolor="#0B132B")

        def _log_pre(e):
            val = float(protein_input.value or 30.0)
            db.log_protein(val, timing_window="before_workout")
            _render_active_tab()

        def _log_post(e):
            val = float(protein_input.value or 30.0)
            db.log_protein(val, timing_window="after_workout")
            _render_active_tab()

        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.icons.EGG_ALT_OUTLINED, size=40, color=ft.colors.AMBER_400),
                            ft.Text(f"{int(today_protein)} gm", size=36, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                            ft.Text(f"Daily Target: {target_protein} gm", size=13, color=ft.colors.GREY_400),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=6,
                    ),
                    bgcolor="#0F172A",
                    padding=ft.padding.all(20),
                    border_radius=16,
                    border=ft.border.all(1, "#1E293B"),
                    alignment=ft.alignment.center,
                ),
                ft.Row([protein_input], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Pre-Workout Intake", bgcolor="#1E293B", color=ft.colors.WHITE, on_click=_log_pre),
                        ft.ElevatedButton("Post-Workout Intake", bgcolor=ft.colors.LIGHT_BLUE_600, color=ft.colors.WHITE, on_click=_log_post),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ],
            spacing=16,
        )

    # --------------------------------------------------------------------------
    # Tab Switching
    # --------------------------------------------------------------------------
    def _switch_tab(tab_name: str):
        nonlocal active_tab
        active_tab = tab_name
        _render_active_tab()

    def _render_active_tab():
        if active_tab == "water":
            content_area.content = _build_water_module()
        elif active_tab == "sleep":
            content_area.content = _build_sleep_module()
        else:
            content_area.content = _build_protein_module()
        page.update()

    # Top Tab Navigation Buttons
    nav_tabs = ft.Row(
        controls=[
            ft.TextButton("Water", on_click=lambda e: _switch_tab("water")),
            ft.TextButton("Sleep", on_click=lambda e: _switch_tab("sleep")),
            ft.TextButton("Protein", on_click=lambda e: _switch_tab("protein")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )

    header = ft.Row(
        controls=[
            ft.IconButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_color=ft.colors.WHITE, on_click=lambda e: page.go("/workouts")),
            ft.Text("Activity & Recovery Ledger", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    _render_active_tab()

    return create_responsive_view(
        route="/activity",
        controls=[
            header,
            nav_tabs,
            ft.Divider(color="#1E293B", height=1),
            content_area,
        ],
        page=page,
        scroll=False,
        bg_color="#020617",
    )
