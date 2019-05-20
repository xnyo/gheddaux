from aiotinydb import AIOTinyDB, AIOJSONStorage
from aiotinydb.middleware import CachingMiddleware
from discord.ext import commands

from utils.singleton import singleton


@singleton
class Bot(commands.Bot):
    def censored_words_db(self):
        return AIOTinyDB("censored_words.json", storage=CachingMiddleware(AIOJSONStorage))
