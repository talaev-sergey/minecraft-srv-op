import flet as ft
from server_status import ServerStatus


class AlertWindow:
    def __init__(self, page: ft.Page):
        self.page = page
        self.error = None
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            content=ft.Text("no text"),
            actions=[ft.TextButton("Ok", on_click=lambda e: self.on_click())],
        )

    def on_click(self):
        self.error = None
        self.close()

    def close(self):
        self.page.close(self.dlg_modal)

    def open(self):
        self.dlg_modal.content.value = f"{ServerStatus.ERROR} {self.error}"
        self.page.open(self.dlg_modal)

    def set_error(self, error: str):
        self.error = error

    def update_state(self):
        if self.error:
            self.open()
