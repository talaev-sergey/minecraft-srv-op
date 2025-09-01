from mcrcon import MCRcon
from ui.alert_window import AlertWindow


class MCommands:
    def __init__(self, rcon: MCRcon, alert_window: AlertWindow):
        self.rcon = rcon
        self.alert_window = alert_window

    def send_command(self, command: str) -> str:
        """
        Отправка команды на сервер через RCON.
        """
        try:
            with self.rcon as mcr:
                response = mcr.command(command)
                return response
        except Exception as e:
            self.alert_window.set_error(f"при выполнении команды '{command}': {e}")
            return ""

    def get_server_time(self) -> str:
        """
        Получение игрового времени на сервере и конвертация в 24-часовой формат.
        """
        response = self.send_command("time query daytime")

        try:
            # Извлекаем тики из ответа
            time_ticks = int(response.strip().split()[-1])
            # Конвертируем тики в минуты: 0 тик = 6:00
            total_minutes = (time_ticks / 1000 * 60 + 360) % 1440
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            return f"{hours:02d}:{minutes:02d}"
        except Exception as e:
            self.alert_window.set_error(f"конвертации времени: {e}")
            return "00:00"

    def set_server_time(self, hours, minutes):
        """
        Перевод реального времени (часы, минуты) в тики Minecraft.
        0 тик = 6:00, 24000 тик = 6:00 следующего дня.
        """
        total_minutes = (hours * 60 + minutes - 360) % 1440
        ticks = int(total_minutes / 60 * 1000)
        self.send_command(f"time set {str(ticks)}")

    def do_day_light_cycle(self, value: str):
        self.send_command(f"gamerule doDaylightCycle {value.lower()}")

    def get_do_day_light_cycle(self):
        result = self.send_command("gamerule doDaylightCycle")
        if result == "Gamerule doDaylightCycle is currently set to: true":
            return True
        if result == "Gamerule doDaylightCycle is currently set to: false":
            return False

    def stop_server(self):
        self.send_command("stop")

    def close(self):
        """
        Закрытие RCON-подключения.
        """
        if self.rcon:
            try:
                self.rcon.disconnect()
            except Exception as e:
                self.alert_window.set_error(f"при закрытии RCON-подключения: {e}")
            self.rcon = None
