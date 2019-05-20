from typing import Optional

import discord
from discord.ext import commands
from tinydb import Query

from singletons.bot import Bot
from utils import checks


class Redacted(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.command(pass_context=True, no_pm=True)
	@checks.admin_only()
	async def censor(self, ctx, word: Optional[str] = None) -> None:
		# Syntax check
		if word is None:
			await ctx.send("**Invalid syntax**. `!censor word`")
			return

		# Make sure the word is not already censored
		word = word.lower()
		async with Bot().censored_words_db() as db:
			db_word = db.search(Query().word == word)
		if db_word:
			await ctx.send("**{}** is already censored!".format(word))
			return

		# Censor new word
		async with Bot().censored_words_db() as db:
			db.insert({"word": word})

		# Bot's reply
		await ctx.send("**{}** is now censored!".format(word))

	@commands.command(pass_context=True, no_pm=True)
	@checks.admin_only()
	async def uncensor(self, ctx, word: Optional[str] = None) -> None:
		# Syntax check
		if word is None:
			await ctx.send("**Invalid syntax**. `!uncensor word`")
			return

		# Make sure the word is censored
		word = word.lower()
		async with Bot().censored_words_db() as db:
			db_word = db.search(Query().word == word)
		if not db_word:
			await ctx.send("**{}** is not censored!".format(word))
			return

		# Uncensor word
		async with Bot().censored_words_db() as db:
			db.remove(Query().word == word)

		# Bot's reply
		await ctx.send("**{}** isn't censored anymore!".format(word))

	@commands.command(pass_context=True, no_pm=True)
	@checks.admin_only()
	async def censoredwords(self, ctx) -> None:
		async with Bot().censored_words_db() as db:
			results = db.all()
		await ctx.send("**Censored words:** {}".format(", ".join(x["word"] for x in results)))

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message) -> None:
		# Don't do anything in private messages or for messages sent in other servers
		if type(message.channel) is not discord.TextChannel \
				or message.channel.guild.id not in Bot().allowed_server_ids \
				or message.author == self.bot.user:
			return

		# Process commands
		# try:
		# 	await self.bot.process_commands(message)
		# except discord.ext.commands.errors.CheckFailure:
		# 	pass

		# Censor only for non-admins
		if not message.author.bot and not checks.is_admin(message):
			async with Bot().censored_words_db() as db:
				banned_words = set(x["word"] for x in db.all())
			message_words = message.content.lower()
			for banned_word in banned_words:
				if banned_word in message_words:
					await message.delete()
					print(
						f"=> Deleted message from {message.author.name} [{message.author.id}] ({message.content})"
					)
					await Bot().log(
						f"**Deleted message from {message.author.mention}:** "
						f"`{message.clean_content.replace('`', '')}`"
					)
