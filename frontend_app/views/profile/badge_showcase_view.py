"""
Aesthetic Physique Builder - Badges, Achievements & Title Showcase
Relative Path: frontend_app/views/profile/badge_showcase_view.py
Architectural Role: Trophy shelf grid view (Slide 24: {Badges, Achievements, Title}).
Visualizes unlocked badges in full metallic color vs. locked badges in
grayscale with padlock overlays, allowing vanity title equipment.
"""

import flet as ft
from typing import List, Dict, Any

from database.db_manager import db
from config.default_config import TIER_COLORS
from views.responsive_wrapper import create_responsive_view

# Optional dynamic import for Step 22 modal
try:
    from views.profile.badge_detail_modal import open_badge_detail_modal
except ImportError:
    def open_badge_detail_modal(page, badge_data, on_title_equipped=None):
        pass


def create_badge_showcase_view(page: ft.Page) -> ft.View:
    """
    Renders the Trophy Shelf Grid view.
    """
    profile = db.get_user_profile()
    equipped_title = profile.get("equipped_title", "Novice Trainee")
    all_badges: List[Dict[str, Any]] = db.get_all_badges_with_status()

    active_filter = "All"
    grid_container = ft.Container(expand=True)

    # Handlers
    def _on_badge_tapped(badge_data: Dict[str, Any]):
        open_badge_detail_modal(page, badge_data, on_title_equipped=_refresh_view)

    def _refresh_view():
        nonlocal profile, equipped_title, all_badges
        profile = db.get_user_profile()
        equipped_title = profile.get("equipped_title", "Novice Trainee")
        all_badges = db.get_all_badges_with_status()
        _render_grid()
        page.update()

    def _filter_badges(filter_name: str):
        nonlocal active_filter
        active_filter = filter_name
        _render_grid()
        page.update()

    def _render_grid():
        filtered = []
        for b in all_badges:
            is_unlocked = bool(b.get("is_unlocked", 0))
            if active_filter == "Earned" and not is_unlocked:
                continue
            if active_filter == "Locked" and is_unlocked:
                continue
            filtered.append(b)

        badge_cards = []
        for b in filtered:
            is_unlocked = bool(b.get("is_unlocked", 0))
            tier = b.get("tier", "bronze").lower()
            tier_color = TIER_COLORS.get(tier, "#CD7F32")
            badge_name = b.get("badge_name", "Badge")
            associated_title = b.get("associated_title", "")
            is_equipped = (associated_title == equipped_title and is_unlocked)

            # Badge Icon Content (Color vs Grayscale)
            badge_icon = ft.Container(
                content=ft.Stack(
                    controls=[
                        ft.Icon(
                            name=ft.icons.WORKSPACE_PREMIUM_ROUNDED,
                            size=44,
                            color=tier_color if is_unlocked else ft.colors.GREY_600,
                        ),
                        ft.Container(
                            content=ft.Icon(ft.icons.LOCK_ROUNDED, size=18, color=ft.colors.WHITE70),
                            alignment=ft.alignment.center,
                            visible=not is_unlocked,
                        ),
                    ],
                    alignment=ft.alignment.center,
                ),
                width=64,
                height=64,
                bgcolor="#0B132B" if is_unlocked else "#020617",
                border=ft.border.all(1.5, tier_color if is_unlocked else "#334155"),
                border_radius=32,
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=12,
                    color=f"{tier_color}44",
                ) if is_unlocked else None,
            )

            card = ft.Container(
                content=ft.Column(
                    controls=[
                        badge_icon,
                        ft.Text(
                            value=badge_name,
                            size=11,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.WHITE if is_unlocked else ft.colors.GREY_500,
                            text_align=ft.TextAlign.CENTER,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Container(
                            content=ft.Text(
                                value="EQUIPPED" if is_equipped else (tier.upper() if is_unlocked else "LOCKED"),
                                size=9,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.LIGHT_BLUE_400 if is_equipped else (ft.colors.WHITE if is_unlocked else ft.colors.GREY_500),
                            ),
                            bgcolor="#020617",
                            border=ft.border.all(1, ft.colors.LIGHT_BLUE_500 if is_equipped else (tier_color if is_unlocked else "#334155")),
                            border_radius=6,
                            padding=ft.padding.symmetric(horizontal=6, vertical=2),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    spacing=4,
                ),
                bgcolor="#0F172A",
                border=ft.border.all(1, "#1E293B"),
                border_radius=14,
                padding=ft.padding.all(10),
                on_click=lambda e, badge=b: _on_badge_tapped(badge),
            )
            badge_cards.append(card)

        grid_container.content = ft.GridView(
            controls=badge_cards,
            runs_count=3,
            max_extent=130,
            spacing=10,
            run_spacing=10,
            expand=True,
        )

    # Header with Back Button
    header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=ft.colors.WHITE,
                icon_size=18,
                on_click=lambda e: page.go("/profile"),
            ),
            ft.Text(
                value="Achievements & Titles",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Active Equipped Title Banner
    active_title_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.STAR_ROUNDED, color=ft.colors.AMBER_400, size=20),
                        ft.Text("Set Display:", size=13, color=ft.colors.GREY_400),
                        ft.Text(equipped_title, size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ],
                    spacing=6,
                ),
                ft.Container(
                    content=ft.Text(
                        f"{sum(1 for b in all_badges if b.get('is_unlocked'))} / {len(all_badges)}",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.LIGHT_BLUE_400,
                    ),
                    bgcolor="#020617",
                    border=ft.border.all(1, "#1E293B"),
                    border_radius=10,
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#0F172A",
        border=ft.border.all(1, "#1E293B"),
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=14, vertical=10),
        margin=ft.margin.symmetric(vertical=8),
    )

    # Filter Segmented Chips
    filters_row = ft.Row(
        controls=[
            ft.TextButton("All", on_click=lambda e: _filter_badges("All")),
            ft.TextButton("Earned", on_click=lambda e: _filter_badges("Earned")),
            ft.TextButton("Locked", on_click=lambda e: _filter_badges("Locked")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )

    _render_grid()

    return create_responsive_view(
        route="/profile/badges",
        controls=[
            header,
            active_title_card,
            filters_row,
            ft.Divider(color="#1E293B", height=1),
            grid_container,
        ],
        page=page,
        scroll=False,
        bg_color="#020617",
    )
