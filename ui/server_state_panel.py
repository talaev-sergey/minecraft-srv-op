import flet as ft
from server_manager import StatusServer


class ServerStatePanel(ft.Card):
    def __init__(self):
        self.progress_ring = ft.ProgressRing(
            width=16,
            height=16,
            stroke_width=2,
            color=ft.Colors.GREEN,
        )
        self.state_server = ft.Text(
            value="127.0.0.1",
            color=ft.Colors.BLUE,
            size=16,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )
        super().__init__(
            content=ft.Container(
                content=ft.Row(
                    [self.progress_ring, self.state_server],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=ft.Padding(top=8, bottom=8, left=20, right=20),
            )
        )

    def update_state(self, status, error: str | None, ip: str | None):
        match status:
            case StatusServer.OFFLINE:
                self.progress_ring.value = 0
                self.progress_ring.visible = False
                self.state_server.value = "Сервер не запущен"
            case StatusServer.ONLINE:
                self.progress_ring.value = 100
                self.progress_ring.visible = True
                self.state_server.value = ip
            case StatusServer.STARTING:
                self.progress_ring.value = None
                self.progress_ring.visible = True
                self.state_server.value = "Запуск сервера..."
            case StatusServer.STOPING:
                self.progress_ring.value = None
                self.progress_ring.visible = True
                self.state_server.value = "Остановка сервера..."
            case StatusServer.RESTATING:
                self.progress_ring.value = None
                self.progress_ring.visible = True
                self.state_server.value = "Перезапуск сервера..."
            case StatusServer.ERROR:
                self.progress_ring.value = 0
                self.progress_ring.visible = False
                self.state_server.value = error
            case StatusServer.RCON_CLOSED:
                self.progress_ring.value = 0
                self.progress_ring.visible = False
                self.state_server.value = error

        self.update()
