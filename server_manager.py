import socket
import os
import platform
import subprocess
import threading
from ui.alert_window import AlertWindow
from server_status import ServerStatus
from mcrcon import MCRcon
import settings as st
from settings_field import SettingsField


class ServerManager:
    def __init__(
        self,
        rcon_host,
        rcon_password,
        rcon_port,
        alert_window=AlertWindow,
        update_status_callback=None,
    ):
        self.rcon_host = rcon_host
        self.rcon_password = rcon_password
        self.rcon_port = rcon_port
        self.mcrcon = MCRcon(self.rcon_host, self.rcon_password, self.rcon_port)
        self.update_status_callback = update_status_callback
        self.status = ServerStatus.OFFLINE
        self.alert_window = alert_window

    def get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            self.alert_window.set_error(
                f"получение ip компьютера:{e}. Переключение на локальный local_ip."
            )
            return "127.0.0.1"

    def _check_port(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            return sock.connect_ex((self.rcon_host, port)) == 0

    def _rcon_is_ok(self) -> bool:
        try:
            with MCRcon(self.rcon_host, self.rcon_password, self.rcon_port) as mcr:
                mcr.connect()
                return True
        except Exception:
            return False

    def update_server_status(self):
        ports = [25565, 25575]

        port_65_ok = self._check_port(ports[0])
        port_75_ok = self._check_port(ports[1])
        rcon_ok = self._rcon_is_ok()

        if port_65_ok and port_75_ok and rcon_ok:
            self.status = ServerStatus.ONLINE
        elif port_65_ok and port_75_ok and not rcon_ok:
            self.status = ServerStatus.STARTING
        elif not port_65_ok and port_75_ok:
            if self.status != ServerStatus.RESTATING:
                self.status = ServerStatus.STOPING
        elif port_65_ok and not port_75_ok:
            self.status = ServerStatus.RCON_CLOSED
        else:
            self.status = ServerStatus.OFFLINE

        if self.update_status_callback:
            self.update_status_callback()

    def get_mcrcon(self):
        return self.mcrcon

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def start_server(self):
        app_settings = st.Settings()
        script = app_settings.get(SettingsField.SERVER_START_SCRIPT.value)
        if not script:
            self.alert_window.set_error(
                "Скрипт для запуска сервера не указан!\nНажмите кнопку   Открыть папку с сервером и найдите файл со скриптом запуска сервера"
            )
            return
        if not os.path.isfile(script):
            self.alert_window.set_error(f"Скрипт не найден:\n{script}")
            return
        system = platform.system()

        def run():
            if system == "Windows" and script.endswith(".bat"):
                self.process = subprocess.Popen(
                    ["cmd.exe", "/c", script], cwd=os.path.dirname(script)
                )
            elif system == "Linux" and script.endswith(".sh"):
                self.process = subprocess.Popen(
                    ["bash", script], cwd=os.path.dirname(script)
                )
            else:
                self.alert_window.set_error(f"Неподдерживаемый скрипт!\n{script}")

        threading.Thread(target=run, daemon=True).start()

        if self.update_status_callback:
            self.update_status_callback()

    def stop_server(self):
        try:
            with self.mcrcon as mcr:
                responce = mcr.command("stop")
        except Exception as e:
            self.alert_window.set_error(f"при выполнении команды '{responce}': {e}")
        if self.process:
            try:
                self.process.wait(timeout=60)  # ждем до 30 секунд
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        if self.update_status_callback:
            self.update_status_callback()

    def restart_server(self):
        self.stop_server()
        self.start_server()
        if self.update_status_callback:
            self.update_status_callback()
