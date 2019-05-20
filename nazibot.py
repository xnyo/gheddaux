import time
from typing import Optional

import discord.ext
import discord
from signal import signal, SIGINT

from tinydb import Query

from singletons.bot import Bot
from singletons.config import Config
from singletons.database import Database
from utils import checks

# Initialize some variables for decorators
bot = Bot(
    command_prefix=";",
    allowed_server_ids=Config()["SERVER_IDS"],
    log_channel_id=Config()["LOG_CHANNEL_ID"]
).bot


@bot.event
async def on_ready() -> None:
    print("=> Logged in as {} [{}]. Ready!".format(bot.user.name, bot.user.id))
    await Bot().log("Started")


@bot.event
async def on_message(message: discord.Message) -> None:
    # Don't do anything in private messages or for messages sent in other servers
    if type(message.channel) is not discord.TextChannel \
            or message.channel.guild.id not in Bot().allowed_server_ids \
            or message.author == bot.user:
        return

    # Process commands
    try:
        await bot.process_commands(message)
    except discord.ext.commands.errors.CheckFailure:
        pass

    # Censor only for non-admins
    if message.author.bot or not checks.is_admin(message):
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


@bot.command(pass_context=True, no_pm=True)
@checks.admin_only()
async def censor(ctx, word: Optional[str] = None) -> None:
    # Syntax check
    if word is None:
        await ctx.message.channel.send("**Invalid syntax**. `!censor word`")
        return

    # Make sure the word is not already censored
    word = word.lower()
    async with Bot().censored_words_db() as db:
        db_word = db.search(Query().word == word)
    if db_word:
        await ctx.message.channel.send("**{}** is already censored!".format(word))
        return

    # Censor new word
    async with Bot().censored_words_db() as db:
        db.insert({"word": word})

    # Bot's reply
    await ctx.message.channel.send("**{}** is now censored!".format(word))


@bot.command(pass_context=True, no_pm=True)
@checks.admin_only()
async def uncensor(ctx, word: Optional[str] = None) -> None:
    # Syntax check
    if word is None:
        await ctx.message.channel.send("**Invalid syntax**. `!uncensor word`")
        return

    # Make sure the word is censored
    word = word.lower()
    async with Bot().censored_words_db() as db:
        db_word = db.search(Query().word == word)
    if not db_word:
        await ctx.message.channel.send("**{}** is not censored!".format(word))
        return

    # Uncensor word
    async with Bot().censored_words_db() as db:
        db.remove(Query().word == word)

    # Bot's reply
    await ctx.message.channel.send("**{}** isn't censored anymore!".format(word))


@bot.command(pass_context=True, no_pm=True)
@checks.admin_only()
async def censoredwords(ctx) -> None:
    async with Bot().censored_words_db() as db:
        results = db.all()
    await ctx.message.channel.send("**Censored words:** {}".format(", ".join(x["word"] for x in results)))

if __name__ == "__main__":
    try:
        print("""\033[92m                 _ _       _
         ___ ___ ___|_| |_ ___| |_
        |   | .'|- _| | . | . |  _|
        |_|_|__,|___|_|___|___|_|
          Nazi Bot - Made by Nyo\033[0m\n""")
        print("=> Logging in")
        signal(SIGINT, lambda s, f: bot.loop.stop())
        while True:
            try:
                bot.loop.run_until_complete(bot.start(Config()["BOT_TOKEN"]))
            except TimeoutError:
                print("[!] TimeoutError! Reconnecting...")
                time.sleep(1)
    except KeyboardInterrupt:
        print("=> Disposing bot")
        bot.loop.run_until_complete(bot.logout())
        bot.loop.run_until_complete(Database().dispose())
    finally:
        bot.loop.close()
        print("=> Bot stopped, goodbye!")
