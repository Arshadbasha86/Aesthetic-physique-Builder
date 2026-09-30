"""
admin_dashboard_view.py - Aesthetic Physique Admin Operations Dashboard
Architectural Role: Main high-level telemetry and fleet management overview
presenting real-time system health, workout volume KPIs, client version distribution,
and an interactive athlete roster with drill-down hooks.
"""

import flet as ft
from typing import Callable, Optional, Dict, Any, List


def create_admin_dashboard_view(
    on_edit_user: Optional[Callable[[Dict[str, Any]], None]] = None,
    on_refresh: Optional[Callable[[], None]] = None,
) -> ft.Control:
    """
    Constructs the Admin Operations Analytics Dashboard.
    Designed for wide desktop/tablet web displays (1200px+ fluid container).
    """

    # 1. Header Row
    header_section = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.icons.SHIELD_ROUNDED, color="#00F2FE", size=28),
                                ft.Text(
                                    "SYSTEM OPERATIONS & TELEMETRY",
                                    size=22,
                                    weight=ft.FontWeight.W_900,
                                    color="#F0F6FC",
                                    style=ft.TextStyle(letter_spacing=1.5),
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Text(
                            "Real-time monitoring of athlete fleet, workout volume, and cloud infrastructure.",
                            size=13,
                            color="#8B949E",
                        ),
                    ],
                    spacing=4,
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        width=8,
                                        height=8,
                                        border_radius=4,
                                        bgcolor="#10B981",
                                    ),
                                    ft.Text(
                                        "SERVER OPERATIONAL",
                                        size=11,
                                        weight=ft.FontWeight.BOLD,
                                        color="#10B981",
                                        style=ft.TextStyle(letter_spacing=1.0),
                                    ),
                                ],
                                spacing=8,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            border=ft.border.all(1, "#10B98144"),
                            border_radius=16,
                            bgcolor="#10B98115",
                        ),
                        ft.ElevatedButton(
                            text="Refresh Data",
                            icon=ft.icons.REFRESH_ROUNDED,
                            style=ft.ButtonStyle(
                                color="#F0F6FC",
                                bgcolor="#21262D",
                                side=ft.BorderSide(1, "#30363D"),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=lambda e: on_refresh() if on_refresh else None,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(bottom=16),
    )

    # 2. Metric KPI Cards
    def make_kpi_card(
        title: str,
        value: str,
        subtitle: str,
        icon: str,
        accent_color: str,
        trend_label: str = "+12% vs last week",
    ) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                title.upper(),
                                size=11,
                                weight=ft.FontWeight.W_700,
                                color="#8B949E",
                                style=ft.TextStyle(letter_spacing=1.0),
                            ),
                            ft.Icon(icon, color=accent_color, size=20),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(
                        value,
                        size=28,
                        weight=ft.FontWeight.W_900,
                        color="#F0F6FC",
                    ),
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.TRENDING_UP_ROUNDED, color="#10B981", size=14),
                            ft.Text(trend_label, size=11, color="#10B981", weight=ft.FontWeight.W_600),
                            ft.Text(f"• {subtitle}", size=11, color="#8B949E"),
                        ],
                        spacing=4,
                    ),
                ],
                spacing=8,
            ),
            padding=16,
            border_radius=12,
            bgcolor="#161B22",
            border=ft.border.all(1, "#21262D"),
            expand=True,
        )

    kpi_grid = ft.Row(
        controls=[
            make_kpi_card(
                "Active Athletes",
                "1,284",
                "342 active today",
                ft.icons.PEOPLE_ROUNDED,
                "#00F2FE",
                "+8.4%",
            ),
            make_kpi_card(
                "Sets Completed",
                "18,920",
                "2,140 today",
                ft.icons.FITNESS_CENTER_ROUNDED,
                "#FFD700",
                "+14.2%",
            ),
            make_kpi_card(
                "Failure Sets",
                "4,821",
                "25.4% intensity ratio",
                ft.icons.LOCAL_FIRE_DEPARTMENT_ROUNDED,
                "#EF4444",
                "+18.1%",
            ),
            make_kpi_card(
                "Rest Compliance",
                "94.6%",
                "Wall-clock audio sync",
                ft.icons.TIMER_ROUNDED,
                "#10B981",
                "+1.2%",
            ),
        ],
        spacing=16,
    )

    # 3. Middle Section: Activity Volume Graph & Version Fleet Breakdown
    volume_bars = [
        ("Mon", 0.65, "2,410"),
        ("Tue", 0.80, "2,950"),
        ("Wed", 0.55, "2,100"),
        ("Thu", 0.90, "3,400"),
        ("Fri", 0.85, "3,150"),
        ("Sat", 0.95, "3,620"),
        ("Sun", 0.40, "1,290"),
    ]

    volume_columns = []
    for day, ratio, count in volume_bars:
        volume_columns.append(
            ft.Column(
                controls=[
                    ft.Text(count, size=9, color="#8B949E", weight=ft.FontWeight.W_600),
                    ft.Container(
                        width=28,
                        height=int(140 * ratio),
                        border_radius=ft.border_radius.only(top_left=6, top_right=6),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_center,
                            end=ft.alignment.bottom_center,
                            colors=["#00F2FE", "#0072B2"],
                        ),
                    ),
                    ft.Text(day, size=11, color="#C9D1D9", weight=ft.FontWeight.W_700),
                ],
                alignment=ft.MainAxisAlignment.END,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            )
        )

    volume_chart_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "WEEKLY TRAINING VOLUME (SETS COMPLETED)",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color="#F0F6FC",
                            style=ft.TextStyle(letter_spacing=1.0),
                        ),
                        ft.Text("7-Day Trajectory", size=11, color="#8B949E"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=1, color="#21262D"),
                ft.Container(
                    height=180,
                    content=ft.Row(
                        controls=volume_columns,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    padding=ft.padding.symmetric(vertical=8),
                ),
            ],
            spacing=10,
        ),
        padding=16,
        border_radius=12,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
        expand=2,
    )

    version_breakdown_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "APP FLEET VERSION ADOPTION",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color="#F0F6FC",
                    style=ft.TextStyle(letter_spacing=1.0),
                ),
                ft.Divider(height=1, color="#21262D"),
                ft.Column(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("v1.2.0 (Latest Release)", size=12, color="#F0F6FC", weight=ft.FontWeight.W_600),
                                        ft.Text("82.4% (1,058)", size=12, color="#10B981", weight=ft.FontWeight.BOLD),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.ProgressBar(value=0.824, color="#10B981", bgcolor="#21262D", height=6),
                            ],
                            spacing=4,
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("v1.1.0 (Supported)", size=12, color="#F0F6FC", weight=ft.FontWeight.W_600),
                                        ft.Text("14.1% (181)", size=12, color="#F59E0B", weight=ft.FontWeight.BOLD),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.ProgressBar(value=0.141, color="#F59E0B", bgcolor="#21262D", height=6),
                            ],
                            spacing=4,
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("v1.0.0 (Legacy / Force Update Pending)", size=12, color="#F0F6FC", weight=ft.FontWeight.W_600),
                                        ft.Text("3.5% (45)", size=12, color="#EF4444", weight=ft.FontWeight.BOLD),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.ProgressBar(value=0.035, color="#EF4444", bgcolor="#21262D", height=6),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=16,
                ),
            ],
            spacing=10,
        ),
        padding=16,
        border_radius=12,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
        expand=1,
    )

    middle_grid = ft.Row(
        controls=[volume_chart_card, version_breakdown_card],
        spacing=16,
    )

    # 4. Athlete Roster Table
    mock_athletes = [
        {"id": "ATH-001", "name": "Alexander Stone", "email": "a.stone@gmail.com", "tier": "Platinum", "streak": 42, "failure_reps": 184, "status": "ACTIVE"},
        {"id": "ATH-002", "name": "Elena Rostova", "email": "elena.r@outlook.com", "tier": "Gold", "streak": 28, "failure_reps": 142, "status": "ACTIVE"},
        {"id": "ATH-003", "name": "Marcus Vance", "email": "mvance@proton.me", "tier": "Gold", "streak": 19, "failure_reps": 98, "status": "ACTIVE"},
        {"id": "ATH-004", "name": "Chloe Bennett", "email": "chloe.b@gmail.com", "tier": "Silver", "streak": 14, "failure_reps": 65, "status": "SUSPENDED"},
        {"id": "ATH-005", "name": "David Kim", "email": "dkim@techcorp.io", "tier": "Bronze", "streak": 7, "failure_reps": 32, "status": "ACTIVE"},
    ]

    tier_color_map = {
        "Platinum": "#00F2FE",
        "Gold": "#FFD700",
        "Silver": "#C0C0C0",
        "Bronze": "#CD7F32",
    }

    table_rows = []
    for ath in mock_athletes:
        tier_color = tier_color_map.get(ath["tier"], "#8B949E")
        status_color = "#10B981" if ath["status"] == "ACTIVE" else "#EF4444"

        # Capture loop closure properly
        ath_data = ath

        table_rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(ath["id"], size=12, color="#8B949E", weight=ft.FontWeight.BOLD)),
                    ft.DataCell(
                        ft.Column(
                            controls=[
                                ft.Text(ath["name"], size=13, weight=ft.FontWeight.W_700, color="#F0F6FC"),
                                ft.Text(ath["email"], size=11, color="#8B949E"),
                            ],
                            spacing=2,
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(ath["tier"], size=11, weight=ft.FontWeight.BOLD, color=tier_color),
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            border_radius=12,
                            border=ft.border.all(1, f"{tier_color}66"),
                            bgcolor=f"{tier_color}1A",
                        )
                    ),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, color="#F59E0B", size=14),
                                ft.Text(f"{ath['streak']} Days", size=12, color="#F0F6FC", weight=ft.FontWeight.W_600),
                            ],
                            spacing=4,
                        )
                    ),
                    ft.DataCell(
                        ft.Text(f"{ath['failure_reps']} Reps", size=12, color="#F0F6FC", weight=ft.FontWeight.W_600)
                    ),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(ath["status"], size=10, weight=ft.FontWeight.BOLD, color=status_color),
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            border_radius=8,
                            bgcolor=f"{status_color}20",
                        )
                    ),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.icons.EDIT_NOTE_ROUNDED,
                            icon_color="#00F2FE",
                            tooltip="Inspect / Edit Athlete Record",
                            on_click=lambda e, u=ath_data: on_edit_user(u) if on_edit_user else None,
                        )
                    ),
                ]
            )
        )

    roster_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ATHLETE ID", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("NAME & ACCOUNT", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("TIER", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("STREAK", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("FAILURE REPS", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("STATUS", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("ACTIONS", size=11, weight=ft.FontWeight.BOLD, color="#8B949E")),
        ],
        rows=table_rows,
        heading_row_color="#161B22",
        data_row_min_height=52,
        data_row_max_height=60,
        horizontal_lines=ft.border.BorderSide(1, "#21262D"),
    )

    roster_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "ACTIVE ATHLETES ROSTER",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color="#F0F6FC",
                            style=ft.TextStyle(letter_spacing=1.0),
                        ),
                        ft.Text("Showing Top 5 Active Records", size=11, color="#8B949E"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=1, color="#21262D"),
                ft.Container(
                    content=roster_table,
                    alignment=ft.alignment.center_left,
                ),
            ],
            spacing=10,
        ),
        padding=16,
        border_radius=12,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
    )

    # Combine into main dashboard layout container
    return ft.Container(
        content=ft.Column(
            controls=[
                header_section,
                kpi_grid,
                middle_grid,
                roster_card,
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        ),
        padding=24,
        expand=True,
    )
