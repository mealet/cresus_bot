from src import config, filters, utils
from src.database import db_singleton

import nextcord
import datetime

from nextcord.ext import commands
from loguru import logger

"""
Раздел комманд для наказаний со стороны модерации.
Пометка: user команды находятся в контекстном меню пользователя в пункте "Приложения".

User Команды:
    - Ban
      |-- Открывает модальное окно для бана пользователя.
      |-- После успешного бана высылает общедоступное сообщение с информацией.
      |-- Бан безвременный, снятие происходит вручную.

    - Kick
      |-- Открывает модальное окно для кика пользователя.
      |-- После успешного кика высылает общедоступное сообщение с информацией.
"""


class Punishments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.user_command(name="Ban", guild_ids=config.GUILD_IDS)
    @filters.has_any_role([config.MODERATION_ROLES])
    async def ban_application(
        self, interaction: nextcord.Interaction, user: nextcord.Member
    ):
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ Нельзя забанить самого себя!", ephemeral=True
            )
            return

        if user.bot:
            await interaction.response.send_message(
                "❌ Нельзя забанить бота!", ephemeral=True
            )
            return

        await interaction.response.send_modal(BanModal(user))

    @nextcord.user_command(name="Kick", guild_ids=config.GUILD_IDS)
    @filters.has_any_role([config.MODERATION_ROLES])
    async def kick_application(
        self, interaction: nextcord.Interaction, user: nextcord.Member
    ):
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ Нельзя выгнать самого себя!", ephemeral=True
            )
            return

        if user.bot:
            await interaction.response.send_message(
                "❌ Нельзя выгнать бота!", ephemeral=True
            )
            return

        await interaction.response.send_modal(BanModal(user))


def setup(bot):
    bot.add_cog(Punishments(bot))


"""
Модальные окна
"""


class BanModal(nextcord.ui.Modal):
    def __init__(self, target: nextcord.Member):
        super().__init__(
            title=f"Бан `{target.name} ({target.id})`",
            custom_id="moderation_ban_modal",
        )

        self.target = target

        self.reason = nextcord.ui.TextInput(
            label="Введите причину бана",
            custom_id="reason",
            placeholder="Нарушение правил чата",
            style=nextcord.TextInputStyle.short,
            required=True,
        )

        self.time = nextcord.ui.TextInput(
            label="Укажите время бана", custom_id="time", placeholder="30d, 3h, 12s"
        )

        self.add_item(self.reason)
        self.add_item(self.time)

    async def callback(self, interaction):
        # Embed плажка с информацией о бане
        embed_info = nextcord.Embed(
            colour=nextcord.Colour.red(), timestamp=datetime.datetime.now()
        )

        embed_info.add_field(
            name="Пользователь забанен",
            value=f"Пользователь: {self.target.mention}\nПричина: {self.reason.value}",
        )

        # Проверка на наличие аватарки (если нет - заменяем на свою)
        author_avatar_url = (
            "https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png"
            if interaction.user.avatar is None
            else interaction.user.avatar.url
        )

        banned_avatar_url = (
            "https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png"
            if self.target.avatar is None
            else self.target.avatar.url
        )

        embed_info.set_author(name=interaction.user.name, icon_url=author_avatar_url)
        embed_info.set_thumbnail(url=banned_avatar_url)

        try:
            ban_time = utils.parse_time_to_seconds(self.time.value)

            await self.target.ban(reason=self.reason.value)
            await db_singleton.get_client().ban_user(
                self.target.id, interaction.user.id, self.reason.value, ban_time
            )
            await interaction.response.send_message(embed=embed_info)

            logger.info(
                f'`{self.target.name} ({self.target.id}) was banned by `{interaction.user.name} ({interaction.user.id})` on "{self.time.value}": {self.reason.value}'
            )
        except Exception as exception:
            await interaction.response.send_message(
                f"❌ Произошла ошибка:\n```{exception}```", ephemeral=True
            )


class KickModal(nextcord.ui.Modal):
    def __init__(self, target: nextcord.Member):
        super().__init__(
            title=f"Кик `{target.name} ({target.nick})`",
            custom_id="moderation_kick_modal",
        )

        self.target = target

        self.reason = nextcord.ui.TextInput(
            label="Введите причину кика",
            custom_id="reason",
            placeholder="Нарушение правил чата",
            style=nextcord.TextInputStyle.short,
            required=True,
        )

        self.add_item(self.reason)

    async def callback(self, interaction):
        embed_info = nextcord.Embed(
            colour=nextcord.Colour.red(), timestamp=datetime.datetime.now()
        )

        embed_info.add_field(
            name="Пользователь выгнан с сервера",
            value=f"Пользователь: {self.target.mention}\nПричина: {self.reason.value}",
        )

        # Проверка на наличие аватарки (если нет - заменяем на свою)
        author_avatar_url = (
            "https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png"
            if interaction.user.avatar is None
            else interaction.user.avatar.url
        )

        banned_avatar_url = (
            "https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png"
            if self.target.avatar is None
            else self.target.avatar.url
        )

        embed_info.set_author(name=interaction.user.name, icon_url=author_avatar_url)
        embed_info.set_thumbnail(url=banned_avatar_url)

        try:
            await self.target.ban(reason=self.reason.value)
            await interaction.response.send_message(embed=embed_info)

            logger.info(
                f"`{self.target.name} ({self.target.id}) was kicked from server by `{interaction.user.name} ({interaction.user.id})`"
            )
        except Exception as exception:
            await interaction.response.send_message(
                f"❌ Произошла ошибка:\n```{exception}```", ephemeral=True
            )
