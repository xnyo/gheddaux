import asyncio
import time

from discord.ext import commands
from signal import signal, SIGINT

from singletons.bot import Bot
from singletons.config import Config
from singletons.database import Database
from singletons.words_cache import WordsCache
from utils import checks


async def connect_db():
    print("=> Connecting to database")

    # Connect to database and create table if needed
    await Database().connect(Config()["DB_DSN"], loop=asyncio.get_event_loop())
    await Database().execute("""
CREATE TABLE IF NOT EXISTS `banned_words` (
    `id`	INTEGER PRIMARY KEY AUTOINCREMENT,
    `word`	TEXT UNIQUE
);""")

    # Load forbidden words
    await WordsCache().reload()

# Initialize some variables for decorators
bot = Bot(command_prefix=";")


@bot.event
async def on_ready():
    print("=> Logged in as {} [{}]. Ready!".format(bot.user.name, bot.user.id))


@bot.event
async def on_message(message):
    # Don't do anything in private messages
    if message.server is None:
        return

    # Process commands
    try:
        await bot.process_commands(message)
    except commands.errors.CheckFailure:
        pass

    # Censor only for non-admins
    if not checks.is_admin(message):
        banned_words = WordsCache()
        message_words = message.content.lower()
        for banned_word in banned_words:
            if banned_word in message_words:
                await bot.delete_message(message)
                print(
                    "=> Deleted message from {} [{}] ({})".format(message.author.name, message.author.id, message.content)
                )


@bot.command(pass_context=True, no_pm=True)
@checks.admin_only()
async def censor(ctx, word=None):
    # Syntax check
    if word is None:
        await bot.say("**Invalid syntax**. `!censor word`")
        return

    # Make sure the word is not already censored
    word = word.lower()
    if word in WordsCache():
        await bot.say("**{}** is already censored!".format(word))
        return

    # Censor new word and reload cache
    await Database().execute("INSERT INTO banned_words (word) VALUES (?)", [word])
    await WordsCache().reload()

    # Bot's reply
    await bot.say("**{}** is now censored!".format(word))


@bot.command(pass_context=True, no_pm=True)
@checks.admin_only()
async def uncensor(ctx, word=None):
    # Syntax check
    if word is None:
        await bot.say("**Invalid syntax**. `!uncensor word`")
        return

    # Make sure the word is censored
    word = word.lower()
    if word not in WordsCache():
        await bot.say("**{}** is not censored!".format(word))
        return

    # Censor new word and reload cache
    await Database().execute("DELETE FROM banned_words WHERE word = ? LIMIT 1", [word])
    await WordsCache().reload()

    # Bot's reply
    await bot.say("**{}** isn't censored anymore!".format(word))


@bot.command(pass_context=True, no_pm=True)
@checks.admin_only()
async def censoredwords(ctx, word=None):
    await bot.say("**Censored words:** {}".format(", ".join(WordsCache())))

try:
    print("""\033[92m                 _ _       _   
     ___ ___ ___|_| |_ ___| |_ 
    |   | .'|- _| | . | . |  _|
    |_|_|__,|___|_|___|___|_|  
      Nazi Bot - Made by Nyo\033[0m\n""")
    print("=> Logging in")
    bot.loop.run_until_complete(connect_db())
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
