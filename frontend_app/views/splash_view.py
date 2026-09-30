"""
Aesthetic Physique Builder - Splash Screen & Startup Lifecycle Gate
Relative Path: frontend_app/views/splash_view.py
Architectural Role: Displays the initial branded splash view (Slide 1),
executes a 2.0-second timer, and intercepts onboarding state to route
either to the Legal Gate (/onboarding/disclaimer) or Home (/workouts).
"""

import time
import threading
import flet as ft

from config.default_config import APP_NAME, APP_SLOGAN, SPLASH_SCREEN_DURATION_SEC
from database.db_manager import db
from views.responsive_wrapper import create_responsive_view


def create_splash_view(page: ft.Page) -> ft.View:
    """
    Renders the opening splash screen and initiates the 2.0s lifecycle transition.
    """
    # Animated opacity container for smooth dissolve effect
    branding_content = ft.Container(
        content=ft.Column(
            controls=[
                # Solo Developer signature tag
                ft.Container(
                    content=ft.Text(
                        value="BASHA",
                        size=14,
                        weight=ft.FontWeight.W_800,
                        color=ft.colors.AMBER_400,
                        style=ft.TextStyle(letter_spacing=3.0),
                    ),
                    padding=ft.padding.only(bottom=16),
                ),
                # Official Aesthetic Physique Icon (Classical Greek Statue Bust)
                ft.Container(
                    content=ft.Image(
                        src="images/app_icon.png",
                        width=140,
                        height=140,
                        fit=ft.ImageFit.CONTAIN,
                        border_radius=24,
                    ),
                    padding=ft.padding.all(8),
                    bgcolor="#0B132B",
                    border=ft.border.all(2, "#00F2FE66"),
                    border_radius=28,
                    shadow=ft.BoxShadow(
                        spread_radius=4,
                        blur_radius=35,
                        color="#00F2FE44",
                        offset=ft.Offset(0, 6),
                    ),
                ),
                # Primary Brand Title
                ft.Container(
                    content=ft.Text(
                        value=APP_NAME,
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                        style=ft.TextStyle(letter_spacing=1.0),
                    ),
                    padding=ft.padding.only(top=24, bottom=6),
                ),
                # Subtitle Slogan
                ft.Text(
                    value=APP_SLOGAN,
                    size=14,
                    weight=ft.FontWeight.W_400,
                    color=ft.colors.GREY_400,
                    style=ft.TextStyle(letter_spacing=1.5),
                ),
                # Subtle Loading Pulse Indicator
                ft.Container(
                    content=ft.ProgressRing(
                        width=22,
                        height=22,
                        stroke_width=2.5,
                        color=ft.colors.LIGHT_BLUE_400,
                    ),
                    padding=ft.padding.only(top=48),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0,
        ),
        alignment=ft.alignment.center,
        expand=True,
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        opacity=1.0,
    )

    def _execute_lifecycle_transition():
        # Sleep for prescribed 2.0s splash display duration
        time.sleep(SPLASH_SCREEN_DURATION_SEC)

        # Trigger fade-out dissolve
        branding_content.opacity = 0.0
        try:
            page.update()
        except Exception:
            pass

        # Brief pause to allow fade-out completion before routing
        time.sleep(0.3)

        # Route evaluation: Check if first-time user needs legal onboarding
        if db.is_onboarding_completed():
            page.go("/workouts")
        else:
            page.go("/onboarding/disclaimer")

    # Start transition timer in background thread
    threading.Thread(target=_execute_lifecycle_transition, daemon=True).start()

    return create_responsive_view(
        route="/",
        controls=[branding_content],
        page=page,
        scroll=False,
        bg_color="#020617",
    )
