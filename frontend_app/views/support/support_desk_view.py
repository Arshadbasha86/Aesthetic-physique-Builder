"""
Aesthetic Physique Builder - Customer Support & Feedback Desk
Relative Path: frontend_app/views/support/support_desk_view.py
Architectural Role: In-app support and feedback interface (Slide 27).
Allows trainees to submit tickets/feedback ("Comment your problem:")
and read administrative replies ("Feedback & Response:") offline-first.
"""

import flet as ft
from typing import List, Dict, Any

from database.db_manager import db
from views.responsive_wrapper import create_responsive_view


def create_support_desk_view(page: ft.Page) -> ft.View:
    """
    Renders the Customer Support & Feedback Desk view.
    """
    tickets_list_column = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

    # Form inputs
    subject_input = ft.TextField(
        label="Subject",
        hint_text="e.g. Sync issue or exercise question",
        bgcolor="#0B132B",
        text_size=13,
    )
    category_dropdown = ft.Dropdown(
        value="feedback",
        label="Category",
        options=[
            ft.dropdown.Option("feedback", "General Feedback"),
            ft.dropdown.Option("bug", "Bug Report"),
            ft.dropdown.Option("workout_help", "Workout / Form Help"),
            ft.dropdown.Option("billing", "Billing & Account"),
        ],
        bgcolor="#0B132B",
        text_size=13,
    )
    problem_input = ft.TextField(
        label="Comment your problem / Feedback",
        hint_text="Describe the issue or share your suggestion in detail...",
        multiline=True,
        min_lines=3,
        max_lines=6,
        bgcolor="#0B132B",
        text_size=13,
    )

    feedback_banner = ft.Text(value="", size=12, color="#10B981")

    # Handlers
    def _submit_ticket(e):
        subj = subject_input.value.strip() if subject_input.value else ""
        msg = problem_input.value.strip() if problem_input.value else ""
        cat = category_dropdown.value or "feedback"

        if not subj or not msg:
            feedback_banner.value = "Please enter both a subject and details."
            feedback_banner.color = ft.colors.RED_400
            page.update()
            return

        db.create_support_ticket(subject=subj, category=cat, message=msg)
        subject_input.value = ""
        problem_input.value = ""
        feedback_banner.value = "Your request has been submitted to Admin Support!"
        feedback_banner.color = "#10B981"
        _refresh_tickets()
        page.update()

    def _refresh_tickets():
        tickets = db.get_support_tickets()
        cards = []
        if not tickets:
            cards.append(
                ft.Container(
                    content=ft.Text("No feedback tickets submitted yet.", size=12, color=ft.colors.GREY_500),
                    padding=ft.padding.symmetric(vertical=10),
                    alignment=ft.alignment.center,
                )
            )
        else:
            for t in tickets:
                t_id = t["ticket_id"]
                messages = db.get_support_messages(t_id)
                msg_previews = []
                for m in messages:
                    is_admin = (m["sender_type"] == "admin")
                    msg_previews.append(
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Support Officer" if is_admin else "You", size=10, weight=ft.FontWeight.BOLD, color=ft.colors.AMBER_400 if is_admin else ft.colors.LIGHT_BLUE_300),
                                    ft.Text(m["body"], size=12, color=ft.colors.WHITE),
                                ],
                                spacing=2,
                            ),
                            bgcolor="#1E293B" if is_admin else "#020617",
                            border_radius=8,
                            padding=ft.padding.all(8),
                            margin=ft.margin.only(bottom=4),
                        )
                    )

                card = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text(t["subject"], size=13, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                                    ft.Container(
                                        content=ft.Text(t["status"].upper(), size=9, weight=ft.FontWeight.BOLD, color=ft.colors.LIGHT_BLUE_400),
                                        bgcolor="#020617",
                                        border=ft.border.all(1, ft.colors.LIGHT_BLUE_400),
                                        border_radius=6,
                                        padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(f"Ticket #{t_id} • {t['created_at'][:10]}", size=10, color=ft.colors.GREY_400),
                            ft.Divider(color="#1E293B", height=8),
                            ft.Column(controls=msg_previews, spacing=2),
                        ],
                        spacing=4,
                    ),
                    bgcolor="#0F172A",
                    border=ft.border.all(1, "#1E293B"),
                    border_radius=12,
                    padding=ft.padding.all(12),
                    margin=ft.margin.only(bottom=8),
                )
                cards.append(card)
        tickets_list_column.controls = cards

    # Header with Back Button
    header = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color=ft.colors.WHITE,
                icon_size=18,
                on_click=lambda e: page.go("/profile"),
            ),
            ft.Text("Customer Support & Feedback", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    # Submission Form Card ("Comment your problem:")
    form_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.EDIT_NOTE_ROUNDED, color=ft.colors.LIGHT_BLUE_400, size=20),
                        ft.Text("Comment your problem:", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ],
                    spacing=6,
                ),
                category_dropdown,
                subject_input,
                problem_input,
                feedback_banner,
                ft.ElevatedButton(
                    text="Send Feedback / Submit Ticket",
                    icon=ft.icons.SEND_ROUNDED,
                    bgcolor=ft.colors.LIGHT_BLUE_600,
                    color=ft.colors.WHITE,
                    width=420,
                    height=44,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    on_click=_submit_ticket,
                ),
            ],
            spacing=8,
        ),
        bgcolor="#0F172A",
        border=ft.border.all(1, "#1E293B"),
        border_radius=14,
        padding=ft.padding.all(14),
        margin=ft.margin.only(bottom=10),
    )

    _refresh_tickets()

    # Feed Header ("Feedback & Response:")
    feed_section = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Icon(ft.icons.QUESTION_ANSWER_ROUNDED, color=ft.colors.AMBER_400, size=20),
                    ft.Text("Feedback & Response:", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ],
                spacing=6,
            ),
            tickets_list_column,
        ],
        spacing=8,
        expand=True,
    )

    scrollable_content = ft.Column(
        controls=[
            header,
            form_card,
            feed_section,
        ],
        spacing=8,
        expand=True,
    )

    return create_responsive_view(
        route="/support",
        controls=[scrollable_content],
        page=page,
        scroll=True,
        bg_color="#020617",
    )
