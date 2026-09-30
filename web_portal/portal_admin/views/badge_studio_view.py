"""
badge_studio_view.py - Aesthetic Physique Admin Badge Studio & Constraint Engine
Architectural Role: Achievement creation module providing vector/artwork asset
uploading, metadata configuration, programmatic requirement constraint rules
(streaks, failure volume, hydration/sleep), and real-time metallic preview rendering.
"""

import flet as ft
from typing import Callable, Optional, Dict, Any
from web_portal.portal_admin.admin_config import (
    BadgeTier,
    ConstraintType,
    TIER_STYLING,
)


def create_badge_studio_view(
    on_create_badge: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> ft.Control:
    """
    Constructs the Badge & Achievement Studio view for desktop/web administrative console.
    """

    # --- Form Inputs ---
    badge_id_field = ft.TextField(
        label="Badge Unique ID (Slug)",
        value="BADGE_IRON_WILL",
        hint_text="e.g. BADGE_CENTURION_STREAK",
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    badge_name_field = ft.TextField(
        label="Badge Name",
        value="Iron Will",
        hint_text="e.g. Centurion Streak",
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    associated_title_field = ft.TextField(
        label="Associated Vanity Title (Granted upon unlocking)",
        value="The Unyielding",
        hint_text="e.g. The Iron Centurion",
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    badge_desc_field = ft.TextField(
        label="Achievement Description & Criteria Lore",
        value="Complete 30 consecutive training days without missing an active session.",
        multiline=True,
        min_lines=2,
        max_lines=3,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        expand=True,
    )

    tier_dropdown = ft.Dropdown(
        label="Achievement Tier",
        value=BadgeTier.GOLD.value,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        options=[
            ft.dropdown.Option(BadgeTier.BRONZE.value, text="Bronze Tier"),
            ft.dropdown.Option(BadgeTier.SILVER.value, text="Silver Tier"),
            ft.dropdown.Option(BadgeTier.GOLD.value, text="Gold Tier"),
            ft.dropdown.Option(BadgeTier.PLATINUM.value, text="Platinum Tier"),
        ],
        text_size=13,
        expand=True,
    )

    glyph_dropdown = ft.Dropdown(
        label="Badge Vector Glyph / Icon",
        value="fitness_center_rounded",
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        options=[
            ft.dropdown.Option("fitness_center_rounded", text="Dumbbell / Iron"),
            ft.dropdown.Option("local_fire_department_rounded", text="Fire / Failure Intensity"),
            ft.dropdown.Option("water_drop_rounded", text="Water Drop / Hydration"),
            ft.dropdown.Option("bedtime_rounded", text="Moon / Recovery & Sleep"),
            ft.dropdown.Option("military_tech_rounded", text="Medal / Excellence"),
            ft.dropdown.Option("shield_rounded", text="Shield / Consistency"),
            ft.dropdown.Option("bolt_rounded", text="Lightning / Power"),
        ],
        text_size=13,
        expand=True,
    )

    # --- Programmatic Constraint Rules ---
    constraint_type_dropdown = ft.Dropdown(
        label="Constraint Type (Unlock Trigger)",
        value=ConstraintType.STREAK_DAYS.value,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        options=[
            ft.dropdown.Option(ConstraintType.STREAK_DAYS.value, text="Workout Streak (Days)"),
            ft.dropdown.Option(ConstraintType.TOTAL_FAILURE_REPS.value, text="Total Reps to Failure"),
            ft.dropdown.Option(ConstraintType.HYDRATION_STREAK.value, text="Hydration Target Streak (Days)"),
            ft.dropdown.Option(ConstraintType.SLEEP_CONSISTENCY.value, text="Sleep Consistency Streak (Days)"),
            ft.dropdown.Option(ConstraintType.MANUAL_AWARD.value, text="Manual Coach / Admin Award Only"),
        ],
        text_size=13,
        expand=True,
    )

    constraint_threshold_field = ft.TextField(
        label="Constraint Threshold Metric",
        value="30",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="e.g. 30 (days) or 250 (reps)",
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    custom_artwork_url_field = ft.TextField(
        label="Custom Vector / PNG Artwork URL (Optional override)",
        value="",
        hint_text="https://cdn.aestheticphysique.com/badges/custom-iron-will.svg",
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        expand=True,
    )

    status_message = ft.Text("", size=12, color="#10B981", weight=ft.FontWeight.W_600, visible=False)

    # --- Real-Time Live Preview Cards ---
    preview_name = ft.Text(badge_name_field.value, size=16, weight=ft.FontWeight.W_800, color="#F0F6FC")
    preview_title = ft.Text(f"Title: {associated_title_field.value}", size=11, color="#FFD700", weight=ft.FontWeight.W_700)
    preview_lore = ft.Text(badge_desc_field.value, size=11, color="#8B949E", text_align=ft.TextAlign.CENTER)
    preview_criteria = ft.Text("Requires 30 consecutive workout streak days", size=10, color="#00F2FE", weight=ft.FontWeight.W_600)
    preview_glyph_icon = ft.Icon(ft.icons.FITNESS_CENTER_ROUNDED, size=36, color="#FFD700")

    unlocked_preview_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("UNLOCKED ATHLETE PREVIEW", size=9, weight=ft.FontWeight.BOLD, color="#10B981"),
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    bgcolor="#10B98122",
                    border_radius=6,
                ),
                ft.Container(
                    content=preview_glyph_icon,
                    width=72,
                    height=72,
                    border_radius=36,
                    border=ft.border.all(2, "#F4D03F"),
                    bgcolor="#2A2300",
                    alignment=ft.alignment.center,
                ),
                preview_name,
                preview_title,
                preview_lore,
                ft.Container(
                    content=preview_criteria,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    bgcolor="#0D1117",
                    border_radius=8,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        width=280,
        padding=20,
        border_radius=16,
        bgcolor="#161B22",
        border=ft.border.all(1.5, "#FFD700"),
        alignment=ft.alignment.center,
    )

    locked_preview_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("LOCKED / GRAYSCALE PREVIEW", size=9, weight=ft.FontWeight.BOLD, color="#8B949E"),
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    bgcolor="#21262D",
                    border_radius=6,
                ),
                ft.Stack(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.icons.FITNESS_CENTER_ROUNDED, size=36, color="#484F58"),
                            width=72,
                            height=72,
                            border_radius=36,
                            border=ft.border.all(2, "#30363D"),
                            bgcolor="#161B22",
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.Icon(ft.icons.LOCK_ROUNDED, size=18, color="#8B949E"),
                            alignment=ft.alignment.bottom_right,
                            width=72,
                            height=72,
                            padding=ft.padding.only(right=4, bottom=4),
                        ),
                    ],
                    width=72,
                    height=72,
                ),
                ft.Text("Locked Trophy", size=15, weight=ft.FontWeight.W_800, color="#8B949E"),
                ft.Text("Title: Hidden", size=11, color="#484F58", weight=ft.FontWeight.W_700),
                ft.Text("Complete requirements to reveal vanity badge & title.", size=11, color="#484F58", text_align=ft.TextAlign.CENTER),
                ft.Container(
                    content=ft.Text("Target: 30 Workout Streak Days", size=10, color="#8B949E", weight=ft.FontWeight.W_600),
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    bgcolor="#0D1117",
                    border_radius=8,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
        width=280,
        padding=20,
        border_radius=16,
        bgcolor="#12161C",
        border=ft.border.all(1.5, "#30363D"),
        alignment=ft.alignment.center,
    )

    def update_preview(e=None):
        tier_key = tier_dropdown.value or BadgeTier.GOLD.value
        tier_style = TIER_STYLING.get(tier_key, TIER_STYLING[BadgeTier.GOLD.value])

        preview_name.value = badge_name_field.value or "Untitled Badge"
        preview_title.value = f"Title: {associated_title_field.value or 'None'}"
        preview_title.color = tier_style["primary_color"]
        preview_lore.value = badge_desc_field.value or "No lore specified."

        # Map selected icon string to Flet icon
        icon_map = {
            "fitness_center_rounded": ft.icons.FITNESS_CENTER_ROUNDED,
            "local_fire_department_rounded": ft.icons.LOCAL_FIRE_DEPARTMENT_ROUNDED,
            "water_drop_rounded": ft.icons.WATER_DROP_ROUNDED,
            "bedtime_rounded": ft.icons.BEDTIME_ROUNDED,
            "military_tech_rounded": ft.icons.MILITARY_TECH_ROUNDED,
            "shield_rounded": ft.icons.SHIELD_ROUNDED,
            "bolt_rounded": ft.icons.BOLT_ROUNDED,
        }
        chosen_icon = icon_map.get(glyph_dropdown.value, ft.icons.FITNESS_CENTER_ROUNDED)
        preview_glyph_icon.name = chosen_icon
        preview_glyph_icon.color = tier_style["primary_color"]

        # Update styling border and backdrop of preview card
        unlocked_preview_card.border = ft.border.all(1.5, tier_style["border_color"])

        c_type = constraint_type_dropdown.value or ConstraintType.STREAK_DAYS.value
        c_val = constraint_threshold_field.value or "0"
        if c_type == ConstraintType.STREAK_DAYS.value:
            preview_criteria.value = f"Requires {c_val} consecutive workout streak days"
        elif c_type == ConstraintType.TOTAL_FAILURE_REPS.value:
            preview_criteria.value = f"Requires {c_val} lifetime sets taken to failure"
        elif c_type == ConstraintType.HYDRATION_STREAK.value:
            preview_criteria.value = f"Requires {c_val} consecutive days hitting 3000ml water"
        elif c_type == ConstraintType.SLEEP_CONSISTENCY.value:
            preview_criteria.value = f"Requires {c_val} consecutive days optimal sleep"
        else:
            preview_criteria.value = "Direct Admin / Coach Designation Only"

        if e and hasattr(e, "control") and e.control and e.control.page:
            e.control.page.update()

    # Bind on_change callbacks
    badge_name_field.on_change = update_preview
    associated_title_field.on_change = update_preview
    badge_desc_field.on_change = update_preview
    tier_dropdown.on_change = update_preview
    glyph_dropdown.on_change = update_preview
    constraint_type_dropdown.on_change = update_preview
    constraint_threshold_field.on_change = update_preview

    def handle_publish(e):
        name = badge_name_field.value.strip() if badge_name_field.value else ""
        slug = badge_id_field.value.strip() if badge_id_field.value else ""
        if not name or not slug:
            status_message.value = "Badge ID and Badge Name are mandatory."
            status_message.color = "#EF4444"
            status_message.visible = True
            e.control.page.update()
            return

        payload = {
            "badge_id": slug,
            "name": name,
            "tier": tier_dropdown.value or BadgeTier.GOLD.value,
            "title": associated_title_field.value.strip() if associated_title_field.value else "",
            "description": badge_desc_field.value.strip() if badge_desc_field.value else "",
            "glyph": glyph_dropdown.value or "fitness_center_rounded",
            "constraint_type": constraint_type_dropdown.value or ConstraintType.STREAK_DAYS.value,
            "constraint_threshold": int(constraint_threshold_field.value or "0"),
            "artwork_url": custom_artwork_url_field.value.strip() if custom_artwork_url_field.value else None,
        }

        status_message.value = f"Achievement '{name}' published successfully to ecosystem catalog."
        status_message.color = "#10B981"
        status_message.visible = True
        e.control.page.update()

        if on_create_badge:
            on_create_badge(payload)

    # Layout structure
    header = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.WORKSPACE_PREMIUM_ROUNDED, color="#FFD700", size=26),
                            ft.Text(
                                "NEW BADGES & ACHIEVEMENTS STUDIO",
                                size=20,
                                weight=ft.FontWeight.W_900,
                                color="#F0F6FC",
                                style=ft.TextStyle(letter_spacing=1.5),
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Text(
                        "Design new accolades, define mathematical unlock triggers, and publish to athlete trophy cases.",
                        size=13,
                        color="#8B949E",
                    ),
                ],
                spacing=4,
            ),
        ]
    )

    form_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("1. METADATA DEFINITIONS", size=11, weight=ft.FontWeight.BOLD, color="#00F2FE", style=ft.TextStyle(letter_spacing=1.0)),
                ft.Row(controls=[badge_id_field, badge_name_field], spacing=12),
                ft.Row(controls=[associated_title_field, tier_dropdown], spacing=12),
                badge_desc_field,
                ft.Divider(height=1, color="#21262D"),
                ft.Text("2. ARTWORK & GLYPH ASSETS", size=11, weight=ft.FontWeight.BOLD, color="#00F2FE", style=ft.TextStyle(letter_spacing=1.0)),
                ft.Row(controls=[glyph_dropdown, custom_artwork_url_field], spacing=12),
                ft.Divider(height=1, color="#21262D"),
                ft.Text("3. PROGRAMMATIC CONSTRAINT RULES", size=11, weight=ft.FontWeight.BOLD, color="#00F2FE", style=ft.TextStyle(letter_spacing=1.0)),
                ft.Row(controls=[constraint_type_dropdown, constraint_threshold_field], spacing=12),
                status_message,
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Publish Achievement to Ecosystem",
                        icon=ft.icons.PUBLISH_ROUNDED,
                        style=ft.ButtonStyle(
                            color="#0D1117",
                            bgcolor="#FFD700",
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=handle_publish,
                    ),
                    padding=ft.padding.only(top=8),
                ),
            ],
            spacing=12,
        ),
        padding=20,
        border_radius=12,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
        expand=3,
    )

    preview_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("LIVE TROPHY SHELF PREVIEW", size=11, weight=ft.FontWeight.BOLD, color="#8B949E", style=ft.TextStyle(letter_spacing=1.0)),
                unlocked_preview_card,
                locked_preview_card,
            ],
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
        border_radius=12,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
        expand=2,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                header,
                ft.Row(
                    controls=[form_panel, preview_panel],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    spacing=20,
                ),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=24,
        expand=True,
    )
