"""
main_web.py - Aesthetic Physique Master Web Portals Router
Architectural Role: Universal web entry point unifying the Athlete Web Companion Portal
and the Administrative Operations Console with dynamic role switching, route guards,
tabbed administration sub-navigation, and audit-logged dialog coordination.
"""

import os
import sys
import types
from pathlib import Path
import flet as ft
from typing import Dict, Any, Optional

# Ensure both direct imports and package imports resolve in Pyodide/WASM and local dev
CURRENT_DIR = Path(__file__).parent.resolve()
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))
if str(CURRENT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR.parent))

try:
    import portal_admin
    import portal_user
    sys.modules["web_portal.portal_admin"] = portal_admin
    sys.modules["web_portal.portal_user"] = portal_user
    if "web_portal" not in sys.modules:
        wp = types.ModuleType("web_portal")
        wp.portal_admin = portal_admin
        wp.portal_user = portal_user
        sys.modules["web_portal"] = wp
except Exception:
    try:
        import web_portal
    except ImportError:
        web_portal_pkg = types.ModuleType("web_portal")
        web_portal_pkg.__path__ = [str(CURRENT_DIR)]
        sys.modules["web_portal"] = web_portal_pkg

from web_portal.portal_admin.admin_config import (
    ADMIN_NAV_TABS,
    INBOX_ICON_DEFAULT,
    INBOX_ICON_ACTIVE,
    AdminRole,
)
from web_portal.portal_admin.views.admin_dashboard_view import create_admin_dashboard_view
from web_portal.portal_admin.views.edit_user_modal import show_edit_user_modal
from web_portal.portal_admin.views.badge_studio_view import create_badge_studio_view
from web_portal.portal_admin.views.direct_badge_manager import create_direct_badge_manager_view
from web_portal.portal_admin.views.admin_inbox_view import create_admin_inbox_view
from web_portal.portal_admin.views.version_manager_view import create_version_manager_view
from web_portal.portal_user.views.user_portal_view import create_user_portal_view


