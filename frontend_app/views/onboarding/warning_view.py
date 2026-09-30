"""
Aesthetic Physique Builder - Physical Risk & Injury Warning Screen
Relative Path: frontend_app/views/onboarding/warning_view.py
Architectural Role: Step 2 of the One-Time Legal Compliance Gate (Slides 4 & 5).
Displays physical risk and bodily harm warning; tapping anywhere on the container
or on the 'skip ->' chevron advances to the Week Plan Alignment Wizard
(/onboarding/plan_alignment) or returns to Settings if viewed on-demand.
"""

import flet as ft
from database.db_manager import db
from views.responsive_wrapper import create_responsive_view

WARNING_TEXT = (
    "Exercise at Your Own Risk: Physical workouts carry an inherent risk of muscle "
    "strain, joint stress, or serious bodily injury.\n\n"
    "Any pain, strain, or physical harm experienced during or after an activity indicates "
    "that the movement may have been performed with improper posture, incorrect pacing, "
    "or without adhering to your body’s safe range of motion.\n\n"
    "It is your direct responsibility to maintain correct form, execute movements within "
    "your personal capabilities, and discontinue any workout immediately if you feel pain, "
    "dizziness, or unusual discomfort. Always consult a licensed medical professional before "
    "beginning any new training or nutrition plan."
)


def create_warning_view(page: ft.Page, from_settings: bool = False) -> ft.View:
    """
    Renders the Physical Risk Warning view.
    """
    def _advance(e=None):
        if not from_settings:
            db.set_config("has_seen_warning", "true")
            page.go("/onboarding/plan_alignment")
        else:
            page.go("/settings")

    # Header with Warning Triangle Icon & Title
    header = ft.Column(
        controls=[
            ft.Container(
                content=ft.Icon(
                    name=ft.icons.WARNING_AMBER_ROUNDED,
                    size=48,
                    color=ft.colors.AMBER_400,
                ),
                padding=ft.padding.all(16),
                bgcolor="#1E1B0E",
                border=ft.border.all(1, "#78350F"),
                border_radius=40,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=20,
                    color="#F59E0B22",
                ),
            ),
            ft.Text(
                value="WARNING",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                style=ft.TextStyle(letter_spacing=2.0),
            ),
            ft.Text(
                value="Exercise At Your Own Risk",
                size=12,
                color=ft.colors.AMBER_300,
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
                    value=WARNING_TEXT,
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

    # Footer Chevron "skip ->" / "Accept & Continue ->"
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
                        ft.Text(
                            "skip ->" if not from_settings else "Back to Settings",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.AMBER_400,
                        ),
                    ],
                    tight=True,
                ),
                on_click=_advance,
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
        on_click=_advance,
    )

    return create_responsive_view(
        route="/onboarding/warning" if not from_settings else "/settings/warning",
        controls=[main_container],
        page=page,
        scroll=False,
        bg_color="#020617",
    )
