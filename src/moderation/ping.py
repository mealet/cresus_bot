from .. import config
from .. import filters

from loguru import logger

import nextcord
from nextcord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", guild_ids=config.GUILD_IDS)
    @filters.has_any_role([config.MODERATION_ROLES])
    async def ping_handler(self, interaction: nextcord.Interaction):
        logger.debug(f"Ping call handled from {interaction.user.name}")

        await interaction.response.send_message(
            "Бот работает исправно!", ephemeral=True
        )


def setup(bot):
    bot.add_cog(Ping(bot))
