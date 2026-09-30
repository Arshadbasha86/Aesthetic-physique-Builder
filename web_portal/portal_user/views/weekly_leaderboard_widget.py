"""
weekly_leaderboard_widget.py - Aesthetic Physique Athlete Companion Weekly Arena
Architectural Role: Gamification leaderboard component featuring visual podium
standings for Ranks 1-3 (Gold, Silver, Bronze), extended roster for Ranks 4-10,
and real-time XP calculation based on consistency, intensity, and failure volume.
"""

import flet as ft
from typing import List, Dict, Any, Optional


def calculate_athlete_xp(
    workouts_completed: int,
    failure_reps: int,
    streak_days: int,
    hydration_days: int = 7,
) -> int:
    """
    Standardized Aesthetic Physique Weekly XP Formula:
    XP = (Workouts * 100) + (Failure Reps * 15) + (Streak Days * 25) + (Hydration Days * 10)
    """
    return (
        (workouts_completed * 100)
        + (failure_reps * 15)
        + (streak_days * 25)
        + (hydration_days * 10)
    )


def create_weekly_leaderboard_widget(
    current_user_id: str = "ATH-004",
) -> ft.Control:
    """
    Constructs the Weekly Arena Leaderboard component for the User Web Companion Portal.
    """

    # Mock weekly standings dataset
    raw_athletes = [
        {
            "rank": 1,
            "id": "ATH-001",
            "name": "Alexander Stone",
            "title": "Titan of Failure",
            "tier": "Platinum",
            "workouts": 6,
            "failure_reps": 68,
            "streak": 42,
            "hydration_days": 7,
        },
        {
            "rank": 2,
            "id": "ATH-002",
            "name": "Elena Rostova",
            "title": "Somnus Lord",
            "tier": "Gold",
            "workouts": 6,
            "failure_reps": 52,
            "streak": 28,
            "hydration_days": 7,
        },
        {
            "rank": 3,
            "id": "ATH-003",
            "name": "Marcus Vance",
            "title": "The Unyielding",
            "tier": "Gold",
            "workouts": 5,
            "failure_reps": 44,
            "streak": 19,
            "hydration_days": 6,
        },
        {
            "rank": 4,
            "id": "ATH-004",
            "name": "Chloe Bennett (You)",
            "title": "Pure Flow",
            "tier": "Silver",
            "workouts": 5,
            "failure_reps": 38,
            "streak": 14,
            "hydration_days": 6,
        },
        {
            "rank": 5,
            "id": "ATH-005",
            "name": "David Kim",
            "title": "The Early Riser",
            "tier": "Bronze",
            "workouts": 4,
            "failure_reps": 26,
            "streak": 7,
            "hydration_days": 5,
        },
        {
            "rank": 6,
            "id": "ATH-006",
            "name": "Sarah Connor",
            "title": "Iron Initiate",
            "tier": "Silver",
            "workouts": 4,
            "failure_reps": 22,
            "streak": 11,
            "hydration_days": 5,
        },
        {
            "rank": 7,
            "id": "ATH-007",
            "name": "James Wilson",
            "title": "Aesthetic Disciple",
            "tier": "Bronze",
            "workouts": 3,
            "failure_reps": 18,
            "streak": 5,
            "hydration_days": 4,
        },
    ]

    # Calculate XP for all athletes
    for ath in raw_athletes:
        ath["xp"] = calculate_athlete_xp(
            ath["workouts"],
            ath["failure_reps"],
            ath["streak"],
            ath["hydration_days"],
        )

    # Sort descending by XP
    raw_athletes.sort(key=lambda x: x["xp"], reverse=True)
    for idx, ath in enumerate(raw_athletes, start=1):
        ath["rank"] = idx

    top_3 = raw_athletes[:3]
    ranks_4_plus = raw_athletes[3:]

    # Helper: Podium Card for Ranks 1, 2, 3
    def make_podium_card(
        ath: Dict[str, Any],
        rank: int,
        accent_color: str,
        podium_height: int,
        is_first: bool = False,
    ) -> ft.Container:
        crown_icon = (
            ft.Icon(ft.icons.EMOJI_EVENTS_ROUNDED, color="#FFD700", size=24)
            if is_first
            else ft.Container(height=8)
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    crown_icon,
                    ft.Container(
                        content=ft.Text(
                            str(rank),
                            size=18,
                            weight=ft.FontWeight.W_900,
                            color="#0D1117" if is_first else "#F0F6FC",
                        ),
                        width=38,
                        height=38,
                        border_radius=19,
                        bgcolor=accent_color,
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        ath["name"],
                        size=13,
                        weight=ft.FontWeight.W_800,
                        color="#F0F6FC",
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(
                        ath["title"],
                        size=11,
                        color=accent_color,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Container(
                        content=ft.Text(
                            f"{ath['xp']:,} XP",
                            size=13,
                            weight=ft.FontWeight.W_900,
                            color="#00F2FE",
                        ),
                        padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        bgcolor="#0D1117",
                        border_radius=8,
                        border=ft.border.all(1, f"{accent_color}44"),
                    ),
                    ft.Text(
                        f"{ath['workouts']} Sessions • {ath['failure_reps']} Failure Reps",
                        size=10,
                        color="#8B949E",
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=210,
            height=podium_height,
            padding=12,
            border_radius=16,
            bgcolor="#161B22",
            border=ft.border.all(2 if is_first else 1, accent_color),
            alignment=ft.alignment.center,
        )

    # Order podium visually: Rank 2 (Left), Rank 1 (Center Elevated), Rank 3 (Right)
    podium_row = ft.Row(
        controls=[
            make_podium_card(top_3[1], 2, "#C0C0C0", 220) if len(top_3) > 1 else ft.Container(),
            make_podium_card(top_3[0], 1, "#FFD700", 250, is_first=True) if len(top_3) > 0 else ft.Container(),
            make_podium_card(top_3[2], 3, "#CD7F32", 200) if len(top_3) > 2 else ft.Container(),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.END,
        spacing=16,
    )

    # Ranks 4+ Data Table
    table_rows = []
    for ath in ranks_4_plus:
        is_current_user = ath["id"] == current_user_id
        row_bg = "#00F2FE15" if is_current_user else "#161B22"
        text_color = "#00F2FE" if is_current_user else "#F0F6FC"

        table_rows.append(
            ft.DataRow(
                color=row_bg,
                cells=[
                    ft.DataCell(
                        ft.Text(
                            f"#{ath['rank']}",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=text_color,
                        )
                    ),
                    ft.DataCell(
                        ft.Column(
                            controls=[
                                ft.Text(
                                    ath["name"],
                                    size=12,
                                    weight=ft.FontWeight.W_700,
                                    color=text_color,
                                ),
                                ft.Text(ath["title"], size=10, color="#8B949E"),
                            ],
                            spacing=1,
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            f"{ath['streak']}d",
                            size=12,
                            color="#F0F6FC",
                            weight=ft.FontWeight.W_600,
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            f"{ath['failure_reps']} reps",
                            size=12,
                            color="#EF4444",
                            weight=ft.FontWeight.W_600,
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            f"{ath['xp']:,} XP",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color="#00F2FE",
                        )
                    ),
                ],
            )
        )

    roster_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("RANK", size=10, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("ATHLETE & TITLE", size=10, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("STREAK", size=10, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("FAILURE", size=10, weight=ft.FontWeight.BOLD, color="#8B949E")),
            ft.DataColumn(ft.Text("TOTAL XP", size=10, weight=ft.FontWeight.BOLD, color="#8B949E")),
        ],
        rows=table_rows,
        heading_row_color="#161B22",
        data_row_min_height=48,
        data_row_max_height=52,
        horizontal_lines=ft.border.BorderSide(1, "#21262D"),
    )

    # Current User Highlight Banner
    user_standing = next((a for a in raw_athletes if a["id"] == current_user_id), None)
    user_banner = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.STARS_ROUNDED, color="#00F2FE", size=22),
                        ft.Text(
                            f"YOUR ARENA STANDING: #{user_standing['rank']} • Top 5% Worldwide",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color="#F0F6FC",
                        ) if user_standing else ft.Text("YOUR ARENA STANDING", size=12, color="#F0F6FC"),
                    ],
                    spacing=8,
                ),
                ft.Text(
                    f"{user_standing['xp']:,} Total XP This Cycle" if user_standing else "",
                    size=12,
                    weight=ft.FontWeight.W_800,
                    color="#00F2FE",
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=10),
        border_radius=10,
        bgcolor="#00F2FE15",
        border=ft.border.all(1, "#00F2FE44"),
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.icons.LEADERBOARD_ROUNDED, color="#00F2FE", size=24),
                                ft.Text(
                                    "WEEKLY ARENA LEADERBOARD",
                                    size=16,
                                    weight=ft.FontWeight.W_900,
                                    color="#F0F6FC",
                                    style=ft.TextStyle(letter_spacing=1.0),
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Text("Resets Sunday 23:59 UTC", size=11, color="#8B949E"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                user_banner,
                ft.Divider(height=1, color="#21262D"),
                ft.Text(
                    "TOP PERFORMERS PODIUM",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                    color="#8B949E",
                    style=ft.TextStyle(letter_spacing=1.0),
                ),
                podium_row,
                ft.Divider(height=1, color="#21262D"),
                ft.Text(
                    "ARENA ROSTER (RANKS 4 - 10)",
                    size=11,
                    weight=ft.FontWeight.BOLD,
                    color="#8B949E",
                    style=ft.TextStyle(letter_spacing=1.0),
                ),
                ft.Container(
                    content=roster_table,
                    alignment=ft.alignment.center_left,
                ),
            ],
            spacing=14,
        ),
        padding=20,
        border_radius=16,
        bgcolor="#161B22",
        border=ft.border.all(1, "#21262D"),
    )
