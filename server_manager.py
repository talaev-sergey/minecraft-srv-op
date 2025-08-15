import os
import socket
import subprocess
import time
from enum import Enum
import glob
import platform


class StatusServer(Enum):
    OFFLINE = 0
    ONLINE = 1
    STARTING = 2
    STOPING = 3
    RESTATING = 4
    ERROR = 5
    RCON_CLOSED = 6


class ServerManager:
    def __init__(
        self,
        rcon_host,
        server_bat=None,
        update_status_callback=None,
        status=StatusServer.OFFLINE,
        error="None",
    ):
        self.rcon_host = rcon_host
        self.server_bat = server_bat
        self.update_status_callback = update_status_callback
        self.status = status
        self.error = error
        self.os_type = platform.system()

    def get_local_ip(self):
        try:
            # Создаем временное подключение, чтобы ОС выбрала реальный интерфейс
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # Подключение не отправляет данных
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def server_running(self):
        ports = [25565, 25575]

        def check_port(port: int) -> bool:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                return sock.connect_ex((self.rcon_host, port)) == 0

        port_65 = check_port(ports[0])
        port_75 = check_port(ports[1])

        if port_65 and port_75:
            self.status = StatusServer.ONLINE
        elif not port_65 and port_75:
            self.status = (
                StatusServer.STOPING
                if self.status != StatusServer.RESTATING
                else self.status
            )

        elif port_65 and not port_75:
            self.status = StatusServer.RCON_CLOSED
            self.error = "RCON соединение закрыто"
        else:
            self.status = StatusServer.OFFLINE

        if self.update_status_callback:
            self.update_status_callback()

    def find_server_script(self):
        if self.os_type == "Windows":
            path_pattern = os.path.join(
                "C:\\", os.getlogin(), "Minecraft*", "server", "start.bat"
            )
        else:  # Linux
            path_pattern = os.path.expanduser("~/.minecraft/Minecraft*/server/start.sh")
        scripts = glob.glob(path_pattern)
        return scripts[0] if scripts else None

    def start_server(self):
        try:
            self.status = 2
            script = self.server_bat or self.find_server_script()
            if not script:
                self.error = "Скрипт запуска сервера не найден"
                self.status = 5
                if self.update_status_callback:
                    self.update_status_callback()
                return
            subprocess.Popen([script], shell=True)
            # Ждем, пока сервер откроет порт
            for _ in range(30):
                time.sleep(1)
                self.server_running()
                if self.status == 1:
                    break
            else:
                self.error = "Сервер не запустился за 30 секунд"
                self.status = 5
        except Exception as e:
            self.error = str(e)
            self.status = 5
        if self.update_status_callback:
            self.update_status_callback()

    def stop_server(self):
        self.status = 3
        if self.update_status_callback:
            self.update_status_callback()

    def restart_server(self):
        try:
            self.status = 4
            self.stop_server()
            self.start_server()
        except Exception as e:
            self.error = str(e)
            self.status = 5
        if self.update_status_callback:
            self.update_status_callback()
