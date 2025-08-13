import socket
import subprocess
import time
from mcrcon import MCRcon
import queue


class ServerManager:
    def __init__(self, rcon_host, rcon_port, rcon_password, server_bat, update_status_callback=None, status=0, error='None'):
        self.rcon_host = rcon_host
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password
        self.server_bat = server_bat
        self.update_status_callback = update_status_callback
        self.status = status  # 0 - сервер не запущен, 1 - запущен, 2 - запуск, 3 - остановка, 4 - рестарт, 5 - ошибка
        self.error = error
        # Очередь для потокобезопасной передачи строк лога
        self.log_queue = queue.Queue()
        self.max_log_lines = 500  # максимум строк в окне лога

    def get_local_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def server_running(self, start_check=False, restart_check=False):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # 1 секунда ожидания
            try:
                result = sock.connect_ex((self.rcon_host, self.rcon_port))
                if result == 0:  # 0 = порт открыт
                    self.status = 1
                    start_check = False
                    restart_check = False
                else:
                    if start_check:
                        self.status = 2
                    elif restart_check:
                        self.status = 4
                    else:
                        self.status = 0   
            except socket.error:
                self.status = 5
                self.error = "Ошибка подключения к порту"
        if self.update_status_callback:
            self.update_status_callback()

    def start_server(self):
        try:
            self.status = 2
            process = subprocess.Popen(
                self.server_bat,
                shell=True,
                # creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            while self.status != 1:
                time.sleep(1)
                self.server_running(start_check=True)
        except Exception as e:
            self.error = "Ошибка запуска сервера"
            self.status = 5
        if self.update_status_callback:
            self.update_status_callback()
            
    
    def stop_server(self):
        try:
            self.status = 3
            # Пытаемся остановить через RCON
            try:
                with MCRcon(self.rcon_host, self.rcon_password, port=self.rcon_port) as mcr:
                    mcr.command("stop")
                    mcr.disconnect()
                    time.sleep(5)
                    self.status = 0
            except Exception:
             self.error = "Не удалось остановить через RCON, пробую завершить процесс"
        except Exception as e:
            self.error = "Ошибка остановки сервера"
            self.status = 5
        if self.update_status_callback:
            self.update_status_callback()

    def restart_server(self):
        try:
            self.status = 4
            self.stop_server()
            self.start_server()
        except Exception as e:
            self.error = "Ошибка перезапуска сервера"
            self.status = 5
        if self.update_status_callback:
            self.update_status_callback()
            
    def get_server_time(self):
        try:
            with MCRcon(self.rcon_host, self.rcon_password, port=self.rcon_port) as mcr:
                response = mcr.command("time query daytime")
                return response
        except Exception as e:
            self.error = "Ошибка получения времени сервера"
            return None
            
