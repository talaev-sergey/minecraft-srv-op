from datetime import timedelta
import flet as ft
from server_manager import StatusServer


class ServerTimePanel(ft.Card):
    def __init__(self, page: ft.Page, mcommands):
        self.page = page
        self.mcommands = mcommands

        self.time_picker = ft.TimePicker(
            on_change=self.handle_change,
            on_dismiss=self.handle_dismissal,
        )
        self.page.overlay.append(self.time_picker)

        self.elevated_time = ft.ElevatedButton(
            text="Текущее время",
            icon=ft.Icons.ACCESS_TIME,
            width=100,
            height=40,
            on_click=self.open_time_picker,
        )

        self.switch = ft.Switch(
            label="Остановить время",
            value=True if not self.mcommands.get_do_day_light_cycle() else False,
            on_change=self.toggle_daylight_cycle,
        )

        super().__init__(
            content=ft.Container(
                content=ft.Row(
                    [self.elevated_time, self.switch],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=ft.Padding(top=8, bottom=8, left=20, right=20),
                visible=False,
            )
        )

    def open_time_picker(self, e):
        self.time_picker.open = True

    def handle_change(self, e):
        selected_time = e.control.value  # datetime.time
        if selected_time:
            # Показываем SnackBar
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Время выбрано: {selected_time.strftime('%H:%M:%S')}")
            )
            self.page.snack_bar.open = True
            self.page.update()
            self.mcommands.set_server_time(selected_time.hour, selected_time.minute)

    def handle_dismissal(self, e):
        pass

    def toggle_daylight_cycle(self, e):
        value = "False" if e.control.value == True else "True"
        self.mcommands.do_day_light_cycle(value)

    def update_state(self, status):
        if status is StatusServer.ONLINE:
            self.content.visible = True
            self.elevated_time.text = self.mcommands.get_server_time()
        else:
            self.content.visible = False
        self.update()
