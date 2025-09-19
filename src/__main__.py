"""
Главный файл с запуском бота с настройками предоставленными в конфиге.

Если токен из окружения не был подгружен - будет выведена ошибка и в
дальнейшем выход из программы (т.к невозможно дальше продолжать).

Все расширения (extensions или cogs) загружаются в ивенте `on_ready`,
добавление новых происходит вручную через модульное наименование.
"""

from nextcord.ext import commands
from loguru import logger
from .database import db_singleton, client
from . import config

import os

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=config.INTENTS)


@bot.event
async def on_ready():
    """Установка singleton для базы данных и инициализация таблиц"""
    db_singleton.initialize(client.SqliteClient, config.SQLITE_DATABASE_PATH)
    await db_singleton.get_client().init()

    try:
        """
        Расширения (extensions или cogs) используются для распределения кода на различные
        модульные файлы для структуризации проекта. При добавлении нового нужно обязательно
        вписать его ниже через `bot.load_extension("src.DIRECTORY.MODULE")`
        """
        bot.load_extension("src.cogs.moderation.ping")
        bot.load_extension("src.cogs.moderation.punishments")
    except Exception as exception:
        logger.error(f"Extension setup error: {exception}")
        exit()

    logger.debug("Extensions loaded")

    """Синхронизация слэш комманд и application комманд"""
    await bot.sync_all_application_commands()
    logger.debug("Application commands synced")

    logger.debug("Database initialized")

    await bot.change_presence(
        status=config.PRESENCE_STATUS, activity=config.PRESENCE_ACTIVITY
    )

    """Установка расширений с `on_ready()` слушателем"""
    from src.cogs import applications

    await applications.project_applications_setup(bot)

    logger.success(f"Bot started `{bot.user.name}`")


def main():
    # Логирование в специальный файл
    os.makedirs(config.LOGS_DIRECTORY, exist_ok=True)
    logger.add(
        f"{config.LOGS_DIRECTORY}/{{time:DD.MM.YYYY}}.log",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
    )

    logger.debug("Setting up...")

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

    logger.debug("Token fetched, starting bot...")
    bot.run(config.BOT_TOKEN, reconnect=True)
