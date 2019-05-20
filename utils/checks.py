from typing import Callable

from discord.ext import commands
import discord

from singletons.bot import Bot


def is_admin(message: discord.Message) -> bool:
    if type(message.author) is not discord.Member:
        return False
    return message.author.permissions_in(message.channel).administrator


def is_server_allowed(message: discord.Message) -> bool:
    return message.channel.guild.id in Bot().allowed_server_ids


def privileged() -> Callable:
    return commands.check(lambda ctx: is_server_allowed(ctx.message) and is_admin(ctx.message))


def allowed_servers() -> Callable:
    return commands.check(lambda ctx: is_server_allowed(ctx.message))
