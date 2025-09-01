import flet as ft
from server_status import ServerStatus
import settings as st
from settings_field import SettingsField


class ServerControlPanel(ft.Card):
    """
    A control panel UI component for managing a server with Start, Stop, and Restart buttons.

    This class extends Flet's `Card` widget and provides a horizontal layout of
    control buttons for server management. The button states can be dynamically updated
    based on the server's running status.

    Attributes:
        start_btn (ft.IconButton): Button to start the server.
        stop_btn (ft.IconButton): Button to stop the server.
        restart_btn (ft.IconButton): Button to restart the server.

    Methods:
        update_state(is_running: bool):
            Updates the enabled/disabled state of buttons depending on whether the server is running.
    """

    def __init__(self, on_file_dialog, on_start, on_stop, on_restart):
        """
        Initializes the server control panel with Start, Stop, and Restart buttons.

        Args:
            on_start (Callable): Callback function triggered when the Start button is clicked.
            on_stop (Callable): Callback function triggered when the Stop button is clicked.
            on_restart (Callable): Callback function triggered when the Restart button is clicked.
        """
        self.open_dialog_btn = ft.IconButton(
            icon=ft.Icons.FOLDER,
            icon_color=ft.Colors.BLUE_300,
            tooltip="Открыть папку с сервером",
            on_click=on_file_dialog,
        )

        # Create the "Start" button
        self.start_btn = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,  # Play icon
            icon_color=ft.Colors.GREEN_300,  # Green color for "Start"
            tooltip="Запустить сервер",
            on_click=self._on_start_click(on_start),  # Attach start callback
        )

        # Create the "Stop" button
        self.stop_btn = ft.IconButton(
            icon=ft.Icons.STOP,  # Stop icon
            icon_color=ft.Colors.RED_300,  # Red color for "Stop"
            tooltip="Остановить сервер",
            on_click=on_stop,  # Attach stop callback
        )

        # Create the "Restart" button
        self.restart_btn = ft.IconButton(
            icon=ft.Icons.REFRESH,  # Refresh icon
            icon_color=ft.Colors.ORANGE_300,  # Orange color for "Restart"
            tooltip="Перезапустить сервер",
            on_click=on_restart,  # Attach restart callback
        )

        # Call the parent `Card` constructor to wrap the buttons inside a row layout
        super().__init__(
            content=ft.Row(
                [self.open_dialog_btn, self.start_btn, self.stop_btn, self.restart_btn],
                alignment=ft.MainAxisAlignment.CENTER,  # Center alignment
                spacing=10,  # Space between buttons
            )
        )

        settings = st.Settings()
        find_field = settings.get(SettingsField.SERVER_START_SCRIPT.value)
        if find_field:
            self.start_btn.icon_color = ft.Colors.GREEN_300
            self.start_btn.disabled = False
        else:
            self.start_btn.icon_color = ft.Colors.GREY_400
            self.start_btn.disabled = True

        self.check_click = False  # Проверка нажатия кнопки старт

    def _on_start_click(self, on_start):
        def handler(e):
            self.start_btn.disabled = True
            self.start_btn.icon_color = ft.Colors.GREY_400
            self.update()
            on_start(e)
            self.check_click = True

        return handler

    def update_state(self, status):
        """
        Updates the button states based on the server's running status.

        Args:
            is_running (bool): True if the server is currently running, False otherwise.
        """

        if status == ServerStatus.OFFLINE:
            self.open_dialog_btn.icon_color = ft.Colors.BLUE_300
            self.open_dialog_btn.disabled = False

            if not self.check_click:  # Если не нажимали старт
                self.start_btn.icon_color = ft.Colors.GREEN_300
                self.start_btn.disabled = False

            self.stop_btn.icon_color = ft.Colors.GREY_400
            self.stop_btn.disabled = True

            self.restart_btn.icon_color = ft.Colors.GREY_400
            self.restart_btn.disabled = True

        elif status == ServerStatus.ONLINE:
            self.check_click = False  # Делаем сброс нажатия кнопки старт
            self.open_dialog_btn.icon_color = ft.Colors.GREY_400
            self.open_dialog_btn.disabled = True

            self.start_btn.icon_color = ft.Colors.GREY_400
            self.start_btn.disabled = True

            self.stop_btn.icon_color = ft.Colors.RED_300
            self.stop_btn.disabled = False

            self.restart_btn.icon_color = ft.Colors.ORANGE_300
            self.restart_btn.disabled = False

        elif status == ServerStatus.STARTING:
            self.open_dialog_btn.icon_color = ft.Colors.GREY_400
            self.open_dialog_btn.disabled = True

            self.start_btn.icon_color = ft.Colors.GREY_400
            self.start_btn.disabled = True

            self.stop_btn.icon_color = ft.Colors.GREY_400
            self.stop_btn.disabled = True

            self.restart_btn.icon_color = ft.Colors.GREY_400
            self.restart_btn.disabled = True

        elif status == ServerStatus.STOPING:
            self.open_dialog_btn.icon_color = ft.Colors.GREY_400
            self.open_dialog_btn.disabled = True

            self.start_btn.icon_color = ft.Colors.GREY_400
            self.start_btn.disabled = True

            self.stop_btn.icon_color = ft.Colors.GREY_400
            self.stop_btn.disabled = True

            self.restart_btn.icon_color = ft.Colors.GREY_400
            self.restart_btn.disabled = True

        elif status == ServerStatus.RESTATING:
            self.open_dialog_btn.icon_color = ft.Colors.GREY_400
            self.open_dialog_btn.disabled = True

            self.start_btn.icon_color = ft.Colors.GREY_400
            self.start_btn.disabled = True

            self.stop_btn.icon_color = ft.Colors.GREY_400
            self.stop_btn.disabled = True

            self.restart_btn.icon_color = ft.Colors.GREY_400
            self.restart_btn.disabled = True

        elif status == ServerStatus.ERROR:
            self.open_dialog_btn.icon_color = ft.Colors.GREY_400
            self.open_dialog_btn.disabled = True

            self.start_btn.icon_color = ft.Colors.GREEN_300
            self.start_btn.disabled = False

            self.stop_btn.icon_color = ft.Colors.GREY_400
            self.stop_btn.disabled = True

            self.restart_btn.icon_color = ft.Colors.GREY_400
            self.restart_btn.disabled = True

        elif status == ServerStatus.RCON_CLOSED:
            self.open_dialog_btn.icon_color = ft.Colors.GREY_400
            self.open_dialog_btn.disabled = True

            self.start_btn.icon_color = ft.Colors.GREEN_300
            self.start_btn.disabled = False

            self.stop_btn.icon_color = ft.Colors.GREY_400
            self.stop_btn.disabled = True

            self.restart_btn.icon_color = ft.Colors.GREY_400
            self.restart_btn.disabled = True
        self.update()
