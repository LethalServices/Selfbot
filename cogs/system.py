from discord.ext import commands

from mod.desings import LethalLogo
from mod.error import CustomLogger
from mod.db import DatabaseManager

import discord, logging

class SystemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logo = LethalLogo()
        self.custom_logger = CustomLogger('System', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    @commands.command()
    async def cls(self, ctx):
        self.logo.main_logo()
