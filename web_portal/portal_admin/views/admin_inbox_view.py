"""
admin_inbox_view.py - Aesthetic Physique Admin Support & Feedback Inbox
Architectural Role: Customer support desk console featuring dynamic unread status
indicators (✉️ -> 📩), structured ticket feed [Subject - User ID | Mail], ticket thread
inspection, and administrative reply composer writing back to the athlete ledger.
"""

import flet as ft
from datetime import datetime
from typing import Callable, Optional, Dict, Any, List
from web_portal.portal_admin.admin_config import (
    TicketStatus,
    INBOX_ICON_DEFAULT,
    INBOX_ICON_ACTIVE,
)


def create_admin_inbox_view(
    on_send_reply: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> ft.Control:
    """
    Constructs the Admin Support & Feedback Inbox view.
    """

    # Mock ticket repository
    tickets = [
        {
            "id": "TCK-101",
            "subject": "Audio Rest Timer Ducking on Bluetooth Headphones",
            "user_id": "ATH-001",
            "user_email": "a.stone@gmail.com",
            "status": TicketStatus.UNREAD.value,
            "created_at": "2026-09-30 09:20",
            "messages": [
                {
                    "sender": "athlete",
                    "text": "Hi team, when I use my AirPods Pro, the 3-2-1 whistle sound volume is slightly low compared to Spotify music playing. Could you adjust the audio ducking threshold?",
                    "timestamp": "2026-09-30 09:20",
                }
            ],
        },
        {
            "id": "TCK-102",
            "subject": "Offline Workout Sync Dispute (Day-D Streak)",
            "user_id": "ATH-002",
            "user_email": "elena.r@outlook.com",
            "status": TicketStatus.UNREAD.value,
            "created_at": "2026-09-29 18:45",
            "messages": [
                {
                    "sender": "athlete",
                    "text": "I completed my Day-D evening pull routine on an airplane without WiFi. When I landed, the app showed Day-D as pending instead of completed, resetting my streak from 28 to 1.",
                    "timestamp": "2026-09-29 18:45",
                },
                {
                    "sender": "admin",
                    "text": "Hello Elena, our FIFO sync worker flushes pending mutations on reconnection. We are checking the local mutation outbox logs for your account.",
                    "timestamp": "2026-09-29 19:10",
                },
            ],
        },
        {
            "id": "TCK-103",
            "subject": "Feature Request: Custom Yoga Routine Timers",
            "user_id": "ATH-003",
            "user_email": "mvance@proton.me",
            "status": TicketStatus.IN_PROGRESS.value,
            "created_at": "2026-09-28 11:30",
            "messages": [
                {
                    "sender": "athlete",
                    "text": "Would it be possible to add custom hold durations for Sunday Yoga flow instead of fixed 45s intervals?",
                    "timestamp": "2026-09-28 11:30",
                }
            ],
        },
        {
            "id": "TCK-104",
            "subject": "Vanity Title Unlocked but Not Equipping",
            "user_id": "ATH-004",
            "user_email": "chloe.b@gmail.com",
            "status": TicketStatus.RESOLVED.value,
            "created_at": "2026-09-27 14:15",
            "messages": [
                {
                    "sender": "athlete",
                    "text": "I unlocked 'Titan of Failure' but my profile banner still shows 'The Aesthetic Initiate'.",
                    "timestamp": "2026-09-27 14:15",
                },
                {
                    "sender": "admin",
                    "text": "Issue resolved. We pushed a remote cache refresh to your device. Please restart the app.",
                    "timestamp": "2026-09-27 15:00",
                },
            ],
        },
    ]

    selected_ticket = {"ref": tickets[0]}

    # Dynamic status indicators
    def get_unread_count() -> int:
        return sum(1 for t in tickets if t["status"] == TicketStatus.UNREAD.value)

    inbox_icon_text = ft.Text(
        INBOX_ICON_ACTIVE if get_unread_count() > 0 else INBOX_ICON_DEFAULT,
        size=26,
    )
    unread_badge = ft.Container(
        content=ft.Text(f"{get_unread_count()} Unread", size=11, color="#EF4444", weight=ft.FontWeight.BOLD),
        padding=ft.padding.symmetric(horizontal=8, vertical=3),
        border_radius=12,
        bgcolor="#EF444420",
        border=ft.border.all(1, "#EF444466"),
    )

    # Conversation View Controls
    thread_subject = ft.Text(selected_ticket["ref"]["subject"], size=16, weight=ft.FontWeight.W_800, color="#F0F6FC")
    thread_meta = ft.Text(
        f"{selected_ticket['ref']['user_id']} | {selected_ticket['ref']['user_email']} • Ticket #{selected_ticket['ref']['id']}",
        size=12,
        color="#8B949E",
    )
    thread_status_dropdown = ft.Dropdown(
        label="Ticket Status",
        value=selected_ticket["ref"]["status"],
        options=[
            ft.dropdown.Option(TicketStatus.UNREAD.value, text="Unread"),
            ft.dropdown.Option(TicketStatus.IN_PROGRESS.value, text="In Progress"),
            ft.dropdown.Option(TicketStatus.RESOLVED.value, text="Resolved"),
        ],
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        width=160,
    )

    messages_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO)
    reply_field = ft.TextField(
        hint_text="Write administrative response directly to athlete's ledger...",
        multiline=True,
        min_lines=3,
        max_lines=4,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        expand=True,
    )
    feedback_alert = ft.Text("", size=11, color="#10B981", weight=ft.FontWeight.W_600, visible=False)

    ticket_feed_column = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)

    def render_messages():
        messages_column.controls.clear()
        for msg in selected_ticket["ref"]["messages"]:
            is_admin = msg["sender"] == "admin"
            bg = "#00F2FE15" if is_admin else "#21262D"
            border_c = "#00F2FE44" if is_admin else "#30363D"
            sender_label = "OPERATOR / ADMIN" if is_admin else f"ATHLETE ({selected_ticket['ref']['user_id']})"
            sender_color = "#00F2FE" if is_admin else "#FFD700"

            bubble = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(sender_label, size=10, weight=ft.FontWeight.BOLD, color=sender_color),
                                ft.Text(msg["timestamp"], size=10, color="#8B949E"),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(msg["text"], size=12, color="#F0F6FC"),
                    ],
                    spacing=6,
                ),
                padding=12,
                border_radius=8,
                bgcolor=bg,
                border=ft.border.all(1, border_c),
                alignment=ft.alignment.center_left,
            )
            messages_column.controls.append(bubble)

    def select_ticket(t: Dict[str, Any], e=None):
        selected_ticket["ref"] = t
        thread_subject.value = t["subject"]
        thread_meta.value = f"{t['user_id']} | {t['user_email']} • Ticket #{t['id']}"
        thread_status_dropdown.value = t["status"]
        feedback_alert.visible = False
        render_messages()
        render_feed()
        if e and hasattr(e, "control") and e.control and e.control.page:
            e.control.page.update()

    def render_feed():
        ticket_feed_column.controls.clear()
        for t in tickets:
            is_selected = t["id"] == selected_ticket["ref"]["id"]
            is_unread = t["status"] == TicketStatus.UNREAD.value
            status_color = "#EF4444" if is_unread else ("#F59E0B" if t["status"] == TicketStatus.IN_PROGRESS.value else "#10B981")

            # Scope closure
            ticket_item = t

            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=8,
                                            height=8,
                                            border_radius=4,
                                            bgcolor=status_color,
                                        ),
                                        ft.Text(
                                            t["subject"],
                                            size=13,
                                            weight=ft.FontWeight.W_700 if is_unread else ft.FontWeight.W_600,
                                            color="#F0F6FC" if is_unread else "#C9D1D9",
                                            max_lines=1,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                            expand=True,
                                        ),
                                    ],
                                    spacing=8,
                                    expand=True,
                                ),
                                ft.Container(
                                    content=ft.Text(t["status"], size=9, weight=ft.FontWeight.BOLD, color=status_color),
                                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                                    border_radius=4,
                                    bgcolor=f"{status_color}20",
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(
                            f"{t['user_id']} | {t['user_email']}",
                            size=11,
                            color="#8B949E",
                        ),
                        ft.Text(
                            t["created_at"],
                            size=10,
                            color="#484F58",
                        ),
                    ],
                    spacing=4,
                ),
                padding=12,
                border_radius=8,
                bgcolor="#1C2128" if is_selected else "#161B22",
                border=ft.border.all(1.5 if is_selected else 1, "#00F2FE" if is_selected else "#21262D"),
                on_click=lambda e, curr=ticket_item: select_ticket(curr, e),
            )
            ticket_feed_column.controls.append(card)

    def handle_status_change(e):
        selected_ticket["ref"]["status"] = thread_status_dropdown.value
        unread_count = get_unread_count()
        inbox_icon_text.value = INBOX_ICON_ACTIVE if unread_count > 0 else INBOX_ICON_DEFAULT
        unread_badge.content.value = f"{unread_count} Unread"
        render_feed()
        e.control.page.update()

    thread_status_dropdown.on_change = handle_status_change

    def handle_submit_reply(e):
        reply_text = reply_field.value.strip() if reply_field.value else ""
        if not reply_text:
            return

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_msg = {
            "sender": "admin",
            "text": reply_text,
            "timestamp": now_str,
        }
        selected_ticket["ref"]["messages"].append(new_msg)
        selected_ticket["ref"]["status"] = TicketStatus.IN_PROGRESS.value
        thread_status_dropdown.value = TicketStatus.IN_PROGRESS.value

        unread_count = get_unread_count()
        inbox_icon_text.value = INBOX_ICON_ACTIVE if unread_count > 0 else INBOX_ICON_DEFAULT
        unread_badge.content.value = f"{unread_count} Unread"

        reply_field.value = ""
        feedback_alert.value = f"Reply dispatched to {selected_ticket['ref']['user_id']}'s active ledger at {now_str}."
        feedback_alert.visible = True

        render_messages()
        render_feed()
        e.control.page.update()

        if on_send_reply:
            on_send_reply({
                "ticket_id": selected_ticket["ref"]["id"],
                "user_id": selected_ticket["ref"]["user_id"],
                "message": reply_text,
                "timestamp": now_str,
            })

    # Initial Render
    render_feed()
    render_messages()

    # Layout Assembly
    header = ft.Row(
        controls=[
            ft.Row(
                controls=[
                    inbox_icon_text,
                    ft.Column(
                        controls=[
                            ft.Text(
                                "SUPPORT & FEEDBACK INBOX",
                                size=20,
                                weight=ft.FontWeight.W_900,
                                color="#F0F6FC",
                                style=ft.TextStyle(letter_spacing=1.5),
                            ),
                            ft.Text(
                                "Direct two-way administrative communication desk writing responses to mobile athlete feeds.",
                                size=13,
                                color="#8B949E",
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
            ),
            unread_badge,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    feed_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("INCOMING ATHLETE TICKETS", size=11, weight=ft.FontWeight.BOLD, color="#8B949E", style=ft.TextStyle(letter_spacing=1.0)),
                ft.Container(content=ticket_feed_column, height=480),
            ],
            spacing=10,
        ),
        padding=16,
        border_radius=12,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
        expand=2,
    )

    thread_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                thread_subject,
                                thread_meta,
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        thread_status_dropdown,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=1, color="#21262D"),
                ft.Container(
                    content=messages_column,
                    height=280,
                    padding=ft.padding.symmetric(vertical=6),
                ),
                ft.Divider(height=1, color="#21262D"),
                reply_field,
                ft.Row(
                    controls=[
                        feedback_alert,
                        ft.ElevatedButton(
                            text="Send Response to Athlete",
                            icon=ft.icons.SEND_ROUNDED,
                            style=ft.ButtonStyle(
                                color="#0D1117",
                                bgcolor="#00F2FE",
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=handle_submit_reply,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=10,
        ),
        padding=20,
        border_radius=12,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
        expand=3,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                header,
                ft.Row(
                    controls=[feed_panel, thread_panel],
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
