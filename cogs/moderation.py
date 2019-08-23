import discord
from discord.ext import commands
from singletons.bot import Bot

from utils import checks


class Moderation(commands.Cog):
	@commands.command()
	@checks.privileged()
	async def isin(self, ctx, user_id: int) -> None:
		"""
		Checks if '<user_id>' is in the current Discord guild.
		"""

		if ctx.message.guild.get_member(user_id) is None:
			await ctx.send("No. The specified user is not in this guild.")
		await ctx.send(f"Yes. Username: `{u.name}`")

	@commands.command()
	@checks.privileged()
	async def prune(self, ctx, how_many: int) -> None:
		"""
		Deletes '<x>' messages in the current channel.
		"""

		if how_many > 50:
			await ctx.send("You can delete up to 50 messages")
			return
		async for message in ctx.channel.history(limit=how_many):
			await message.delete()

	@commands.command()
	@checks.privileged()
	async def pruneu(self, ctx, member: discord.User, how_many: int) -> None:
		"""
		Deletes '<x>' messages sent by '<@user>' in the current channel.
		"""

		if how_many > 50:
			await ctx.send("You can delete up to 50 messages")
			return
		c = 0
		async for message in ctx.channel.history(limit=2 * how_many):
			if c >= how_many or message.author != member:
				continue
			await message.delete()
			c += 1
