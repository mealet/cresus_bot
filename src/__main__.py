from nextcord.ext import commands

from loguru import logger
from . import config

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX)


@bot.event
async def on_ready():
    logger.info(f"Bot started `{bot.user.name}`")

    await bot.change_presence(
        status=config.PRESENCE_STATUS, activity=config.PRESENCE_ACTIVITY
    )


def main():
    if config.BOT_TOKEN is None:
        logger.error("Unable to fetch bot token from environment, exiting...")
        quit()

    bot.run(config.BOT_TOKEN)
