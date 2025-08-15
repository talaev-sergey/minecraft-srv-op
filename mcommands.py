from mcrcon import MCRcon


class MCommands:
    def __init__(self, rcon_host, rcon_password, rcon_port):
        """
        Инициализация с ServerManager.
        Подключение к RCON создаётся один раз.
        """
        try:
            self.rcon = MCRcon(host=rcon_host, password=rcon_password, port=rcon_port)
            self.rcon.connect()
        except Exception as e:
            print(f"Ошибка подключения к RCON: {e}")
            self.rcon = None

    def send_command(self, command: str) -> str:
        """
        Отправка команды на сервер через RCON.
        """
        if not self.rcon:
            print("RCON не подключен")
            return ""
        try:
            response = self.rcon.command(command)
            return response
        except Exception as e:
            print(f"Ошибка при выполнении команды '{command}': {e}")
            return ""

    def get_server_time(self) -> str:
        """
        Получение игрового времени на сервере и конвертация в 24-часовой формат.
        """
        response = self.send_command("time query daytime")
        if not response:
            return "00:00"
        try:
            # Извлекаем тики из ответа
            time_ticks = int(response.strip().split()[-1])
            # Конвертируем тики в минуты: 0 тик = 6:00
            total_minutes = (time_ticks / 1000 * 60 + 360) % 1440
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            return f"{hours:02d}:{minutes:02d}"
        except Exception as e:
            print(f"Ошибка конвертации времени: {e}")
            return "00:00"

    def set_server_time(self, hours, minutes):
        """
        Перевод реального времени (часы, минуты) в тики Minecraft.
        0 тик = 6:00, 24000 тик = 6:00 следующего дня.
        """
        total_minutes = (hours * 60 + minutes - 360) % 1440
        ticks = int(total_minutes / 60 * 1000)
        responce = self.send_command(f"time set {str (ticks)}")

    def do_day_light_cycle(self, value: str):
        responce = self.send_command(f"gamerule doDaylightCycle {value.lower()}")

    def get_do_day_light_cycle(self) -> bool:
        result = self.send_command("gamerule doDaylightCycle")
        if result == "Gamerule doDaylightCycle is currently set to: true":
            return True
        if result == "Gamerule doDaylightCycle is currently set to: false":
            return False

    def stop_server(self):
        try:
            self.send_command("stop")
        except:
            print("Ошибка отправки команды stop")

    def close(self):
        """
        Закрытие RCON-подключения.
        """
        if self.rcon:
            try:
                self.rcon.disconnect()
            except:
                pass
            self.rcon = None
