import os


class SQLProvider:
    def __init__(self, file_path):
        self.scripts = {}  # инициализируем словарь
        # цикл по всем файлам во входной директории
        for file in os.listdir(file_path):
            _sql = open(f'{file_path}/{file}').read()
            # заносим sql-запрос в словарь, где ключ — это имя файла
            self.scripts[file] = _sql

    def get(self, file):
        _sql = self.scripts[file]
        return _sql