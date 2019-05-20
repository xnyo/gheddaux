import time
from signal import signal, SIGINT

from cogs.redacted import Redacted
from singletons.bot import Bot
from singletons.config import Config
from singletons.database import Database

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
                bot.add_cog(Redacted(bot))
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
