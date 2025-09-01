from enum import Enum


class ServerStatus(Enum):
    OFFLINE = "Сервер выключен"
    ONLINE = "Сервер работает. Подключение совершено."
    STARTING = "Запуск сервера..."
    STOPING = "Остановка сервера..."
    RESTATING = "Перезапуск сервера..."
    ERROR = "Ошибка:"
    RCON_CLOSED = "Невозможно подключится к серверу"
