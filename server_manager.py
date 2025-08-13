import os
import socket
import subprocess
import time
from mcrcon import MCRcon
import glob
import platform
from mcommands import MCommands
import threading

class ServerManager:
    def __init__(self, rcon_host, rcon_port, rcon_password, server_bat=None, update_status_callback=None, status=0, error='None'):
        self.rcon_host = rcon_host
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password
        self.server_bat = server_bat
        self.update_status_callback = update_status_callback
        self.status = status  # 0 - остановлен, 1 - запущен, 2 - запуск, 3 - остановка, 4 - рестарт, 5 - ошибка
        self.error = error
        self.os_type = platform.system()

    def get_local_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def server_running(self):
        ports = [25565, 25575]
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                if sock.connect_ex((self.rcon_host, port)) == 0:
                    self.status = 1
                    break
        else:
            self.status = 0
        if self.update_status_callback:
            self.update_status_callback()

    def find_server_script(self):
        if self.os_type == "Windows":
            path_pattern = os.path.join("C:\\", os.getlogin(), "Minecraft*", "server", "start.bat")
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
