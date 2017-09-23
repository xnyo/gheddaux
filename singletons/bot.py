from discord.ext import commands

from utils.singleton import singleton


@singleton
class Bot(commands.Bot):
    pass
