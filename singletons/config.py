from decouple import config, Csv

from utils.singleton import singleton


@singleton
class Config:
    def __init__(self):
        self._config = {
            "BOT_TOKEN": config("BOT_TOKEN", default=""),
            "DB_DSN": config("DB_DSN", default="Driver=SQLite3;Database=nazi.db")
        }

    def __getitem__(self, item):
        return self._config[item]