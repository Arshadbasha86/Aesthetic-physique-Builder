"""
Aesthetic Physique Builder - Numeric Keypad Modal Component
Relative Path: frontend_app/views/components/numeric_keypad_modal.py
Architectural Role: Specialized on-screen numeric keypad dialog for
"Until Failure" sets (e.g. Diamond Push-ups) allowing athletes to quickly
log actual reps completed in gym conditions without tiny keyboards.
"""

import flet as ft
from typing import Callable, Optional


class NumericKeypadModal:
    """
    On-screen athletic numeric entry keypad modal for failure sets.
    """
    def __init__(
        self,
        page: ft.Page,
        exercise_name: str,
        initial_reps: int = 15,
        on_confirm: Optional[Callable[[int], None]] = None
    ):
        self.page = page
        self.exercise_name = exercise_name
        self.current_value_str = str(initial_reps)
        self.on_confirm = on_confirm

        # Readout text display
        self.readout_text = ft.Text(
            value=self.current_value_str,
            size=44,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.LIGHT_BLUE_400,
            text_align=ft.TextAlign.CENTER,
        )

        self.dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#0F172A",
            surface_tint_color=ft.colors.TRANSPARENT,
            shape=ft.RoundedRectangleBorder(radius=20),
            title=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT, color=ft.colors.ORANGE_400, size=24),
                            ft.Text(
                                value="Log Failure Reps",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE,
                            ),
                        ],
                        spacing=8,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(
                        value=self.exercise_name,
                        size=13,
                        color=ft.colors.GREY_400,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            content=self._build_keypad_content(),
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton(
                            text="Cancel",
                            on_click=self._on_cancel,
                            style=ft.ButtonStyle(color=ft.colors.GREY_400),
                        ),
                        ft.ElevatedButton(
                            text="Confirm Reps",
                            icon=ft.icons.CHECK,
                            bgcolor=ft.colors.LIGHT_BLUE_600,
                            color=ft.colors.WHITE,
                            on_click=self._on_confirm_click,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

    def _build_keypad_content(self) -> ft.Container:
        """Constructs large touch buttons for fast gym tapping."""
        def make_key(digit: str):
            return ft.ElevatedButton(
                text=digit,
                width=64,
                height=52,
                bgcolor="#1E293B",
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD),
                ),
                on_click=lambda e: self._press_digit(digit),
            )

        quick_adjust_row = ft.Row(
            controls=[
                ft.OutlinedButton(text="-5", on_click=lambda e: self._adjust_value(-5)),
                ft.OutlinedButton(text="-1", on_click=lambda e: self._adjust_value(-1)),
                ft.OutlinedButton(text="+1", on_click=lambda e: self._adjust_value(1)),
                ft.OutlinedButton(text="+5", on_click=lambda e: self._adjust_value(5)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
        )

        keypad_rows = [
            ft.Row([make_key("1"), make_key("2"), make_key("3")], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Row([make_key("4"), make_key("5"), make_key("6")], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Row([make_key("7"), make_key("8"), make_key("9")], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.CLEAR_ALL,
                        icon_color=ft.colors.RED_400,
                        width=64,
                        height=52,
                        tooltip="Clear",
                        on_click=lambda e: self._clear_all(),
                    ),
                    make_key("0"),
                    ft.IconButton(
                        icon=ft.icons.BACKSPACE_OUTLINED,
                        icon_color=ft.colors.AMBER_400,
                        width=64,
                        height=52,
                        tooltip="Backspace",
                        on_click=lambda e: self._backspace(),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
        ]

        return ft.Container(
            width=280,
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                self.readout_text,
                                ft.Text("reps", size=16, color=ft.colors.GREY_400, weight=ft.FontWeight.W_500),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=6,
                        ),
                        bgcolor="#020617",
                        border=ft.border.all(1, "#334155"),
                        border_radius=12,
                        padding=ft.padding.symmetric(vertical=8),
                    ),
                    quick_adjust_row,
                    ft.Column(controls=keypad_rows, spacing=8),
                ],
                spacing=14,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def _press_digit(self, digit: str):
        if self.current_value_str == "0":
            self.current_value_str = digit
        elif len(self.current_value_str) < 3:
            self.current_value_str += digit
        self._update_display()

    def _backspace(self):
        if len(self.current_value_str) > 1:
            self.current_value_str = self.current_value_str[:-1]
        else:
            self.current_value_str = "0"
        self._update_display()

    def _clear_all(self):
        self.current_value_str = "0"
        self._update_display()

    def _adjust_value(self, delta: int):
        val = int(self.current_value_str or "0") + delta
        self.current_value_str = str(max(1, min(150, val)))
        self._update_display()

    def _update_display(self):
        self.readout_text.value = self.current_value_str
        self.page.update()

    def _on_confirm_click(self, e):
        reps = int(self.current_value_str or "15")
        self.dialog.open = False
        self.page.update()
        if self.on_confirm:
            self.on_confirm(reps)

    def _on_cancel(self, e):
        self.dialog.open = False
        self.page.update()

    def show(self):
        """Mounts and presents the modal on the active page."""
        self.dialog.open = True
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.page.update()
