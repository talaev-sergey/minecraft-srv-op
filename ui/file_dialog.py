import flet as ft
import settings as st
from settings_field import SettingsField


class FileDialog(ft.FilePicker):
    def __init__(self, page: ft.Page):
        super().__init__(on_result=self.on_file_selected)
        self.page = page
        self.selected_file = "Файл не выбран"
        self.settings = st.Settings()

        page.overlay.append(self)

    def open_dialog(self):
        self.pick_files(
            allow_multiple=False,
            allowed_extensions=["bat", "sh"],
            dialog_title="Выберите файл",
        )

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.selected_file = e.files[0].path
            self.settings.set(
                SettingsField.SERVER_START_SCRIPT.value, self.selected_file
            )
