import flet as ft


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

    def __init__(self, on_start, on_stop, on_restart):
        """
        Initializes the server control panel with Start, Stop, and Restart buttons.

        Args:
            on_start (Callable): Callback function triggered when the Start button is clicked.
            on_stop (Callable): Callback function triggered when the Stop button is clicked.
            on_restart (Callable): Callback function triggered when the Restart button is clicked.
        """
        # Create the "Start" button
        self.start_btn = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,      # Play icon
            icon_color=ft.Colors.GREEN_300,  # Green color for "Start"
            on_click=on_start              # Attach start callback
        )

        # Create the "Stop" button
        self.stop_btn = ft.IconButton(
            icon=ft.Icons.STOP,            # Stop icon
            icon_color=ft.Colors.RED_300,   # Red color for "Stop"
            on_click=on_stop               # Attach stop callback
        )

        # Create the "Restart" button
        self.restart_btn = ft.IconButton(
            icon=ft.Icons.REFRESH,          # Refresh icon
            icon_color=ft.Colors.ORANGE_300,  # Orange color for "Restart"
            on_click=on_restart             # Attach restart callback
        )

        # Call the parent `Card` constructor to wrap the buttons inside a row layout
        super().__init__(
            content=ft.Row(
                [self.start_btn, self.stop_btn, self.restart_btn],
                alignment=ft.MainAxisAlignment.CENTER,  # Center alignment
                spacing=10  # Space between buttons
            )
        )

    def update_state(self, status_server: int):
        """
        Updates the button states based on the server's running status.

        Args:
            is_running (bool): True if the server is currently running, False otherwise.
        """
        match status_server:
            case 0:
                self.start_btn.icon_color = ft.Colors.GREEN_300
                self.start_btn.disabled = False
                self.stop_btn.icon_color = ft.Colors.GREY_400
                self.stop_btn.disabled = True
                self.restart_btn.icon_color = ft.Colors.GREY_400
                self.restart_btn.disabled = True
            case 1:
                self.start_btn.icon_color = ft.Colors.GREY_400
                self.start_btn.disabled = True
                self.stop_btn.icon_color = ft.Colors.RED_300
                self.stop_btn.disabled = False
                self.restart_btn.icon_color = ft.Colors.ORANGE_300
                self.restart_btn.disabled = False
            case 2:
                self.start_btn.icon_color = ft.Colors.GREY_400
                self.start_btn.disabled = True
                self.stop_btn.icon_color = ft.Colors.GREY_400
                self.stop_btn.disabled = True
                self.restart_btn.icon_color = ft.Colors.GREY_400
                self.restart_btn.disabled = True
            case 3:
                self.start_btn.icon_color = ft.Colors.GREY_400
                self.start_btn.disabled = True
                self.stop_btn.icon_color = ft.Colors.GREY_400
                self.stop_btn.disabled = True
                self.restart_btn.icon_color = ft.Colors.GREY_400
                self.restart_btn.disabled = True
            case 4:
                self.start_btn.icon_color = ft.Colors.GREY_400
                self.start_btn.disabled = True
                self.stop_btn.icon_color = ft.Colors.GREY_400
                self.stop_btn.disabled = True
                self.restart_btn.icon_color = ft.Colors.GREY_400
                self.restart_btn.disabled = True
            case 5:
                self.start_btn.icon_color = ft.Colors.GREEN_300
                self.start_btn.disabled = False
                self.stop_btn.icon_color = ft.Colors.GREY_400
                self.stop_btn.disabled = True
                self.restart_btn.icon_color = ft.Colors.GREY_400
                self.restart_btn.disabled = True

        self.update()
