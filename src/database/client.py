from abc import ABC, abstractmethod
from loguru import logger

import aiosqlite
import datetime

"""
В данном модуле распологаются доступные для выбора клиенты работы с базой даннных.
Чтобы создать новый - создайте подкласс от DatabaseClient и замените в инициализации на свой клиент.
"""


class DatabaseClient(ABC):
    @abstractmethod
    async def init() -> None:
        """Инициализация клиента и создание полей для работы"""
        pass

    @abstractmethod
    async def ban_user(
        self, user_id: int, moderator_id: int, reason: str, seconds: int
    ) -> None:
        """Бан пользователя на определенное время в секундах"""

    @abstractmethod
    async def unban_user(self, user_id: int) -> int | None:
        """Преждевременный разбан пользователя"""
        """Вовзаращает ID пользователя если бан существует, иначе - None"""

    @abstractmethod
    async def update_bans(self) -> list[int]:
        """Обновление состояний и проверка банов (разбан если уже прошёл)"""
        """Вовзаращает список ID пользователей которые должны быть разбанены"""


# Async Sqlite Client
class SqliteClient(DatabaseClient):
    def __init__(self, path: str):
        self.path = path

    async def init(self) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS bans (
                user_id INTEGER PRIMARY KEY,
                moderator_id INTEGER,
                reason TEXT,
                datetime INT,
                until INT
            )
            """)
            await db.commit()

    async def ban_user(
        self, user_id: int, moderator_id: int, reason: str, seconds: int
    ) -> None:
        async with aiosqlite.connect(self.path) as db:
            ban_datetime = int(datetime.datetime.now().timestamp())

            await db.execute(
                "INSERT INTO `bans` (user_id, moderator_id, reason, datetime, until) VALUES (?, ?, ?, ?, ?)",
                (user_id, moderator_id, reason, ban_datetime, ban_datetime + seconds),
            )

            await db.commit()

    async def unban_user(self, user_id: int) -> int | None:
        async with aiosqlite.connect(self.path) as db:
            async with db.execute(
                "SELECT 1 FROM `bans` WHERE user_id = ?", (user_id)
            ) as cursor:
                exists = await cursor.fetchone()

        if exists:
            await db.execute("DELETE FROM `bans` WHERE user_id = ?", (user_id))
            await db.commit()
            return user_id

        return None

    async def update_bans(self) -> list[int]:
        outdated_ids = []

        try:
            async with aiosqlite.connect(self.path) as db:
                db.row_factory = aiosqlite.Row
                current_timestamp = int(datetime.datetime.now().timestamp())

                async with db.execute(
                    "SELECT * FROM `bans` WHERE ? >= until", (current_timestamp)
                ) as cursor:
                    outdated_records = await cursor.fetchall()

                outdated_ids = [record["user_id"] for record in outdated_records]

                if outdated_ids:
                    placeholders = ",".join("?" * len(outdated_ids))

                    await db.execute(
                        f"DELETE FROM bans WHERE user_id IN ({placeholders})",
                        outdated_ids,
                    )
                    await db.commit()

        except aiosqlite.Error as error:
            logger.error(f"Sqlite client error: {error}")
        except Exception as exception:
            logger.error(f"Exception int Sqlite client: {exception}")

        return outdated_ids
