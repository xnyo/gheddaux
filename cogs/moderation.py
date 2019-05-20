import asyncio

from discord.ext import commands

from utils import checks


class Moderation(commands.Cog):
	@commands.command()
	@checks.privileged()
	async def prune(self, ctx, how_many: int) -> None:
		log = await ctx.send(f"_💣ing {how_many} messages_")
		async for message in ctx.channel.history(limit=how_many, before=log):
			await message.delete()
		await log.edit(content="👌")
		await asyncio.sleep(2)
		await log.delete()