def main(page: ft.Page):
    page.title = "Aesthetic Physique — Web Portals"
    page.bgcolor = "#0D1117"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK

    # Global session state
    session_state = {
        "active_mode": "user",  # "user" or "admin"
        "admin_tab": "dashboard",  # "dashboard", "badge_studio", "badge_manager", "inbox", "version_manager"
        "current_user": {
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
        },
        "admin_user": {
            "id": "ADM-001",
            "name": "SuperAdmin Operator",
            "role": AdminRole.SUPER_ADMIN.value,
        },
    }

    # Main content container
    content_area = ft.Container(expand=True)

    # Toast banner helper
    def show_toast(message: str, is_error: bool = False):
        snack = ft.SnackBar(
            content=ft.Text(message, color="#0D1117" if not is_error else "#F0F6FC", weight=ft.FontWeight.BOLD),
            bgcolor="#EF4444" if is_error else "#10B981",
            duration=3000,
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # Callback when user record is edited in admin dashboard
    def handle_user_edit_save(updated_record: Dict[str, Any], reason: str):
        show_toast(f"Athlete {updated_record['id']} updated! Audit logged: '{reason[:30]}...'")
        # If the edited athlete is the current session user, update live
        if updated_record.get("id") == session_state["current_user"]["id"]:
            session_state["current_user"].update(updated_record)
        render_current_view()

    def open_edit_modal_callback(user_data: Dict[str, Any]):
        show_edit_user_modal(page, user_data, on_save=handle_user_edit_save)

    # View Builders
    def build_admin_view() -> ft.Control:
        tab = session_state["admin_tab"]
        if tab == "dashboard" or tab == "users":
            return create_admin_dashboard_view(
                on_edit_user=open_edit_modal_callback,
                on_refresh=lambda: show_toast("Admin telemetry and fleet metrics refreshed."),
            )
        elif tab == "badge_studio":
            return create_badge_studio_view(
                on_create_badge=lambda b: show_toast(f"Badge '{b['name']}' published to catalog."),
            )
        elif tab == "badge_manager":
            return create_direct_badge_manager_view(
                on_action_committed=lambda a: show_toast(f"Direct operation logged: {a['action']} for {a['athlete']}."),
            )
        elif tab == "inbox":
            return create_admin_inbox_view(
                on_send_reply=lambda r: show_toast(f"Reply dispatched to ticket {r['ticket_id']}."),
            )
        elif tab == "version_manager":
            return create_version_manager_view(
                on_save_config=lambda c: show_toast(f"Version rules saved. Latest mobile build: v{c['latest_mobile_version']}"),
            )
        else:
            return create_admin_dashboard_view(on_edit_user=open_edit_modal_callback)

    def render_current_view():
        if session_state["active_mode"] == "user":
            admin_subnav_bar.visible = False
            user_nav_btn.style.bgcolor = "#00F2FE22"
            user_nav_btn.style.color = "#00F2FE"
            admin_nav_btn.style.bgcolor = "transparent"
            admin_nav_btn.style.color = "#8B949E"
            identity_chip.content.controls[1].value = f"Athlete: {session_state['current_user']['name']} ({session_state['current_user']['id']})"
            content_area.content = create_user_portal_view(current_athlete=session_state["current_user"])
        else:
            admin_subnav_bar.visible = True
            admin_nav_btn.style.bgcolor = "#00F2FE22"
            admin_nav_btn.style.color = "#00F2FE"
            user_nav_btn.style.bgcolor = "transparent"
            user_nav_btn.style.color = "#8B949E"
            identity_chip.content.controls[1].value = f"Admin: {session_state['admin_user']['name']} [{session_state['admin_user']['role']}]"
            update_admin_subnav_styling()
            content_area.content = build_admin_view()

        page.update()

    # Portal Mode Switch Handlers
    def switch_to_user_mode(e):
        session_state["active_mode"] = "user"
        render_current_view()

    def switch_to_admin_mode(e):
        session_state["active_mode"] = "admin"
        render_current_view()

    # Top Navigation Bar Controls
    brand_logo = ft.Row(
        controls=[
            ft.Container(
                content=ft.Image(
                    src="images/app_icon.png",
                    width=32,
                    height=32,
                    fit=ft.ImageFit.COVER,
                    border_radius=8,
                ),
                width=32,
                height=32,
                border_radius=8,
                bgcolor="#0D1117",
                border=ft.border.all(1, "#00F2FE66"),
                alignment=ft.alignment.center,
            ),
            ft.Text(
                "AESTHETIC PHYSIQUE",
                size=16,
                weight=ft.FontWeight.W_900,
                color="#F0F6FC",
                style=ft.TextStyle(letter_spacing=1.5),
            ),
        ],
        spacing=10,
    )

    user_nav_btn = ft.TextButton(
        text="Athlete Companion",
        icon=ft.icons.PERSON_ROUNDED,
        style=ft.ButtonStyle(
            color="#00F2FE",
            bgcolor="#00F2FE22",
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        on_click=switch_to_user_mode,
    )

    admin_nav_btn = ft.TextButton(
        text="Operations Console",
        icon=ft.icons.ADMIN_PANEL_SETTINGS_ROUNDED,
        style=ft.ButtonStyle(
            color="#8B949E",
            bgcolor="transparent",
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        on_click=switch_to_admin_mode,
    )

    identity_chip = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(width=8, height=8, border_radius=4, bgcolor="#10B981"),
                ft.Text(
                    f"Athlete: {session_state['current_user']['name']} ({session_state['current_user']['id']})",
                    size=11,
                    weight=ft.FontWeight.W_600,
                    color="#C9D1D9",
                ),
            ],
            spacing=8,
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=16,
        bgcolor="#161B22",
        border=ft.border.all(1, "#30363D"),
    )

    topbar = ft.Container(
        content=ft.Row(
            controls=[
                brand_logo,
                ft.Row(
                    controls=[user_nav_btn, admin_nav_btn],
                    spacing=8,
                ),
                identity_chip,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=12),
        bgcolor="#161B22",
        border=ft.border.only(bottom=ft.BorderSide(1, "#21262D")),
    )

    # Admin Sub-navigation Bar
    admin_tab_buttons: Dict[str, ft.TextButton] = {}

    def switch_admin_tab(tab_key: str):
        session_state["admin_tab"] = tab_key
        render_current_view()

    def update_admin_subnav_styling():
        curr_tab = session_state["admin_tab"]
        for key, btn in admin_tab_buttons.items():
            is_active = key == curr_tab
            btn.style.color = "#00F2FE" if is_active else "#8B949E"
            btn.style.bgcolor = "#00F2FE15" if is_active else "transparent"

    subnav_controls = []
    tab_icon_map = {
        "dashboard": ft.icons.ANALYTICS_ROUNDED,
        "users": ft.icons.PEOPLE_ROUNDED,
        "badge_studio": ft.icons.WORKSPACE_PREMIUM_ROUNDED,
        "badge_manager": ft.icons.ASSIGNMENT_IND_ROUNDED,
        "inbox": ft.icons.MARK_EMAIL_UNREAD_ROUNDED,
        "version_manager": ft.icons.PHONELINK_SETUP_ROUNDED,
    }

    for tab_def in ADMIN_NAV_TABS:
        t_key = tab_def["key"]
        t_label = tab_def["label"]
        t_icon = tab_icon_map.get(t_key, ft.icons.ANALYTICS_ROUNDED)

        btn = ft.TextButton(
            text=t_label,
            icon=t_icon,
            style=ft.ButtonStyle(
                color="#8B949E",
                bgcolor="transparent",
                shape=ft.RoundedRectangleBorder(radius=6),
            ),
            on_click=lambda e, k=t_key: switch_admin_tab(k),
        )
        admin_tab_buttons[t_key] = btn
        subnav_controls.append(btn)

    admin_subnav_bar = ft.Container(
        content=ft.Row(
            controls=subnav_controls,
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=ft.padding.symmetric(horizontal=24, vertical=6),
        bgcolor="#0D1117",
        border=ft.border.only(bottom=ft.BorderSide(1, "#21262D")),
        visible=False,
    )

    # Assemble Master Page Layout
    page.add(
        ft.Column(
            controls=[
                topbar,
                admin_subnav_bar,
                content_area,
            ],
            spacing=0,
            expand=True,
        )
    )

    # Initial Render
    render_current_view()


if __name__ == "__main__":
    assets_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    ft.app(target=main, assets_dir=assets_dir_path)
