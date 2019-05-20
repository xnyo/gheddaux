from decouple import config, Csv

from utils.singleton import singleton


@singleton
class Config:
    def __init__(self):
        self._config = {
            "BOT_TOKEN": config("BOT_TOKEN", default=""),
            "SERVER_IDS": config("SERVER_IDS", cast=Csv(int)),
            "LOG_CHANNEL_ID": config("LOG_CHANNEL_ID", cast=int),
            "WELCOME_CHANNEL_ID": config("WELCOME_CHANNEL_ID", cast=int, default=""),
            "DB_DSN": config("DB_DSN", default="Driver=SQLite3;Database=nazi.db")
        }

    def __getitem__(self, item):
        return self._config[item]