import flet as ft


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
                    spacing=10
                ),
                padding=ft.Padding(
                    top=8,
                    bottom=8,
                    left=20,
                    right=20
                )
            )

        )

    def update_state(self, status_server : int, error: str | None, ip: str | None):
        match status_server:
            case 0:
                self.progress_ring.value = 0
                self.progress_ring.visible = False
                self.state_server.value = "Сервер не запущен"
            case 1:
                self.progress_ring.value = 100
                self.progress_ring.visible = True
                self.state_server.value = ip
            case 2:
                self.progress_ring.value = None
                self.progress_ring.visible = True
                self.state_server.value = "Запуск сервера..."
            case 3:
                self.progress_ring.value = None
                self.progress_ring.visible = True
                self.state_server.value = "Остановка сервера..."
            case 4:
                self.progress_ring.value = None
                self.progress_ring.visible = True
                self.state_server.value = "Перезапуск сервера..."
            case 5:
                self.progress_ring.value = 0
                self.progress_ring.visible = False
                self.state_server.value = error

        self.update()
