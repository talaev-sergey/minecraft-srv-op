import flet as ft


def handle_change(e):
    selected_time = e.control.value
    if selected_time:
        e.control.page.snack_bar = ft.SnackBar(
            ft.Text(f"Время выбрано: {selected_time.strftime('%H:%M:%S')}"))
        e.control.page.snack_bar.open = True
        e.control.page.update()


def handle_dismissal(e):
    print("Диалог выбора времени закрыт")


class ServerTimePanel(ft.Row):
    def __init__(self, page: ft.Page):
        self.page = page

        self.time_picker = ft.TimePicker(
            on_change=handle_change,
            on_dismiss=handle_dismissal,
        )
        self.page.overlay.append(self.time_picker)

        self.elevated_time = ft.ElevatedButton(
            text="Текущее время",
            icon=ft.Icons.ACCESS_TIME,
            width=200,
            height=40,
            on_click=self.open_time_picker
        )

        super().__init__(
            controls=[self.elevated_time],
            spacing=10
        )

    def open_time_picker(self, e):
        self.time_picker.open = True
