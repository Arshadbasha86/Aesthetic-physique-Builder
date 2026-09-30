"""
Aesthetic Physique Builder - User Profile & Biometrics Hub
Relative Path: frontend_app/views/profile/profile_view.py
Architectural Role: Primary user identity showcase (Slides 20, 21 & 22).
Renders profile banner, avatar, equipped vanity title, streak counter,
biometrics input manager (Weight/Height/Age), shortcuts, and account deletion modal.
"""

import flet as ft
from database.db_manager import db
from views.responsive_wrapper import create_responsive_view


def create_profile_view(page: ft.Page) -> ft.View:
    """
    Renders the Profile & Settings Hub.
    """
    profile = db.get_user_profile()
    streak_data = db.get_streak()

    full_name = profile.get("full_name", "Athlete")
    username = profile.get("username", "athlete")
    equipped_title = profile.get("equipped_title", "Novice Trainee")
    current_streak = streak_data.get("current_streak_days", 1)

    # Biometric form controllers
    weight_field = ft.TextField(
        label="Current Weight (kg)",
        value=str(profile.get("current_weight_kg", 65.0)),
        width=170,
        bgcolor="#0B132B",
    )
    target_weight_field = ft.TextField(
        label="Target Weight (kg)",
        value=str(profile.get("target_weight_kg", 70.0)),
        width=170,
        bgcolor="#0B132B",
    )
    height_field = ft.TextField(
        label="Height (cm)",
        value=str(profile.get("height_cm", 175.0)),
        width=170,
        bgcolor="#0B132B",
    )
    age_field = ft.TextField(
        label="Age (Years)",
        value=str(profile.get("age_years", 21)),
        width=170,
        bgcolor="#0B132B",
    )
    sex_dropdown = ft.Dropdown(
        value=profile.get("biological_sex", "male"),
        options=[ft.dropdown.Option("male"), ft.dropdown.Option("female")],
        label="Biological Sex",
        width=170,
        bgcolor="#0B132B",
    )

    feedback_text = ft.Text(value="", size=12, color="#10B981")

    # --------------------------------------------------------------------------
    # Handlers
    # --------------------------------------------------------------------------
    def _save_biometrics(e):
        try:
            cw = float(weight_field.value)
            tw = float(target_weight_field.value)
            h = float(height_field.value)
            age = int(age_field.value)
            sex = sex_dropdown.value or "male"
            db.update_user_biometrics(cw, tw, h, age, sex)
            feedback_text.value = "Biometrics successfully saved!"
            feedback_text.color = "#10B981"
        except Exception as err:
            feedback_text.value = f"Invalid input: {err}"
            feedback_text.color = ft.colors.RED_400
        page.update()

    def _show_delete_account_modal(e):
        delete_input = ft.TextField(hint_text="Type DELETE to confirm", bgcolor="#0B132B")
        confirm_btn = ft.ElevatedButton("Permanently Delete", bgcolor=ft.colors.RED_700, color=ft.colors.WHITE, disabled=True)

        def _validate_delete(de):
            confirm_btn.disabled = (delete_input.value.strip() != "DELETE")
            page.update()

        def _execute_purge(pe):
            db.purge_all_local_data()
            dialog.open = False
            page.update()
            page.go("/")

        delete_input.on_change = _validate_delete
        confirm_btn.on_click = _execute_purge

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#0F172A",
            title=ft.Row([ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED_400), ft.Text("Delete Account", color=ft.colors.WHITE)]),
            content=ft.Column(
                controls=[
                    ft.Text("This action will permanently erase your workouts, streak, and local history.", size=13, color=ft.colors.GREY_300),
                    delete_input,
                ],
                tight=True,
                spacing=10,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda ce: [setattr(dialog, "open", False), page.update()]),
                confirm_btn,
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # --------------------------------------------------------------------------
    # Profile Display Header
    # --------------------------------------------------------------------------
    banner_container = ft.Container(
        content=ft.Stack(
            controls=[
                # Top ambient gradient banner
                ft.Container(
                    height=100,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=["#0EA5E9", "#1E1B4B"],
                    ),
                    border_radius=ft.border_radius.only(top_left=16, top_right=16),
                ),
                # Avatar overlapping banner
                ft.Container(
                    content=ft.CircleAvatar(
                        radius=36,
                        bgcolor="#0F172A",
                        content=ft.Icon(ft.icons.PERSON, size=40, color=ft.colors.LIGHT_BLUE_400),
                    ),
                    alignment=ft.alignment.bottom_center,
                    padding=ft.padding.only(top=50),
                ),
            ],
            alignment=ft.alignment.center,
        ),
        height=140,
    )

    identity_info = ft.Column(
        controls=[
            ft.Text(full_name, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Row(
                controls=[
                    ft.Text(f"@{username}", size=12, color=ft.colors.GREY_400),
                    ft.Text("•", color=ft.colors.GREY_600),
                    ft.Container(
                        content=ft.Text(equipped_title, size=11, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER_300),
                        bgcolor="#78350F44",
                        border=ft.border.all(1, ft.colors.AMBER_600),
                        border_radius=6,
                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=6,
            ),
            ft.Row(
                controls=[
                    ft.Row([ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT, color=ft.colors.ORANGE_400, size=16), ft.Text(f"{current_streak} Days Streak", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)]),
                    ft.Text("•", color=ft.colors.GREY_600),
                    ft.Row([ft.Icon(ft.icons.SHIELD_ROUNDED, color=ft.colors.AMBER_400, size=16), ft.Text("Bronze Tier", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)]),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=4,
    )

    # --------------------------------------------------------------------------
    # Navigation Shelf
    # --------------------------------------------------------------------------
    def _make_shelf_tile(icon, title: str, on_tap):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row([ft.Icon(icon, size=18, color=ft.colors.LIGHT_BLUE_400), ft.Text(title, size=13, weight=ft.FontWeight.W_500, color=ft.colors.WHITE)], spacing=10),
                    ft.Icon(ft.icons.ARROW_FORWARD_IOS_ROUNDED, size=14, color=ft.colors.GREY_500),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#0F172A",
            border=ft.border.all(1, "#1E293B"),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=14, vertical=12),
            margin=ft.margin.only(bottom=6),
            on_click=on_tap,
        )

    nav_shelf = ft.Column(
        controls=[
            _make_shelf_tile(ft.icons.CALENDAR_MONTH_ROUNDED, "Workouts Plan Update", lambda e: page.go("/settings/plan_update")),
            _make_shelf_tile(ft.icons.WORKSPACE_PREMIUM_ROUNDED, "{Badges, Achievements, Title}", lambda e: page.go("/profile/badges")),
            _make_shelf_tile(ft.icons.SETTINGS_OUTLINED, "Settings Console", lambda e: page.go("/settings")),
            _make_shelf_tile(ft.icons.SUPPORT_AGENT_ROUNDED, "Customer Support & Feedback", lambda e: page.go("/support")),
            _make_shelf_tile(ft.icons.GAVEL_ROUNDED, "Disclaimer & Warning", lambda e: page.go("/settings/disclaimer")),
        ],
        spacing=2,
    )

    # --------------------------------------------------------------------------
    # Personal Biometrics Section
    # --------------------------------------------------------------------------
    biometrics_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Personal Info & Biometrics", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ft.Row([weight_field, target_weight_field], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([height_field, age_field], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([sex_dropdown, ft.ElevatedButton("Save Metrics", bgcolor=ft.colors.LIGHT_BLUE_600, color=ft.colors.WHITE, on_click=_save_biometrics)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                feedback_text,
            ],
            spacing=10,
        ),
        bgcolor="#0F172A",
        border=ft.border.all(1, "#1E293B"),
        border_radius=14,
        padding=ft.padding.all(14),
        margin=ft.margin.symmetric(vertical=8),
    )

    # Danger Zone
    danger_zone = ft.Container(
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Delete Account (Data Purge)",
                    icon=ft.icons.DELETE_FOREVER_ROUNDED,
                    style=ft.ButtonStyle(color=ft.colors.RED_400),
                    on_click=_show_delete_account_modal,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=10),
    )

    version_tag = ft.Text(
        value="Version 1.1.1 alpha • Solo Developer Edition",
        size=11,
        color=ft.colors.GREY_600,
        text_align=ft.TextAlign.CENTER,
    )

    scrollable_column = ft.Column(
        controls=[
            banner_container,
            identity_info,
            ft.Divider(color="#1E293B", height=20),
            nav_shelf,
            biometrics_section,
            danger_zone,
            version_tag,
        ],
        spacing=8,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return create_responsive_view(
        route="/profile",
        controls=[scrollable_column],
        page=page,
        scroll=True,
        bg_color="#020617",
    )
