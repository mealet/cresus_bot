from src import config, filters

import nextcord
from nextcord.ext import commands
from loguru import logger


"""
Классический пинговщик для проверки состояния и работоспособности бота.

Команды:
    * /ping
      |-- Стандартная команда, которая возвращает эфемеральное (видно только пользователю) сообщение о работоспособности бота.
      |-- Доступно для модерационных ролей (config.MODERATION_ROLES)
"""


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", guild_ids=[config.GUILD_ID])
    @filters.has_any_role([config.MODERATION_ROLES])
    async def ping_handler(self, interaction: nextcord.Interaction):
        latency = round(interaction.client.latency * 1000)
        status = ""
        color = nextcord.Color.default()

        if latency < 100:
            color = nextcord.Color.green()
            status = "✅ Отличное соединение"
        elif latency < 200:
            color = nextcord.Color.orange()
            status = "⚠️ Нормальное соединение"
        else:
            color = nextcord.Color.red()
            status = "❗ Высокая задержка"

        embed = nextcord.Embed(title="😴 Статус бота", color=color)

        embed.add_field(name="Задержка", value=f"{latency} мс", inline=False)
        embed.add_field(name="Статус", value=status, inline=False)

        logger.info(
            f"`{interaction.user.name} ({interaction.user.id})` called `/ping`: {latency} ms"
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Ping(bot))
