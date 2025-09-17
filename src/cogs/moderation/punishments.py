from src import config, filters, utils
from src.database import db_singleton

import nextcord
import datetime

from nextcord.ext import commands, tasks
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

        # Tasks
        self.check_bans.start()

    @nextcord.user_command(name="Ban", guild_ids=[config.GUILD_ID])
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

    @nextcord.slash_command(name="ban", guild_ids=[config.GUILD_ID])
    @filters.has_any_role([config.MODERATION_ROLES])
    async def ban_handler(self, interaction: nextcord.Interaction, user: nextcord.User):
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

    @nextcord.slash_command(name="unban", guild_ids=[config.GUILD_ID])
    @filters.has_any_role([config.MODERATION_ROLES])
    async def unban_handler(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.User = nextcord.SlashOption(
            name="пользователь",
            description="Укажите ID или упомяните пользователя",
            required=True,
        ),
    ):
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❌ Нельзя изменять состояние бана для себя!", ephemeral=True
            )
            return

        guild = interaction.guild
        unbanned_user = await db_singleton.get_client().unban_user(user_id=user.id)

        if unbanned_user is None:
            ban_entries = [entry async for entry in guild.bans()]
            if any(ban.user.id == user.id for ban in ban_entries):
                await interaction.response.send_message(
                    "❌ Пользователь не находится в бане!", ephemeral=True
                )
                return

        await guild.unban(user)
        await interaction.response.send_message(
            f"✅ Пользователь {user.mention} был разбанен на данном сервере!",
            ephemeral=True,
        )

    @nextcord.user_command(name="Kick", guild_ids=[config.GUILD_ID])
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

    # Tasks
    @tasks.loop(minutes=0.5)
    async def check_bans(self):
        guild = self.bot.get_guild(config.GUILD_ID)
        unban_users_ids = await db_singleton.get_client().update_bans()

        for user_id in unban_users_ids:
            discord_user = await self.bot.fetch_user(user_id)

            try:
                logger.info(
                    f"User's `{discord_user.name} ({discord_user.id})` ban expired"
                )
                await guild.unban(discord_user)
            except Exception as exception:
                logger.error(
                    f"Unban of `{discord_user.name} ({discord_user.id})` threw an exception: {exception}"
                )

        return

    @check_bans.before_loop
    async def before_check_bans(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Punishments(bot))


"""
Модальные окна
"""


class BanModal(nextcord.ui.Modal):
    def __init__(self, target: nextcord.Member):
        super().__init__(
            title=f"Бан `{target.name}`",
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

        self.dm_message = nextcord.ui.TextInput(
            label="Сообщение пользователю (в личные сообщения)",
            custom_id="dm_message",
            placeholder="Можно оставить пустым",
            style=nextcord.TextInputStyle.paragraph,
            required=False,
        )

        self.add_item(self.reason)
        self.add_item(self.time)
        self.add_item(self.dm_message)

    async def callback(self, interaction):
        ban_timestamp = datetime.datetime.now()

        # Сообщение пользователю о бане
        dm_embed = nextcord.Embed(
            title=f'Вы забанены на сервере "{interaction.guild.name}"',
            colour=nextcord.Colour.red(),
            timestamp=ban_timestamp,
        )

        dm_embed.add_field(
            name="Информация",
            value=f'Вы были временно заблокированы на сервере "{interaction.guild.name}" по решению модерации. Если вы несогласны с данным решением - пожалуйста обратитесь к руководству сервера.\n - **Модератор:** {interaction.user.mention}\n - **Срок:** {self.time.value}\n - **Причина:** {self.reason.value}',
            inline=False,
        )

        if self.dm_message.value:
            dm_embed.add_field(
                name=f"Сообщение от модератора `{interaction.user.name}`",
                value=f"```\n{self.dm_message.value}\n```",
                inline=False,
            )

        try:
            await self.target.send(embed=dm_embed)
        except Exception as exception:
            logger.warning(
                f"Unable to send ban message to `{self.target.name} ({self.target.id})`: {exception}"
            )

        # Сообщение в чат о бане
        embed_info = nextcord.Embed(
            colour=nextcord.Colour.red(), timestamp=ban_timestamp
        )

        embed_info.add_field(
            name="Пользователь временно заблокирован",
            value=f" - **Пользователь:** {self.target.mention}\n - **Срок:** {self.time.value}\n - **Причина:** {self.reason.value}",
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
            title=f"Кик `{target.name}`",
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
