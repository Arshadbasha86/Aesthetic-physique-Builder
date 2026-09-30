"""
version_manager_view.py - Aesthetic Physique Admin Version & Documentation Manager
Architectural Role: Server-side configuration console for mobile client release versions,
minimum required build gating, force-update kill switches, CDN download endpoints,
and dynamic web URL launcher targets.
"""

import flet as ft
from typing import Callable, Optional, Dict, Any
from web_portal.portal_admin.admin_config import DEFAULT_VERSION_CONFIG


def create_version_manager_view(
    on_save_config: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> ft.Control:
    """
    Constructs the Platform Documentation & Version Management console.
    """

    # Input Form Fields
    latest_version_field = ft.TextField(
        label="Latest Mobile Version (SemVer)",
        value=DEFAULT_VERSION_CONFIG["latest_mobile_version"],
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    min_version_field = ft.TextField(
        label="Minimum Required Build (Hard Gate)",
        value=DEFAULT_VERSION_CONFIG["min_required_mobile_version"],
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    apk_download_field = ft.TextField(
        label="Production APK Direct Download CDN Endpoint",
        value=DEFAULT_VERSION_CONFIG["apk_download_url"],
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        expand=True,
    )

    docs_url_field = ft.TextField(
        label="Official Athlete Documentation & Handbook URL",
        value=DEFAULT_VERSION_CONFIG["documentation_url"],
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        expand=True,
    )

    companion_portal_url_field = ft.TextField(
        label="Web Companion Portal URL",
        value="https://portal.aestheticphysique.com",
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        expand=True,
    )

    terms_url_field = ft.TextField(
        label="Terms of Service & Legal Disclaimer URL",
        value="https://aestheticphysique.com/legal/terms",
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        expand=True,
    )

    force_update_switch = ft.Switch(
        label="Enforce Mandatory Hard Update (Blocks Legacy Clients)",
        value=DEFAULT_VERSION_CONFIG["force_update_flag"],
        active_color="#EF4444",
    )

    release_notes_field = ft.TextField(
        label="Client Release Notes & Changelog",
        value=DEFAULT_VERSION_CONFIG["release_notes"],
        multiline=True,
        min_lines=3,
        max_lines=4,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        expand=True,
    )

    save_alert = ft.Text("", size=12, color="#10B981", weight=ft.FontWeight.W_600, visible=False)

    # Client Simulator Preview
    simulator_header = ft.Text("CLIENT ENFORCEMENT SIMULATION", size=10, weight=ft.FontWeight.BOLD, color="#8B949E")
    simulator_state_text = ft.Text("Status: Up to Date", size=13, weight=ft.FontWeight.BOLD, color="#10B981")
    simulator_desc_text = ft.Text(
        "Athletes running v1.2.0 enjoy full offline/online capabilities with zero interruption.",
        size=11,
        color="#8B949E",
        text_align=ft.TextAlign.CENTER,
    )
    simulator_cta_button = ft.ElevatedButton(
        text="All Systems Go",
        icon=ft.icons.CHECK_CIRCLE_ROUNDED,
        style=ft.ButtonStyle(color="#0D1117", bgcolor="#10B981"),
        disabled=True,
    )

    simulator_card = ft.Container(
        content=ft.Column(
            controls=[
                simulator_header,
                ft.Container(
                    content=ft.Icon(ft.icons.SMARTPHONE_ROUNDED, size=40, color="#10B981"),
                    width=64,
                    height=64,
                    border_radius=32,
                    bgcolor="#10B98120",
                    border=ft.border.all(1.5, "#10B981"),
                    alignment=ft.alignment.center,
                ),
                simulator_state_text,
                simulator_desc_text,
                simulator_cta_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=20,
        border_radius=16,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
        alignment=ft.alignment.center,
        width=300,
    )

    def update_simulator(e=None):
        forced = force_update_switch.value
        min_ver = min_version_field.value or "1.0.0"
        lat_ver = latest_version_field.value or "1.2.0"

        if forced:
            simulator_state_text.value = "CRITICAL: MANDATORY UPDATE ACTIVE"
            simulator_state_text.color = "#EF4444"
            simulator_desc_text.value = f"All client builds below v{lat_ver} are immediately hard-blocked at splash screen."
            simulator_cta_button.text = f"Download APK (v{lat_ver})"
            simulator_cta_button.icon = ft.icons.DOWNLOAD_ROUNDED
            simulator_cta_button.style = ft.ButtonStyle(color="#F0F6FC", bgcolor="#EF4444")
            simulator_cta_button.disabled = False
            simulator_card.border = ft.border.all(1.5, "#EF4444")
        else:
            simulator_state_text.value = "STANDARD GATING ACTIVE"
            simulator_state_text.color = "#10B981"
            simulator_desc_text.value = f"Clients >= v{min_ver} function smoothly. Build v{lat_ver} promoted via in-app banner."
            simulator_cta_button.text = "All Systems Go"
            simulator_cta_button.icon = ft.icons.CHECK_CIRCLE_ROUNDED
            simulator_cta_button.style = ft.ButtonStyle(color="#0D1117", bgcolor="#10B981")
            simulator_cta_button.disabled = True
            simulator_card.border = ft.border.all(1, "#21262D")

        if e and hasattr(e, "control") and e.control and e.control.page:
            e.control.page.update()

    force_update_switch.on_change = update_simulator
    min_version_field.on_change = update_simulator
    latest_version_field.on_change = update_simulator

    def handle_save_config(e):
        payload = {
            "latest_mobile_version": latest_version_field.value.strip(),
            "min_required_mobile_version": min_version_field.value.strip(),
            "apk_download_url": apk_download_field.value.strip(),
            "documentation_url": docs_url_field.value.strip(),
            "companion_portal_url": companion_portal_url_field.value.strip(),
            "terms_url": terms_url_field.value.strip(),
            "force_update_flag": force_update_switch.value,
            "release_notes": release_notes_field.value.strip(),
        }

        save_alert.value = "Platform configuration & dynamic URL routes published to mobile fleet."
        save_alert.visible = True
        e.control.page.update()

        if on_save_config:
            on_save_config(payload)

    # Layout Assembly
    header = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.PHONELINK_SETUP_ROUNDED, color="#00F2FE", size=26),
                            ft.Text(
                                "PLATFORM DOCUMENTATION & VERSION MANAGER",
                                size=20,
                                weight=ft.FontWeight.W_900,
                                color="#F0F6FC",
                                style=ft.TextStyle(letter_spacing=1.5),
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Text(
                        "Manage mobile client build compatibility, forced update kill switches, CDN endpoints, and dynamic URLs.",
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
                ft.Text("1. CLIENT VERSION & BUILD COMPATIBILITY GATING", size=11, weight=ft.FontWeight.BOLD, color="#00F2FE", style=ft.TextStyle(letter_spacing=1.0)),
                ft.Row(controls=[latest_version_field, min_version_field], spacing=16),
                ft.Container(
                    content=force_update_switch,
                    padding=ft.padding.symmetric(vertical=4),
                ),
                release_notes_field,
                ft.Divider(height=1, color="#21262D"),
                ft.Text("2. PRODUCTION CDN DOWNLOAD ENDPOINTS", size=11, weight=ft.FontWeight.BOLD, color="#00F2FE", style=ft.TextStyle(letter_spacing=1.0)),
                apk_download_field,
                ft.Divider(height=1, color="#21262D"),
                ft.Text("3. DYNAMIC URL LAUNCHER ENDPOINTS", size=11, weight=ft.FontWeight.BOLD, color="#00F2FE", style=ft.TextStyle(letter_spacing=1.0)),
                ft.Row(controls=[docs_url_field, companion_portal_url_field], spacing=16),
                terms_url_field,
                save_alert,
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Publish Configuration to Ecosystem",
                        icon=ft.icons.CLOUD_UPLOAD_ROUNDED,
                        style=ft.ButtonStyle(
                            color="#0D1117",
                            bgcolor="#00F2FE",
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=handle_save_config,
                    ),
                    padding=ft.padding.only(top=8),
                ),
            ],
            spacing=14,
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
                ft.Text("FLEET BEHAVIOR SIMULATOR", size=11, weight=ft.FontWeight.BOLD, color="#8B949E", style=ft.TextStyle(letter_spacing=1.0)),
                simulator_card,
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
