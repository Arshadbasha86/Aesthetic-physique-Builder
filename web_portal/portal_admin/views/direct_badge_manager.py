"""
direct_badge_manager.py - Aesthetic Physique Admin Direct Badge Assignment & Revocation
Architectural Role: Operational console for granting special accolades, manual honors,
or revoking compromised achievements with mandatory audit reasoning and historical log ledger.
"""

import flet as ft
from datetime import datetime
from typing import Callable, Optional, Dict, Any, List
from web_portal.portal_admin.admin_config import BadgeTier, TIER_STYLING


def create_direct_badge_manager_view(
    on_action_committed: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> ft.Control:
    """
    Constructs the Direct Badge Assignment & Revocation management console.
    """

    # Mock athletes list
    athletes = [
        {"id": "ATH-001", "name": "Alexander Stone", "email": "a.stone@gmail.com"},
        {"id": "ATH-002", "name": "Elena Rostova", "email": "elena.r@outlook.com"},
        {"id": "ATH-003", "name": "Marcus Vance", "email": "mvance@proton.me"},
        {"id": "ATH-004", "name": "Chloe Bennett", "email": "chloe.b@gmail.com"},
        {"id": "ATH-005", "name": "David Kim", "email": "dkim@techcorp.io"},
    ]

    # Mock badge catalog
    badges = [
        {"id": "BADGE_IRON_WILL", "name": "Iron Will", "tier": "Gold", "title": "The Unyielding"},
        {"id": "BADGE_HYDRATION_SENTINEL", "name": "Hydration Sentinel", "tier": "Silver", "title": "Pure Flow"},
        {"id": "BADGE_TITAN_FAILURE", "name": "Titan of Failure", "tier": "Platinum", "title": "Apex Engine"},
        {"id": "BADGE_SLEEP_MONARCH", "name": "Sleep Monarch", "tier": "Gold", "title": "Somnus Lord"},
        {"id": "BADGE_EARLY_BIRD", "name": "Dawn Vanguard", "tier": "Bronze", "title": "The Early Riser"},
    ]

    # Mock historical ledger data
    history_logs = [
        {
            "timestamp": "2026-09-30 08:15",
            "admin": "SuperAdmin-01",
            "athlete": "ATH-001 (Alexander Stone)",
            "badge": "Titan of Failure",
            "tier": "Platinum",
            "action": "ASSIGNED",
            "reason": "Exceeded 500 failure reps during hypertrophy test cycle.",
        },
        {
            "timestamp": "2026-09-29 19:40",
            "admin": "Coach-03",
            "athlete": "ATH-003 (Marcus Vance)",
            "badge": "Iron Will",
            "tier": "Gold",
            "action": "ASSIGNED",
            "reason": "Completed 30-day streak with flawless wall-clock compliance.",
        },
        {
            "timestamp": "2026-09-28 14:12",
            "admin": "SuperAdmin-01",
            "athlete": "ATH-004 (Chloe Bennett)",
            "badge": "Sleep Monarch",
            "tier": "Gold",
            "action": "REVOKED",
            "reason": "Manual audit revealed incorrect sleep sync timestamp.",
        },
    ]

    # UI Inputs
    athlete_dropdown = ft.Dropdown(
        label="Select Target Athlete",
        value=athletes[0]["id"],
        options=[ft.dropdown.Option(a["id"], text=f"{a['id']} - {a['name']}") for a in athletes],
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    badge_dropdown = ft.Dropdown(
        label="Select Achievement / Badge",
        value=badges[0]["id"],
        options=[ft.dropdown.Option(b["id"], text=f"[{b['tier']}] {b['name']} ({b['title']})") for b in badges],
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=13,
        expand=True,
    )

    action_type = ft.RadioGroup(
        content=ft.Row(
            controls=[
                ft.Radio(value="ASSIGN", label="Grant / Assign Badge", fill_color="#10B981"),
                ft.Radio(value="REVOKE", label="Revoke Badge", fill_color="#EF4444"),
            ],
            spacing=20,
        ),
        value="ASSIGN",
    )

    justification_field = ft.TextField(
        label="Administrative Justification / Reason *",
        hint_text="e.g. Exceptional community leadership, verified live competition record, or manual sync dispute.",
        multiline=True,
        min_lines=2,
        max_lines=3,
        bgcolor="#0D1117",
        border_color="#30363D",
        focused_border_color="#00F2FE",
        text_size=12,
        expand=True,
    )

    status_banner = ft.Text("", size=12, weight=ft.FontWeight.W_600, visible=False)

    # Dynamic Table Rows
    def build_table_rows() -> List[ft.DataRow]:
        rows = []
        for log in history_logs:
            action_color = "#10B981" if log["action"] == "ASSIGNED" else "#EF4444"
            tier_style = TIER_STYLING.get(log["tier"].upper(), {"primary_color": "#8B949E"})
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(log["timestamp"], size=11, color="#8B949E")),
                        ft.DataCell(ft.Text(log["admin"], size=12, color="#F0F6FC", weight=ft.FontWeight.W_600)),
                        ft.DataCell(ft.Text(log["athlete"], size=12, color="#C9D1D9")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(log["badge"], size=11, color=tier_style["primary_color"], weight=ft.FontWeight.BOLD),
                                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                border_radius=6,
                                bgcolor=f"{tier_style['primary_color']}15",
                                border=ft.border.all(1, f"{tier_style['primary_color']}44"),
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(log["action"], size=10, color=action_color, weight=ft.FontWeight.BOLD),
                                padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                border_radius=6,
                                bgcolor=f"{action_color}18",
                            )
                        ),
                        ft.DataCell(
                            ft.Text(log["reason"], size=11, color="#8B949E", max_lines=2, overflow=ft.TextOverflow.ELLIPSIS)
                        ),
                    ]
                )
            )
        return rows

    history_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("TIMESTAMP", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("OPERATOR", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("TARGET ATHLETE", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("BADGE", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("OPERATION", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("JUSTIFICATION AUDIT", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
        ],
        rows=build_table_rows(),
        heading_row_color="#161B22",
        data_row_min_height=48,
        data_row_max_height=56,
        horizontal_lines=ft.border.BorderSide(1, "#21262D"),
    )

    def handle_submit(e):
        reason = justification_field.value.strip() if justification_field.value else ""
        if not reason:
            status_banner.value = "Mandatory administrative justification is required before committing action."
            status_banner.color = "#EF4444"
            status_banner.visible = True
            e.control.page.update()
            return

        target_ath_id = athlete_dropdown.value
        target_ath = next((a for a in athletes if a["id"] == target_ath_id), {"name": "Unknown"})
        target_badge_id = badge_dropdown.value
        target_badge = next((b for b in badges if b["id"] == target_badge_id), {"name": "Unknown", "tier": "Bronze"})
        act = action_type.value

        new_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "admin": "SuperAdmin-01",
            "athlete": f"{target_ath_id} ({target_ath['name']})",
            "badge": target_badge["name"],
            "tier": target_badge["tier"],
            "action": "ASSIGNED" if act == "ASSIGN" else "REVOKED",
            "reason": reason,
        }

        history_logs.insert(0, new_entry)
        history_table.rows = build_table_rows()

        action_word = "granted to" if act == "ASSIGN" else "revoked from"
        status_banner.value = f"Success: Badge '{target_badge['name']}' {action_word} {target_ath['name']}."
        status_banner.color = "#10B981"
        status_banner.visible = True
        justification_field.value = ""

        e.control.page.update()

        if on_action_committed:
            on_action_committed(new_entry)

    # Layout Assembly
    header = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.ASSIGNMENT_IND_ROUNDED, color="#00F2FE", size=26),
                            ft.Text(
                                "DIRECT BADGE ASSIGNMENT & REVOCATION CONSOLE",
                                size=20,
                                weight=ft.FontWeight.W_900,
                                color="#F0F6FC",
                                style=ft.TextStyle(letter_spacing=1.5),
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Text(
                        "Directly award special honors or revoke invalid accolades with strict operator audit logging.",
                        size=13,
                        color="#8B949E",
                    ),
                ],
                spacing=4,
            ),
        ]
    )

    action_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("COMMISSION OR REVOKE ACCOLADE", size=11, weight=ft.FontWeight.BOLD, color="#00F2FE", style=ft.TextStyle(letter_spacing=1.0)),
                ft.Row(controls=[athlete_dropdown, badge_dropdown], spacing=16),
                ft.Column(
                    controls=[
                        ft.Text("Action Mode", size=12, color="#8B949E", weight=ft.FontWeight.W_600),
                        action_type,
                    ],
                    spacing=4,
                ),
                justification_field,
                status_banner,
                ft.ElevatedButton(
                    text="Commit Operation & Log Audit Entry",
                    icon=ft.icons.SECURITY_ROUNDED,
                    style=ft.ButtonStyle(
                        color="#0D1117",
                        bgcolor="#00F2FE",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=handle_submit,
                ),
            ],
            spacing=14,
        ),
        padding=20,
        border_radius=12,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
    )

    history_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "HISTORICAL DIRECT OPERATION LEDGER",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color="#F0F6FC",
                            style=ft.TextStyle(letter_spacing=1.0),
                        ),
                        ft.Text("Immutable Audit Log", size=11, color="#8B949E"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=1, color="#21262D"),
                ft.Container(
                    content=history_table,
                    alignment=ft.alignment.center_left,
                ),
            ],
            spacing=10,
        ),
        padding=20,
        border_radius=12,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                header,
                action_card,
                history_card,
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=24,
        expand=True,
    )
