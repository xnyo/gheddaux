import time
from signal import signal, SIGINT

from cogs.redacted import Redacted
from cogs.welcome import Welcome
from singletons.bot import Bot
from singletons.config import Config
from singletons.database import Database


if __name__ == "__main__":
    print("""\033[92m                 _ _       _
     ___ ___ ___|_| |_ ___| |_
    |   | .'|- _| | . | . |  _|
    |_|_|__,|___|_|___|___|_|
      Nazi Bot - Made by Nyo\033[0m\n""")
    bot = Bot(
        command_prefix=";",
        allowed_server_ids=Config()["SERVER_IDS"],
        log_channel_id=Config()["LOG_CHANNEL_ID"],
        welcome_channel_id=Config()["WELCOME_CHANNEL_ID"]
    ).bot
    if Bot().welcome_channel_id:
        bot.add_cog(Welcome())
    bot.add_cog(Redacted(bot))

    try:
        print("=> Starting bot")
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
