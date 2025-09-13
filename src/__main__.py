from nextcord.ext import commands
from loguru import logger
from . import config

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=config.INTENTS)


@bot.event
async def on_ready():
    logger.info(f"Bot started `{bot.user.name}`")

    try:
        bot.load_extension("moderation.ping")
    except Exception as exception:
        logger.error(f"Extension setup error: {exception}")
        exit()

    logger.info("Extensions loaded")

    await bot.change_presence(
        status=config.PRESENCE_STATUS, activity=config.PRESENCE_ACTIVITY
    )


def main():
    logger.info("Setting up...")

    if config.BOT_TOKEN is None:
        logger.error("Unable to fetch bot token from environment, exiting...")
        exit()

    logger.info("Token fetched, starting bot...")
    bot.run(config.BOT_TOKEN)
