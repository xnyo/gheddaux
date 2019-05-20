import random
from datetime import datetime

import discord
from discord.ext import commands

from singletons.bot import Bot


class Reports(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message) -> None:
		if message.channel.id != Bot().reports_user_channel_id \
				or message.author == self.bot.user:
			return
		e = discord.Embed(
			title="New Player Report Received!",
			colour=discord.Colour.from_rgb(*(random.randint(0, 255) for _ in range(3))),
			timestamp=datetime.now()
		).set_thumbnail(
			url=message.author.avatar_url
		).add_field(
			name="Author", value=message.author.mention, inline=False
		).add_field(
			name="Report", value=message.content, inline=False
		)
		await self.bot.get_channel(Bot().reports_admin_channel_id).send(embed=e)
		await message.delete()
		await message.author.send(
			f"Hey there, {message.author}! Thank you for your report. "
			"It will be reviewed by the Ripple Community Managers soon!",
			embed=e
		)
