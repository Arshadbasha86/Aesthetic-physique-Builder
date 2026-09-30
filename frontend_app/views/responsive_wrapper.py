"""
Aesthetic Physique Builder - Responsive Viewport & Multi-Device Container
Relative Path: frontend_app/views/responsive_wrapper.py
Architectural Role: Wraps all application views into a strict portrait 460px
mobile shell that remains centered and letterboxed with dark slate backdrop
(#0D1117) and elevation shadows across tablets, PCs, and web browsers.
"""

import flet as ft
from typing import List, Optional
from config.default_config import (
    MOBILE_VIEWPORT_WIDTH, MOBILE_VIEWPORT_HEIGHT,
    COLOR_LETTERBOX_BG, COLOR_BG_PRIMARY
)


def create_responsive_view(
    route: str,
    controls: List[ft.Control],
    page: ft.Page,
    appbar: Optional[ft.AppBar] = None,
    bottom_appbar: Optional[ft.BottomAppBar] = None,
    floating_action_button: Optional[ft.FloatingActionButton] = None,
    scroll: bool = True,
    bg_color: str = "#020617",
    padding: int = 16,
) -> ft.View:
    """
    Wraps routed views into a locked portrait container (460px max width)
    that remains centered and phone-proportioned across Tablets, PCs, and Mobile browsers.
    """
    # Configure desktop / web window bounds
    try:
        page.window_width = MOBILE_VIEWPORT_WIDTH
        page.window_height = MOBILE_VIEWPORT_HEIGHT
        page.window_resizable = True
    except Exception:
        pass

    # Inner mobile column containing the page controls
    inner_content = ft.Column(
        controls=controls,
        scroll=ft.ScrollMode.AUTO if scroll else None,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
    )

    # 460px Mobile Shell Container
    mobile_shell = ft.Container(
        width=MOBILE_VIEWPORT_WIDTH,
        expand=True,
        bgcolor=bg_color,
        alignment=ft.alignment.top_center,
        padding=padding,
        border=ft.border.all(1, "#1E293B"),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=25,
            color=ft.colors.BLACK54,
            offset=ft.Offset(0, 4),
        ) if page.width and page.width > 500 else None,
        content=inner_content,
    )

    # Outer letterboxed view
    return ft.View(
        route=route,
        appbar=appbar,
        bottom_appbar=bottom_appbar,
        floating_action_button=floating_action_button,
        padding=0,
        spacing=0,
        bgcolor=COLOR_LETTERBOX_BG if page.width and page.width > 500 else bg_color,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[mobile_shell],
    )
