import logging
import discord
import settings

import json as js

from discord import app_commands
from discord.ext import commands

_log = logging.getLogger(__name__)


class TemplateCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        _log.info(f"Loaded {self.__cog_name__}")

    @app_commands.command(name='say', description='Создает эмбед')
    @app_commands.guilds(discord.Object(settings.SERVER_ID))
    async def say(self, interaction: discord.Interaction, json: str):
        try:
            text: dict = js.loads(json)
        except js.JSONDecodeError as e:
            await interaction.response.send_message(f'Ошибка: {e}', ephemeral=True)
        await interaction.channel.send(embed=discord.Embed().from_dict(text))
        await interaction.response.send_message('Готово', ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(TemplateCog(bot))