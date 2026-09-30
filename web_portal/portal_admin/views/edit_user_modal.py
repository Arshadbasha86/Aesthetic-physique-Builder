"""
edit_user_modal.py - Aesthetic Physique Admin Console Athlete Record Editor
Architectural Role: Security-audited administrative dialog allowing authorized
operators to adjust athlete biometrics, override vanity tiers/streaks, modify account
states (Active/Suspended), and record mandatory administrative audit justifications.
"""

import flet as ft
from typing import Dict, Any, Callable, Optional


def show_edit_user_modal(
    page: ft.Page,
    user_data: Dict[str, Any],
    on_save: Optional[Callable[[Dict[str, Any], str], None]] = None,
) -> None:
    """
    Displays the Athlete Record Modification Dialog with mandatory audit justification.
    """
    ath_id = user_data.get("id", "ATH-000")
    ath_name = user_data.get("name", "Athlete")
    ath_email = user_data.get("email", "")
    ath_tier = user_data.get("tier", "Bronze")
    ath_streak = user_data.get("streak", 0)
    ath_failure = user_data.get("failure_reps", 0)
    ath_status = user_data.get("status", "ACTIVE")
    ath_weight = user_data.get("weight", "75.0")
    ath_height = user_data.get("height", "178.0")

    # Form input fields
    name_field = ft.TextField(
        label="Athlete Full Name",
        value=ath_name,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    email_field = ft.TextField(
        label="Email Address",
        value=ath_email,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    tier_dropdown = ft.Dropdown(
        label="Vanity Tier",
        value=ath_tier,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        options=[
            ft.dropdown.Option("Bronze"),
            ft.dropdown.Option("Silver"),
            ft.dropdown.Option("Gold"),
            ft.dropdown.Option("Platinum"),
        ],
        text_size=13,
        expand=True,
    )

    status_dropdown = ft.Dropdown(
        label="Account State",
        value=ath_status,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        options=[
            ft.dropdown.Option("ACTIVE"),
            ft.dropdown.Option("SUSPENDED"),
            ft.dropdown.Option("BANNED"),
        ],
        text_size=13,
        expand=True,
    )

    weight_field = ft.TextField(
        label="Weight (kg)",
        value=str(ath_weight),
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    height_field = ft.TextField(
        label="Height (cm)",
        value=str(ath_height),
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    streak_field = ft.TextField(
        label="Active Streak (Days)",
        value=str(ath_streak),
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    failure_field = ft.TextField(
        label="Lifetime Failure Reps",
        value=str(ath_failure),
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    # Mandatory administrative audit justification input
    audit_reason_field = ft.TextField(
        label="Mandatory Audit Justification / Reason *",
        hint_text="e.g. Account reinstated per support ticket #402, corrected streak sync error.",
        multiline=True,
        min_lines=2,
        max_lines=3,
        bgcolor="#0D1117",
        border_color="#EF444466",
        focused_border_color="#EF4444",
        text_size=12,
        expand=True,
    )

    error_banner = ft.Text(
        "",
        color="#EF4444",
        size=12,
        weight=ft.FontWeight.W_600,
        visible=False,
    )

    modal_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            controls=[
                ft.Icon(ft.icons.MANAGE_ACCOUNTS_ROUNDED, color="#00F2FE", size=24),
                ft.Text(
                    f"MODIFY ATHLETE: {ath_id}",
                    size=16,
                    weight=ft.FontWeight.W_800,
                    color="#F0F6FC",
                    style=ft.TextStyle(letter_spacing=1.0),
                ),
            ],
            spacing=8,
        ),
        content=ft.Container(
            width=580,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "All manual modifications to athlete biometrics or statuses are permanently written to the administrative audit ledger.",
                        size=12,
                        color="#8B949E",
                    ),
                    ft.Divider(height=1, color="#21262D"),
                    ft.Row(controls=[name_field, email_field], spacing=12),
                    ft.Row(controls=[tier_dropdown, status_dropdown], spacing=12),
                    ft.Row(controls=[weight_field, height_field], spacing=12),
                    ft.Row(controls=[streak_field, failure_field], spacing=12),
                    ft.Divider(height=1, color="#21262D"),
                    ft.Text(
                        "ADMINISTRATIVE AUDIT LOG REQUIREMENT",
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color="#EF4444",
                        style=ft.TextStyle(letter_spacing=1.0),
                    ),
                    audit_reason_field,
                    error_banner,
                ],
                spacing=12,
                tight=True,
            ),
            bgcolor="#161B22",
            border_radius=12,
            padding=ft.padding.symmetric(vertical=8, horizontal=4),
        ),
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor="#161B22",
    )

    def close_modal(e):
        modal_dialog.open = False
        page.update()

    def handle_save(e):
        reason = audit_reason_field.value.strip() if audit_reason_field.value else ""
        if not reason:
            error_banner.value = "An administrative audit justification is mandatory before saving."
            error_banner.visible = True
            page.update()
            return

        try:
            streak_val = int(streak_field.value or "0")
            failure_val = int(failure_field.value or "0")
            weight_val = float(weight_field.value or "0.0")
            height_val = float(height_field.value or "0.0")
        except ValueError:
            error_banner.value = "Streak, Failure Reps, Weight, and Height must be valid numeric values."
            error_banner.visible = True
            page.update()
            return

        updated_record = {
            "id": ath_id,
            "name": name_field.value.strip() if name_field.value else ath_name,
            "email": email_field.value.strip() if email_field.value else ath_email,
            "tier": tier_dropdown.value or ath_tier,
            "status": status_dropdown.value or ath_status,
            "streak": streak_val,
            "failure_reps": failure_val,
            "weight": weight_val,
            "height": height_val,
        }

        modal_dialog.open = False
        page.update()

        if on_save:
            on_save(updated_record, reason)

    modal_dialog.actions = [
        ft.TextButton(
            text="Cancel",
            style=ft.ButtonStyle(color="#8B949E"),
            on_click=close_modal,
        ),
        ft.ElevatedButton(
            text="Save Record & Log Audit",
            icon=ft.icons.CHECK_CIRCLE_ROUNDED,
            style=ft.ButtonStyle(
                color="#0D1117",
                bgcolor="#00F2FE",
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
            on_click=handle_save,
        ),
    ]

    page.dialog = modal_dialog
    modal_dialog.open = True
    page.update()
