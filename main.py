import flet as ft
from server_manager import ServerManager
from mcommands import MCommands
from ui import ServerControlPanel, ServerStatePanel, ServerTimePanel
import asyncio

# ===========================
# Server Configuration
# ===========================
RCON_HOST = "127.0.0.1"  # RCON server IP address (localhost by default)
RCON_PORT = 25575  # RCON server port
RCON_PASSWORD = "777"  # RCON authentication password
# Path to server start script
SERVER_BAT = r"C:/Users/talaev/Documents/Minecraft_Spigot_Server/start.bat"


async def periodic_update(
    page: ft.Page,
    server_manager: ServerManager,
    mcommands: MCommands,
    control_panel: ServerControlPanel,
    server_state_panel: ServerStatePanel,
    server_time_panel: ServerTimePanel,
):
    """
    Periodically checks the server status and updates the control panel UI.

    Args:
        page (ft.Page): The main application page.
        server_manager (ServerManager): Instance handling server control commands.
        control_panel (ServerControlPanel): UI component for controlling the server.

    This coroutine runs in an infinite loop and:
        - Checks whether the server is running.
        - Updates the control panel state accordingly.
        - Refreshes the UI every 0.5 seconds.
    """
    while True:
        server_manager.server_running()
        server_ip = server_manager.get_local_ip()
        print(server_manager.status)
        # Обновляем UI панели управления
        control_panel.update_state(server_manager.status)

        # Обновляем панель состояния
        server_state_panel.update_state(
            server_manager.status, server_manager.error, server_ip
        )
        server_time_panel.update_state(server_manager.status)
        await asyncio.sleep(0.5)
        page.update()


async def main(page: ft.Page):
    """
    Main entry point for the Flet application.

    Args:
        page (ft.Page): The main Flet page instance provided by the framework.

    This function:
        - Initializes the UI layout.
        - Creates the server control panel with start/stop/restart buttons.
        - Registers event handlers for these buttons.
        - Starts a background task to periodically update the UI based on server status.
    """

    # Set basic application window properties
    page.title = "SrvOp"
    page.window_width = 500
    page.window_height = 500
    page.update()

    def ui_status_callback():
        page.update()

    # Initialize server manager
    server_manager = ServerManager(
        RCON_HOST,
        SERVER_BAT,
        update_status_callback=ui_status_callback,
    )

    server_manager.server_running()  # Check initial server status

    mcommands = MCommands(RCON_HOST, RCON_PASSWORD, RCON_PORT)

    # Event handlers for control panel buttons
    def on_start_click(e):
        """Triggered when the 'Start' button is clicked."""
        server_manager.start_server()
        page.update()

    def on_stop_click(e):
        """Triggered when the 'Stop' button is clicked."""
        mcommands.stop_server()

        server_manager.stop_server()
        page.update()

    def on_restart_click(e):
        """Triggered when the 'Restart' button is clicked."""
        server_manager.restart_server()
        page.update()

    # Create control panel UI component
    control_panel = ServerControlPanel(
        on_start=on_start_click, on_stop=on_stop_click, on_restart=on_restart_click
    )

    # Create server state panel with initial values
    server_state_panel = ServerStatePanel()

    server_time_panel = ServerTimePanel(page, mcommands)

    # Add control panel to the page
    page.add(
        ft.Row(
            [control_panel, server_state_panel, server_time_panel],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
    )

    # Background updater coroutine
    async def updater():
        await periodic_update(
            page,
            server_manager,
            mcommands,
            control_panel,
            server_state_panel,
            server_time_panel,
        )

    # Schedule background task for server status updates
    page.run_task(updater)


if __name__ == "__main__":
    # Launch the application using Flet
    ft.app(target=main)
