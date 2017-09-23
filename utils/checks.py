from discord.ext import commands


def is_admin(message):
    return message.author.server_permissions.administrator


def admin_only():
    return commands.check(lambda ctx: is_admin(ctx.message))
