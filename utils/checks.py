from discord.ext import commands
from discord import Member


def is_admin(message):
    if type(message.author) is not Member:
        return False
    return message.author.permissions_in(message.channel).administrator


def admin_only():
    return commands.check(lambda ctx: is_admin(ctx.message))
