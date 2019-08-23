import logging
import time
from signal import signal, SIGINT

from cogs.moderation import Moderation
from cogs.redacted import Redacted
from cogs.reports import Reports
from cogs.welcome import Welcome
from singletons.bot import Bot
from singletons.config import Config


if __name__ == "__main__":
    logging.getLogger("discord").setLevel(logging.ERROR)
    logging.basicConfig(level=logging.INFO)
    print("""\033[92m     _         _   _             
 ___| |_ ___ _| |_| |___ _ _ _ _ 
| . |   | -_| . | . | .'| | |_'_|
|_  |_|_|___|___|___|__,|___|_,_|
|___|                            
      Gheddaux - Made by Nyo\033[0m""")
    bot = Bot(
        command_prefix=";",
        allowed_server_ids=Config()["SERVER_IDS"],
        log_channel_id=Config()["LOG_CHANNEL_ID"],
        welcome_channel_id=Config()["WELCOME_CHANNEL_ID"],
        reports_user_channel_id=Config()["REPORTS_USER_CHANNEL_ID"],
        reports_admin_channel_id=Config()["REPORTS_ADMIN_CHANNEL_ID"],
    ).bot
    if Bot().welcome_channel_id:
        bot.add_cog(Welcome(bot))
    else:
        Bot().logger.warning("Welcome cog is disabled.")
    bot.add_cog(Redacted(bot))
    bot.add_cog(Moderation())
    if Bot().reports_enabled:
        bot.add_cog(Reports(bot))
    else:
        Bot().logger.warning("Reports cog is disabled.")

    try:
        Bot().logger.info("Starting bot")
        signal(SIGINT, lambda s, f: bot.loop.stop())
        while True:
            try:
                bot.loop.run_until_complete(bot.start(Config()["BOT_TOKEN"]))
            except TimeoutError:
                Bot().logger.warning("TimeoutError! Reconnecting in 1 second")
                time.sleep(1)
    except KeyboardInterrupt:
        Bot().logger.info("Disposing bot")
        bot.loop.run_until_complete(bot.logout())
    finally:
        bot.loop.close()
        Bot().logger.info("Bot stopped, goodbye!")
