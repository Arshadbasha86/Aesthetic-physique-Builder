"""
Aesthetic Physique Builder - Device Settings & Voice Options Console
Relative Path: frontend_app/views/settings/settings_view.py
Architectural Role: Hardware & Audio-Tactile Settings (Slides 25 & 26).
Configures Voice TTS personas with live test clips, speech rate/volume sliders,
haptics, screen awake, DND auto-suppression, daily reminders, and website launcher.
"""

import flet as ft
from typing import Dict, Any

from database.db_manager import db
from config.default_config import AVAILABLE_COACH_PERSONAS, DEFAULT_COACH_PERSONA
from engine.audio_coordinator import audio_coordinator
from views.responsive_wrapper import create_responsive_view


def create_settings_view(page: ft.Page) -> ft.View:
    """
    Renders the Hardware & System Settings view.
    """
    all_settings: Dict[str, str] = db.get_all_settings()

    selected_persona = all_settings.get("selected_persona", DEFAULT_COACH_PERSONA)
    tts_enabled = all_settings.get("voice_tts_enabled", "true").lower() == "true"
    haptics_enabled = all_settings.get("haptics_enabled", "true").lower() == "true"
    screen_awake = all_settings.get("screen_awake_during_workout", "true").lower() == "true"
    dnd_enabled = all_settings.get("dnd_during_workout", "false").lower() == "true"
    daily_reminder = all_settings.get("daily_reminder_enabled", "true").lower() == "true"

    # Handlers
    def _toggle_setting(key: str, val: bool):
        db.set_setting(key, "true" if val else "false")
        page.update()

    def _select_persona(persona_key: str):
        nonlocal selected_persona
        selected_persona = persona_key
        db.set_setting("selected_persona", persona_key)
        _rebuild_persona_list()
        page.update()

    def _test_persona_audio(persona_key: str):
        db.set_setting("selected_persona", persona_key)
        audio_coordinator.speak_cue("test", fallback_text=f"Hi, I am your workout coach {persona_key.capitalize()}. Let's get started!")

    def _launch_website(e):
        url = db.get_config("website_url", "https://aestheticphysique.app")
        page.launch_url(url)
        page.snack_bar = ft.SnackBar(ft.Text(f"Opening {url}..."), bgcolor=ft.colors.LIGHT_BLUE_700)
        page.snack_bar.open = True
        page.update()

    # Header with Back Button
    header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=ft.colors.WHITE,
                icon_size=18,
                on_click=lambda e: page.go("/profile"),
            ),
            ft.Text("Settings Console", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # --------------------------------------------------------------------------
    # 1. Voice Coach Personas Section (Slide 26)
    # --------------------------------------------------------------------------
    persona_column = ft.Column(spacing=8)

    def _rebuild_persona_list():
        cards = []
        for p_key, p_data in AVAILABLE_COACH_PERSONAS.items():
            is_active = (p_key == selected_persona)
            card = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Radio(
                                    value=p_key,
                                    active_color=ft.colors.LIGHT_BLUE_400,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text(f"{p_data['name']} ({p_data['accent']})", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                        ft.Text(p_data["style"], size=11, color=ft.colors.GREY_400),
                                    ],
                                    spacing=2,
                                ),
                            ],
                            spacing=6,
                        ),
                        ft.ElevatedButton(
                            text="Test",
                            icon=ft.icons.VOLUME_UP_ROUNDED,
                            bgcolor="#1E293B",
                            color=ft.colors.LIGHT_BLUE_400,
                            height=36,
                            on_click=lambda e, k=p_key: _test_persona_audio(k),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor="#0F172A",
                border=ft.border.all(1, ft.colors.LIGHT_BLUE_500 if is_active else "#1E293B"),
                border_radius=12,
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                on_click=lambda e, k=p_key: _select_persona(k),
            )
            cards.append(card)
        persona_column.controls = cards

    _rebuild_persona_list()

    voice_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row([ft.Icon(ft.icons.RECORD_VOICE_OVER_ROUNDED, color=ft.colors.LIGHT_BLUE_400), ft.Text("Voice TTS Coach", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)], spacing=8),
                        ft.Switch(value=tts_enabled, active_color=ft.colors.LIGHT_BLUE_400, on_change=lambda e: _toggle_setting("voice_tts_enabled", e.control.value)),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text("Select your training coach persona:", size=12, color=ft.colors.GREY_400),
                persona_column,
            ],
            spacing=10,
        ),
        bgcolor="#0B132B",
        border=ft.border.all(1, "#1E293B"),
        border_radius=14,
        padding=ft.padding.all(14),
    )

    # --------------------------------------------------------------------------
    # 2. Hardware Toggles Section (Slide 25)
    # --------------------------------------------------------------------------
    def _make_toggle_tile(title: str, subtitle: str, icon, init_val: bool, on_change_fn):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icon, size=20, color=ft.colors.LIGHT_BLUE_400),
                            ft.Column(
                                controls=[
                                    ft.Text(title, size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                    ft.Text(subtitle, size=11, color=ft.colors.GREY_400),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Switch(value=init_val, active_color=ft.colors.LIGHT_BLUE_400, on_change=on_change_fn),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#0F172A",
            border=ft.border.all(1, "#1E293B"),
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=12, vertical=10),
            margin=ft.margin.only(bottom=6),
        )

    toggles_list = ft.Column(
        controls=[
            _make_toggle_tile("Haptics & Tactile Cues", "Vibration on timer triggers & sets", ft.icons.VIBRATION_ROUNDED, haptics_enabled, lambda e: _toggle_setting("haptics_enabled", e.control.value)),
            _make_toggle_tile("Screen Awake", "Keep screen on throughout active workouts", ft.icons.SCREEN_LOCK_PORTRAIT_ROUNDED, screen_awake, lambda e: _toggle_setting("screen_awake_during_workout", e.control.value)),
            _make_toggle_tile("Do Not Disturb (DND)", "Silence alerts automatically in sessions", ft.icons.DO_NOT_DISTURB_ON_TOTAL_SILENCE_ROUNDED, dnd_enabled, lambda e: _toggle_setting("dnd_during_workout", e.control.value)),
            _make_toggle_tile("Daily Workout Reminder", "Morning alert (06:30 AM)", ft.icons.NOTIFICATIONS_ACTIVE_ROUNDED, daily_reminder, lambda e: _toggle_setting("daily_reminder_enabled", e.control.value)),
        ],
        spacing=2,
    )

    # --------------------------------------------------------------------------
    # 3. Dynamic Website Launcher Tile
    # --------------------------------------------------------------------------
    website_tile = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.LANGUAGE_ROUNDED, size=20, color=ft.colors.AMBER_400),
                        ft.Column(
                            controls=[
                                ft.Text("Website (Website URL)", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                ft.Text("Visit official companion & admin domain", size=11, color=ft.colors.GREY_400),
                            ],
                            spacing=2,
                        ),
                    ],
                    spacing=10,
                ),
                ft.IconButton(
                    icon=ft.icons.OPEN_IN_NEW_ROUNDED,
                    icon_color=ft.colors.AMBER_400,
                    tooltip="Open in Browser",
                    on_click=_launch_website,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor="#0F172A",
        border=ft.border.all(1, "#1E293B"),
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=12, vertical=10),
        margin=ft.margin.symmetric(vertical=6),
    )

    scrollable_content = ft.Column(
        controls=[
            header,
            voice_section,
            ft.Text("Device Controls", size=13, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_400),
            toggles_list,
            website_tile,
        ],
        spacing=12,
    )

    return create_responsive_view(
        route="/settings",
        controls=[scrollable_content],
        page=page,
        scroll=True,
        bg_color="#020617",
    )
