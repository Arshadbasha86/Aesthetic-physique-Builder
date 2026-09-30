"""
user_portal_view.py - Aesthetic Physique Athlete Web Companion Portal
Architectural Role: Comprehensive web companion interface featuring athlete profile banner,
"Set Display" vanity title customizer, badges & achievements shelf (color vs. grayscale),
interactive badge detail modal, daily recovery ledger, weekly arena leaderboard, and APK download tile.
"""

import flet as ft
from typing import Dict, Any, List, Optional
from web_portal.portal_admin.admin_config import BadgeTier, TIER_STYLING
from web_portal.portal_user.views.weekly_leaderboard_widget import create_weekly_leaderboard_widget


def create_user_portal_view(
    current_athlete: Optional[Dict[str, Any]] = None,
) -> ft.Control:
    """
    Constructs the Athlete Web Companion Portal view.
    """

    athlete = current_athlete or {
        "id": "ATH-004",
        "name": "Chloe Bennett",
        "email": "chloe.b@gmail.com",
        "tier": "Silver",
        "active_title": "Pure Flow",
        "streak": 14,
        "failure_reps": 38,
        "weight": 62.5,
        "height": 168.0,
        "water_ml": 3200,
        "water_target": 3500,
        "sleep_hours": 7.8,
        "sleep_quality": "Excellent",
        "protein_g": 135,
        "protein_target": 145,
    }

    # Athlete's achievement shelf repository
    achievements = [
        {
            "id": "BADGE_HYDRATION_SENTINEL",
            "name": "Hydration Sentinel",
            "tier": "Silver",
            "title": "Pure Flow",
            "unlocked": True,
            "unlocked_date": "2026-09-15",
            "glyph": ft.icons.WATER_DROP_ROUNDED,
            "criteria": "Maintained 3,500 ml daily water target for 14 consecutive days.",
        },
        {
            "id": "BADGE_EARLY_BIRD",
            "name": "Dawn Vanguard",
            "tier": "Bronze",
            "title": "The Early Riser",
            "unlocked": True,
            "unlocked_date": "2026-09-18",
            "glyph": ft.icons.BEDTIME_ROUNDED,
            "criteria": "Completed 5 consecutive morning routines before 08:00 AM.",
        },
        {
            "id": "BADGE_IRON_WILL",
            "name": "Iron Will",
            "tier": "Gold",
            "title": "The Unyielding",
            "unlocked": False,
            "unlocked_date": None,
            "glyph": ft.icons.FITNESS_CENTER_ROUNDED,
            "criteria": "Assigned upon reaching a 30-day continuous workout streak.",
        },
        {
            "id": "BADGE_TITAN_FAILURE",
            "name": "Titan of Failure",
            "tier": "Platinum",
            "title": "Apex Engine",
            "unlocked": False,
            "unlocked_date": None,
            "glyph": ft.icons.LOCAL_FIRE_DEPARTMENT_ROUNDED,
            "criteria": "Assigned upon logging 100 sets taken to total muscular failure.",
        },
    ]

    active_title_text = ft.Text(
        f"Title: {athlete['active_title']}",
        size=12,
        color="#00F2FE",
        weight=ft.FontWeight.W_700,
        style=ft.TextStyle(letter_spacing=0.5),
    )

    # 1. Profile Banner & Header
    def show_title_customizer(e):
        page: ft.Page = e.control.page

        # Only unlocked badges provide titles
        unlocked_titles = [a["title"] for a in achievements if a["unlocked"] and a["title"]]

        title_radio_group = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(value=t, label=f"Equip Title: '{t}'", fill_color="#00F2FE")
                    for t in unlocked_titles
                ],
                spacing=8,
            ),
            value=athlete["active_title"],
        )

        def save_equipped_title(ev):
            chosen = title_radio_group.value
            athlete["active_title"] = chosen
            active_title_text.value = f"Title: {chosen}"
            modal_dlg.open = False
            page.update()

        modal_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(ft.icons.BADGE_ROUNDED, color="#00F2FE", size=22),
                    ft.Text("SET DISPLAY: VANITY TITLE", size=15, weight=ft.FontWeight.W_800, color="#F0F6FC"),
                ],
                spacing=8,
            ),
            content=ft.Container(
                width=420,
                content=ft.Column(
                    controls=[
                        ft.Text("Select which earned honorific appears on your public arena profile:", size=12, color="#8B949E"),
                        ft.Divider(height=1, color="#21262D"),
                        title_radio_group,
                    ],
                    spacing=12,
                    tight=True,
                ),
                bgcolor="#161B22",
                border_radius=12,
            ),
            actions=[
                ft.TextButton("Cancel", style=ft.ButtonStyle(color="#8B949E"), on_click=lambda _: setattr(modal_dlg, "open", False) or page.update()),
                ft.ElevatedButton(
                    "Equip Title",
                    style=ft.ButtonStyle(color="#0D1117", bgcolor="#00F2FE"),
                    on_click=save_equipped_title,
                ),
            ],
            bgcolor="#161B22",
        )

        page.dialog = modal_dlg
        modal_dlg.open = True
        page.update()

    profile_banner = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.icons.PERSON_ROUNDED, size=38, color="#00F2FE"),
                            width=68,
                            height=68,
                            border_radius=34,
                            bgcolor="#00F2FE15",
                            border=ft.border.all(2, "#00F2FE"),
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(athlete["name"], size=20, weight=ft.FontWeight.W_900, color="#F0F6FC"),
                                        ft.Container(
                                            content=ft.Text(f"{athlete['tier'].upper()} TIER", size=10, weight=ft.FontWeight.BOLD, color="#C0C0C0"),
                                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                            border_radius=8,
                                            border=ft.border.all(1, "#C0C0C066"),
                                            bgcolor="#C0C0C020",
                                        ),
                                    ],
                                    spacing=8,
                                ),
                                active_title_text,
                                ft.Text(f"{athlete['id']} • {athlete['email']}", size=11, color="#8B949E"),
                            ],
                            spacing=3,
                        ),
                    ],
                    spacing=16,
                ),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Set Display Title",
                            icon=ft.icons.STYLE_ROUNDED,
                            style=ft.ButtonStyle(
                                color="#0D1117",
                                bgcolor="#00F2FE",
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=show_title_customizer,
                        ),
                        ft.OutlinedButton(
                            text="Official Documentation",
                            icon=ft.icons.MENU_BOOK_ROUNDED,
                            style=ft.ButtonStyle(
                                color="#F0F6FC",
                                side=ft.BorderSide(1, "#30363D"),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=lambda e: e.control.page.launch_url("https://docs.aestheticphysique.com"),
                        ),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=20,
        border_radius=16,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
    )

    # 2. Daily Recovery Ledger Cards
    def make_stat_chip(label: str, value: str, sub: str, icon: str, color: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(label, size=11, color="#8B949E", weight=ft.FontWeight.W_700),
                            ft.Icon(icon, color=color, size=18),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(value, size=20, weight=ft.FontWeight.W_800, color="#F0F6FC"),
                    ft.Text(sub, size=11, color=color, weight=ft.FontWeight.W_600),
                ],
                spacing=4,
            ),
            padding=14,
            border_radius=12,
            bgcolor="#161B22",
            border=ft.border.all(1, "#21262D"),
            expand=True,
        )

    recovery_row = ft.Row(
        controls=[
            make_stat_chip("WATER HYDRATION", f"{athlete['water_ml']} ml", f"Goal: {athlete['water_target']} ml (91%)", ft.icons.WATER_DROP_ROUNDED, "#00F2FE"),
            make_stat_chip("SLEEP RECOVERY", f"{athlete['sleep_hours']} Hours", f"{athlete['sleep_quality']} Quality", ft.icons.BEDTIME_ROUNDED, "#A78BFA"),
            make_stat_chip("PROTEIN CONSUMPTION", f"{athlete['protein_g']} g", f"Target: {athlete['protein_target']} g (93%)", ft.icons.EGG_ALT_ROUNDED, "#F59E0B"),
            make_stat_chip("ACTIVE STREAK", f"{athlete['streak']} Days", "Flawless Wall-Clock Adherence", ft.icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, "#EF4444"),
        ],
        spacing=14,
    )

    # 3. Badges & Achievements Shelf (Color Unlocked vs Grayscale Locked)
    def open_badge_detail(ach: Dict[str, Any], e):
        page: ft.Page = e.control.page
        is_unlocked = ach["unlocked"]
        tier_style = TIER_STYLING.get(ach["tier"].upper(), {"primary_color": "#8B949E", "border_color": "#30363D"})

        modal = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(ach["glyph"], color=tier_style["primary_color"] if is_unlocked else "#8B949E", size=26),
                    ft.Text(ach["name"], size=16, weight=ft.FontWeight.W_800, color="#F0F6FC"),
                ],
                spacing=8,
            ),
            content=ft.Container(
                width=440,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text(f"{ach['tier'].upper()} TIER", size=10, weight=ft.FontWeight.BOLD, color=tier_style["primary_color"]),
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                    border_radius=8,
                                    border=ft.border.all(1, f"{tier_style['primary_color']}66"),
                                    bgcolor=f"{tier_style['primary_color']}15",
                                ),
                                ft.Text(
                                    f"Unlocked: {ach['unlocked_date']}" if is_unlocked else "LOCKED ACCOLADE",
                                    size=11,
                                    color="#10B981" if is_unlocked else "#EF4444",
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Divider(height=1, color="#21262D"),
                        ft.Text("ACCOLADE CRITERIA & LORE", size=10, weight=ft.FontWeight.BOLD, color="#8B949E"),
                        ft.Text(ach["criteria"], size=12, color="#C9D1D9"),
                        ft.Divider(height=1, color="#21262D"),
                        ft.Text(f"Granted Vanity Title: '{ach['title']}'", size=12, color="#00F2FE", weight=ft.FontWeight.W_700),
                    ],
                    spacing=10,
                    tight=True,
                ),
                bgcolor="#161B22",
                border_radius=12,
            ),
            actions=[
                ft.TextButton("Close", style=ft.ButtonStyle(color="#8B949E"), on_click=lambda _: setattr(modal, "open", False) or page.update()),
                ft.ElevatedButton(
                    "Equip Title",
                    style=ft.ButtonStyle(color="#0D1117", bgcolor="#00F2FE"),
                    disabled=not is_unlocked,
                    on_click=lambda _: (
                        setattr(athlete, "active_title", ach["title"]),
                        setattr(active_title_text, "value", f"Title: {ach['title']}"),
                        setattr(modal, "open", False),
                        page.update(),
                    ),
                ),
            ],
            bgcolor="#161B22",
        )

        page.dialog = modal
        modal.open = True
        page.update()

    badge_tiles = []
    for ach in achievements:
        is_unlocked = ach["unlocked"]
        tier_style = TIER_STYLING.get(ach["tier"].upper(), {"primary_color": "#8B949E", "border_color": "#30363D"})
        accent = tier_style["primary_color"] if is_unlocked else "#484F58"
        border_c = tier_style["border_color"] if is_unlocked else "#30363D"
        card_bg = "#161B22" if is_unlocked else "#101419"

        item_ref = ach

        badge_tiles.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ach["glyph"], size=28, color=accent),
                            width=56,
                            height=56,
                            border_radius=28,
                            bgcolor=f"{accent}20" if is_unlocked else "#161B22",
                            border=ft.border.all(1.5, border_c),
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(ach["name"], size=12, weight=ft.FontWeight.W_800, color="#F0F6FC" if is_unlocked else "#8B949E", text_align=ft.TextAlign.CENTER),
                        ft.Text(
                            ach["title"] if is_unlocked else "Locked",
                            size=10,
                            color=accent,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "UNLOCKED" if is_unlocked else "LOCKED",
                                size=9,
                                weight=ft.FontWeight.BOLD,
                                color="#10B981" if is_unlocked else "#8B949E",
                            ),
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            border_radius=6,
                            bgcolor="#10B98115" if is_unlocked else "#21262D",
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=165,
                height=180,
                padding=12,
                border_radius=12,
                bgcolor=card_bg,
                border=ft.border.all(1, border_c),
                tooltip="Click to inspect accolade criteria & lore",
                on_click=lambda e, curr=item_ref: open_badge_detail(curr, e),
            )
        )

    shelf_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.icons.MILITARY_TECH_ROUNDED, color="#FFD700", size=24),
                                ft.Text(
                                    "BADGES & ACHIEVEMENTS TROPHY SHELF",
                                    size=16,
                                    weight=ft.FontWeight.W_900,
                                    color="#F0F6FC",
                                    style=ft.TextStyle(letter_spacing=1.0),
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Text("Earned in Full Metallic • Locked in Grayscale", size=11, color="#8B949E"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=1, color="#21262D"),
                ft.Row(
                    controls=badge_tiles,
                    wrap=True,
                    spacing=14,
                ),
            ],
            spacing=12,
        ),
        padding=20,
        border_radius=16,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
    )

    # 4. APK Download Banner Module
    apk_download_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.icons.ANDROID_ROUNDED, size=32, color="#10B981"),
                            width=56,
                            height=56,
                            border_radius=28,
                            bgcolor="#10B98120",
                            border=ft.border.all(1.5, "#10B981"),
                            alignment=ft.alignment.center,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Aesthetic Physique Mobile Client (v1.2.0)", size=15, weight=ft.FontWeight.W_800, color="#F0F6FC"),
                                ft.Text("Includes 52 unilateral routines, offline-first SQLite WAL mode, and wall-clock rest audio.", size=11, color="#8B949E"),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=12,
                ),
                ft.ElevatedButton(
                    text="Download Direct APK (v1.2.0)",
                    icon=ft.icons.DOWNLOAD_ROUNDED,
                    style=ft.ButtonStyle(
                        color="#0D1117",
                        bgcolor="#10B981",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda e: e.control.page.launch_url("https://cdn.aestheticphysique.com/builds/AestheticPhysique-v1.2.0.apk"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=18,
        border_radius=14,
        bgcolor="#161B22",
        border=ft.border.all(1, "#10B98144"),
    )

    # 5. Leaderboard Widget
    leaderboard_widget = create_weekly_leaderboard_widget(current_user_id=athlete["id"])

    # Final Combined Layout
    return ft.Container(
        content=ft.Column(
            controls=[
                profile_banner,
                recovery_row,
                shelf_card,
                leaderboard_widget,
                apk_download_card,
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=24,
        expand=True,
    )
