import json
import os


class Settings:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self._data = {}
        self.load()

    def load(self):
        """Загрузка настроек из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except json.JSONDecodeError:
                self._data = {}
        else:
            self._data = {}

    def save(self):
        """Сохранение настроек в файл"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get(self, key, default=None):
        """Получение значения по ключу"""
        return self._data.get(key, default)

    def set(self, key, value):
        """Установка значения"""
        self._data[key] = value
        self.save()

    def remove(self, key):
        """Удаление ключа"""
        if key in self._data:
            del self._data[key]
            self.save()

    def all(self):
        """Возвращает весь словарь настроек"""
        return self._data
