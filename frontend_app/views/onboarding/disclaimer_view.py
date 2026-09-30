"""
Aesthetic Physique Builder - Legal Disclaimer Screen
Relative Path: frontend_app/views/onboarding/disclaimer_view.py
Architectural Role: Step 1 of the One-Time Legal Compliance Gate (Slides 2 & 3).
Displays legal liability disclaimer; tapping anywhere on the container
or on the 'skip ->' chevron advances to the Warning Screen (/onboarding/warning).
"""

import flet as ft
from database.db_manager import db
from views.responsive_wrapper import create_responsive_view

DISCLAIMER_TEXT = (
    "All exercise routines, animations, timer sequences, and nutritional suggestions "
    "provided within this application have been carefully compiled and verified for "
    "general fitness and educational purposes. However, this application does not provide "
    "medical advice, clinical diagnosis, or individualized healthcare treatment.\n\n"
    "You are solely responsible for assessing your own health condition and physical "
    "limitations before starting any program. The developers and publishers of this application "
    "assume no liability or responsibility for any injury, loss, or health complications resulting "
    "from the use of the content or workouts provided.\n\n"
    "Participation in any exercise session is undertaken entirely at your own risk."
)


def create_disclaimer_view(page: ft.Page, from_settings: bool = False) -> ft.View:
    """
    Renders the Legal Disclaimer Gate view.
    """
    def _advance_to_warning(e=None):
        # Update app_config state if running in onboarding sequence
        if not from_settings:
            db.set_config("has_seen_disclaimer", "true")
            page.go("/onboarding/warning")
        else:
            page.go("/settings/warning")

    # Header with Shield Icon & Title
    header = ft.Column(
        controls=[
            ft.Container(
                content=ft.Icon(
                    name=ft.icons.GAVEL_ROUNDED,
                    size=48,
                    color=ft.colors.LIGHT_BLUE_400,
                ),
                padding=ft.padding.all(16),
                bgcolor="#0B132B",
                border=ft.border.all(1, "#1E293B"),
                border_radius=40,
            ),
            ft.Text(
                value="DISCLAIMER",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                style=ft.TextStyle(letter_spacing=2.0),
            ),
            ft.Text(
                value="Important Health & Liability Notice",
                size=12,
                color=ft.colors.GREY_400,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    # Scrollable Legal Body Card
    body_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    value=DISCLAIMER_TEXT,
                    size=14,
                    color=ft.colors.GREY_300,
                    text_align=ft.TextAlign.JUSTIFY,
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor="#0F172A",
        border=ft.border.all(1, "#1E293B"),
        border_radius=16,
        padding=ft.padding.all(20),
        margin=ft.margin.symmetric(vertical=16),
        expand=True,
    )

    # Footer Chevron "skip ->"
    footer = ft.Row(
        controls=[
            ft.Text(
                value="Tap anywhere to advance",
                size=11,
                color=ft.colors.GREY_500,
            ),
            ft.TextButton(
                content=ft.Row(
                    controls=[
                        ft.Text("skip ->", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_400),
                    ],
                    tight=True,
                ),
                on_click=_advance_to_warning,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Tappable outer surface
    main_container = ft.Container(
        content=ft.Column(
            controls=[
                header,
                body_card,
                footer,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
        ),
        expand=True,
        on_click=_advance_to_warning,
    )

    return create_responsive_view(
        route="/onboarding/disclaimer" if not from_settings else "/settings/disclaimer",
        controls=[main_container],
        page=page,
        scroll=False,
        bg_color="#020617",
    )
