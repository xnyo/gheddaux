from typing import List

from aiotinydb import AIOTinyDB, AIOJSONStorage
from aiotinydb.middleware import CachingMiddleware
from discord.ext import commands

from utils.singleton import singleton


@singleton
class Bot:
    def __init__(
        self, *args,
        allowed_server_ids: List[int] = None, log_channel_id: int = None, welcome_channel_id: int = None,
        **kwargs
    ):
        self.bot = commands.Bot(*args, **kwargs)
        self.allowed_server_ids = allowed_server_ids
        self.log_channel_id = log_channel_id
        self.welcome_channel_id = welcome_channel_id

    @staticmethod
    def censored_words_db() -> AIOTinyDB:
        return AIOTinyDB("censored_words.json", storage=CachingMiddleware(AIOJSONStorage))

    async def log(self, message: str) -> None:
        await (self.bot.get_channel(self.log_channel_id)).send(message)
