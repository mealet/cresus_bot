"""
Главный файл с запуском бота с настройками предоставленными в конфиге.

Если токен из окружения не был подгружен - будет выведена ошибка и в
дальнейшем выход из программы (т.к невозможно дальше продолжать).

Все расширения (extensions или cogs) загружаются в ивенте `on_ready`,
добавление новых происходит вручную через модульное наименование.
"""

from nextcord.ext import commands
from loguru import logger
from . import config

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=config.INTENTS)


@bot.event
async def on_ready():
    try:
        """
        Расширения (extensions или cogs) используются для распределения кода на различные
        модульные файлы для структуризации проекта. При добавлении нового нужно обязательно
        вписать его ниже через `bot.load_extension("src.DIRECTORY.MODULE")`
        """
        bot.load_extension("src.moderation.ping")
    except Exception as exception:
        logger.error(f"Extension setup error: {exception}")
        exit()

    logger.debug("Extensions loaded")

    await bot.sync_all_application_commands()
    logger.debug("Application commands synced")

    await bot.change_presence(
        status=config.PRESENCE_STATUS, activity=config.PRESENCE_ACTIVITY
    )

    logger.info(f"Bot started `{bot.user.name}`")


def main():
    logger.info("Setting up...")

    if config.BOT_TOKEN is None:
        """
        Если окружение не подгружает токен, проверьте пожалуйста файл `.env`! Он должен находиться
        в корне проекта, а также иметь следующий формат:
        ---------------------------
        CRESUS_BOT_TOKEN=токен
        ---------------------------

        Если не помогает, можете изменить путь до файла окружения в src/config.py,
        или же вручную добавить в окружение переменную (лишь временно):

        ---- На Windows ----
        setx CRESUS_BOT_TOKEN "токен"

        ---- На Linux/Unix/MacOS ----
        export CRESUS_BOT_TOKEN="токен"

        ---- В fish shell ----
        set -g -x CRESUS_BOT_TOKEN "токен"
        """

        logger.error("Unable to fetch bot token from environment, exiting...")
        exit()

    logger.info("Token fetched, starting bot...")
    bot.run(config.BOT_TOKEN, reconnect=True)
