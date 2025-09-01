import flet as ft
from server_status import ServerStatus


class ServerStatePanel(ft.Card):
    def __init__(self):
        self.progress_ring = ft.ProgressRing(
            width=16,
            height=16,
            stroke_width=2,
            color=ft.Colors.GREEN,
        )
        self.state_server = ft.Text(
            value="",
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

    def update_state(self, status, ip: str | None):
        match status:
            case ServerStatus.OFFLINE:
                self.progress_ring.value = 0
                self.progress_ring.visible = False
                self.state_server.value = ServerStatus.OFFLINE.value
            case ServerStatus.ONLINE:
                self.progress_ring.value = 100
                self.progress_ring.visible = True
                self.state_server.value = ip
            case ServerStatus.STARTING:
                self.progress_ring.value = None
                self.progress_ring.visible = True
                self.state_server.value = ServerStatus.STARTING.value
            case ServerStatus.STOPING:
                self.progress_ring.value = None
                self.progress_ring.visible = True
                self.state_server.value = ServerStatus.STOPING.value
            case ServerStatus.RESTATING:
                self.progress_ring.value = None
                self.progress_ring.visible = True
                self.state_server.value = ServerStatus.RESTATING.value
            # HACK: Если необходимо, то реализовать
            # case ServerStatus.ERROR:
            #     self.progress_ring.value = None
            #     self.progress_ring.visible = True
            #     self.progress_ring.color = ft.Colors.RED
            #     self.state_server.value = ""
            # case ServerStatus.RCON_CLOSED:
            #     self.progress_ring.value = 100
            #     self.progress_ring.visible = True
            #     self.progress_ring.color = ft.Colors.RED
            #     self.state_server.value = ""
            #
        self.update()
