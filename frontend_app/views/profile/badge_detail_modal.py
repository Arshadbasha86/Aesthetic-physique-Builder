"""
Aesthetic Physique Builder - Interactive Badge Detail Modal
Relative Path: frontend_app/views/profile/badge_detail_modal.py
Architectural Role: Focused inspection modal triggered from the Badge Showcase grid.
Exposes unlock criteria, tier aura, unlock timestamps, and vanity title equipment controls.
"""

import flet as ft
from typing import Dict, Any, Callable, Optional

from database.db_manager import db
from config.default_config import TIER_COLORS


def open_badge_detail_modal(
    page: ft.Page,
    badge_data: Dict[str, Any],
    on_title_equipped: Optional[Callable[[], None]] = None
):
    """
    Displays the Badge Inspection Dialog / Bottom Sheet.
    """
    badge_name = badge_data.get("badge_name", "Badge")
    tier = badge_data.get("tier", "bronze").lower()
    tier_color = TIER_COLORS.get(tier, "#CD7F32")
    associated_title = badge_data.get("associated_title", "")
    criteria = badge_data.get("assignment_criteria", "Complete workout requirements to unlock.")
    is_unlocked = bool(badge_data.get("is_unlocked", 0))
    awarded_at = badge_data.get("awarded_at", "Recently")

    profile = db.get_user_profile()
    is_title_currently_equipped = (profile.get("equipped_title") == associated_title and is_unlocked)

    dialog = ft.AlertDialog(
        modal=True,
        bgcolor="#0F172A",
        surface_tint_color=ft.colors.TRANSPARENT,
        shape=ft.RoundedRectangleBorder(radius=20),
    )

    def _equip_title_action(e):
        if is_unlocked and associated_title:
            if is_title_currently_equipped:
                db.equip_title("Novice Trainee")
            else:
                db.equip_title(associated_title)
        dialog.open = False
        page.update()
        if on_title_equipped:
            on_title_equipped()

    def _close_modal(e):
        dialog.open = False
        page.update()

    # Badge Artwork Container
    artwork_emblem = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Icon(
                    name=ft.icons.WORKSPACE_PREMIUM_ROUNDED,
                    size=64,
                    color=tier_color if is_unlocked else ft.colors.GREY_600,
                ),
                ft.Container(
                    content=ft.Icon(ft.icons.LOCK_ROUNDED, size=24, color=ft.colors.WHITE70),
                    alignment=ft.alignment.center,
                    visible=not is_unlocked,
                ),
            ],
            alignment=ft.alignment.center,
        ),
        width=96,
        height=96,
        bgcolor="#0B132B" if is_unlocked else "#020617",
        border=ft.border.all(2, tier_color if is_unlocked else "#334155"),
        border_radius=48,
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color=f"{tier_color}44",
        ) if is_unlocked else None,
    )

    # Criteria or Unlock Info Box
    if is_unlocked:
        status_box = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.CHECK_CIRCLE_ROUNDED, color="#10B981", size=16),
                            ft.Text("Unlocked Achievement", size=12, weight=ft.FontWeight.BOLD, color="#10B981"),
                        ],
                        spacing=6,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(f"Unlocked on: {awarded_at}", size=11, color=ft.colors.GREY_400, text_align=ft.TextAlign.CENTER),
                ],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#020617",
            border=ft.border.all(1, "#10B98133"),
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
        )
    else:
        status_box = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Unlock Requirement", size=11, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_400),
                    ft.Text(criteria, size=12, color=ft.colors.GREY_300, text_align=ft.TextAlign.CENTER),
                ],
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#020617",
            border=ft.border.all(1, "#334155"),
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
        )

    # Equip Title Button
    if is_unlocked and associated_title:
        equip_button = ft.ElevatedButton(
            text="Unequip Title" if is_title_currently_equipped else f"Equip Title: '{associated_title}'",
            icon=ft.icons.CHECK if is_title_currently_equipped else ft.icons.STAR_ROUNDED,
            bgcolor=ft.colors.AMBER_600 if not is_title_currently_equipped else "#1E293B",
            color=ft.colors.WHITE,
            width=280,
            height=46,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
            on_click=_equip_title_action,
        )
    else:
        equip_button = ft.ElevatedButton(
            text="Locked Achievement",
            disabled=True,
            width=280,
            height=46,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        )

    modal_content = ft.Container(
        width=300,
        content=ft.Column(
            controls=[
                artwork_emblem,
                ft.Text(badge_name, size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER),
                ft.Container(
                    content=ft.Text(tier.upper(), size=10, weight=ft.FontWeight.BOLD, color=tier_color),
                    bgcolor="#020617",
                    border=ft.border.all(1, tier_color),
                    border_radius=8,
                    padding=ft.padding.symmetric(horizontal=10, vertical=3),
                ),
                status_box,
                equip_button,
                ft.TextButton("Close", on_click=_close_modal, style=ft.ButtonStyle(color=ft.colors.GREY_400)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
            tight=True,
        ),
        padding=ft.padding.all(8),
    )

    dialog.content = modal_content
    if dialog not in page.overlay:
        page.overlay.append(dialog)
    dialog.open = True
    page.update()
