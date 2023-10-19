from discord.ext import commands

from mod.error import CustomLogger

import discord, json, requests, os, logging

class GamecheatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_logger = CustomLogger('GameCheats', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    @commands.command()
    async def gta(self, ctx):
        await ctx.message.delete()
        try:
            self.logger.info('Launching Kiddions ModMenu!')
            os.system(f"{os.getcwd()}\\Modules\\GameCheats\\GTAV\\modest-menu.exe")
        except:
            self.logger.error('Something went wrong. Contact support.')
