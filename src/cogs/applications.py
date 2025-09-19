from src import config

import nextcord
import datetime

from nextcord.ext import commands
from loguru import logger

"""
Модуль для обработки заявок от пользователей
"""


"""
===================================

Заявки на вступление и на помощника

===================================
"""


async def project_applications_setup(bot: nextcord.Client):
    EMBED_TITLE = "Заявки на проект"
    EMBED_IMAGE = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExeGM4NnNsb3Byb3Q2OTI1bnltaDE2MWl6N3c4ZDJrcXdkNjd4c3M5eSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tEGtwTQLfUsf7bsS0K/giphy.gif"

    FIELD_TITLE = "Информация"
    FIELD_INFO = """
Здесь вы можете подать заявки для участия в жизни проекта.
Чтобы это сделать - нажмите на одну из кнопок ниже и заполните форму.
    """

    guild = bot.get_guild(config.GUILD_ID)
    applications_channel = nextcord.utils.get(
        guild.channels, id=config.PROJECT_APPLICATIONS_CHANNEL
    )

    applications_embed = nextcord.Embed(
        title=EMBED_TITLE,
        colour=nextcord.Colour.blue(),
    )
    applications_embed.add_field(name=FIELD_TITLE, value=FIELD_INFO, inline=False)
    applications_embed.set_image(url=EMBED_IMAGE)

    applications_view = nextcord.ui.View(timeout=0)
    applications_view.add_item(ParticipationButton())
    applications_view.add_item(HelperButton())

    await applications_channel.purge()
    await applications_channel.send(embed=applications_embed, view=applications_view)

    logger.debug(f"Applications embed form was sent to `{applications_channel.name}`")


# Кнопки


class ParticipationButton(nextcord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Заявка на вступление",
            style=nextcord.ButtonStyle.green,
            custom_id="participation_button",
        )

    async def callback(self, interaction):
        await interaction.response.send_modal(ParticipationModal())


class HelperButton(nextcord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Заявка на помощника",
            style=nextcord.ButtonStyle.green,
            custom_id="helper_button",
        )

    async def callback(self, interaction):
        await interaction.response.send_modal(HelperModal())


# Модальные окна


class ParticipationModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Заявка на участие", custom_id="participation_modal")

        self.name = nextcord.ui.TextInput(
            label="Ваше имя",
            placeholder="Владимир",
            style=nextcord.TextInputStyle.short,
            required=True,
        )

        self.nickname = nextcord.ui.TextInput(
            label="Имя в игре",
            placeholder="minecraft_username",
            style=nextcord.TextInputStyle.short,
            required=True,
        )

        self.add_item(self.name)
        self.add_item(self.nickname)

    async def callback(self, interaction):
        guild = interaction.client.get_guild(config.GUILD_ID)
        reciever_channel = nextcord.utils.get(
            guild.channels, id=config.PROJECT_PARTICIPATION_RECIEVER
        )

        application_embed = nextcord.Embed(
            colour=nextcord.Colour.teal(), timestamp=datetime.datetime.now()
        )

        application_embed.add_field(
            name="Заявка на участие в проекте",
            value=f"- **Пользователь:** {interaction.user.mention}\n- **Имя:** {self.name.value}\n- **Имя в игре:** {self.nickname.value}",
        )

        author_avatar_url = (
            "https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png"
            if interaction.user.avatar is None
            else interaction.user.avatar.url
        )

        application_embed.set_author(
            name=interaction.user.name, icon_url=author_avatar_url
        )

        await reciever_channel.send(embed=application_embed)


class HelperModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Заявка на помощника", custom_id="helper_modal")

        self.name = nextcord.ui.TextInput(
            label="Ваше имя",
            placeholder="Владимир",
            style=nextcord.TextInputStyle.short,
            required=True,
        )

        self.age = nextcord.ui.TextInput(
            label="Ваш возраст",
            placeholder="123 лет",
            style=nextcord.TextInputStyle.short,
            required=True,
        )

        self.nickname = nextcord.ui.TextInput(
            label="Имя в игре",
            placeholder="minecraft_username",
            style=nextcord.TextInputStyle.short,
            required=True,
        )

        self.add_item(self.name)
        self.add_item(self.age)
        self.add_item(self.nickname)

    async def callback(self, interaction):
        guild = interaction.client.get_guild(config.GUILD_ID)
        reciever_channel = nextcord.utils.get(
            guild.channels, id=config.PROJECT_HELPER_RECIEVER
        )

        application_embed = nextcord.Embed(
            colour=nextcord.Colour.teal(), timestamp=datetime.datetime.now()
        )

        application_embed.add_field(
            name="Заявка на помощника",
            value=f"- **Пользователь:** {interaction.user.mention}\n- **Имя:** {self.name.value}\n- **Возраст:** {self.age.value}\n- **Имя в игре:** {self.nickname.value}",
        )

        author_avatar_url = (
            "https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png"
            if interaction.user.avatar is None
            else interaction.user.avatar.url
        )

        application_embed.set_author(
            name=interaction.user.name, icon_url=author_avatar_url
        )

        await reciever_channel.send(embed=application_embed)


"""
===================================
"""
