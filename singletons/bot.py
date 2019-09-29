import logging
import traceback
import sys
from typing import List

from aiotinydb import AIOTinyDB, AIOJSONStorage
from aiotinydb.middleware import CachingMiddleware
from discord.ext import commands

from utils.singleton import singleton


@singleton
class Bot:
    logger = logging.getLogger("bot")

    def __init__(
        self, *args,
        allowed_server_ids: List[int] = None, log_channel_id: int = None, welcome_channel_id: int = None,
        reports_user_channel_id: int = None, reports_admin_channel_id: int = None,
        db_file: str = None,
        **kwargs
    ):
        self.bot = commands.Bot(*args, **kwargs)
        self.allowed_server_ids = allowed_server_ids
        self.log_channel_id = log_channel_id
        self.welcome_channel_id = welcome_channel_id
        self.reports_user_channel_id = reports_user_channel_id
        self.reports_admin_channel_id = reports_admin_channel_id
        self.db_file = db_file

    def censored_words_db(self) -> AIOTinyDB:
        return AIOTinyDB(self.db_file, storage=CachingMiddleware(AIOJSONStorage))

    async def log(self, message: str) -> None:
        await (self.bot.get_channel(self.log_channel_id)).send(message)

    @property
    def reports_enabled(self) -> bool:
        return bool(self.reports_admin_channel_id) and bool(self.reports_user_channel_id)
