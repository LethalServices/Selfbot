from discord.ext import commands

from mod.error import CustomLogger
from mod.db import DatabaseManager

import discord, json, logging

class NsfwCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_logger = CustomLogger('Events', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    @commands.command()
    async def nsfw(self, ctx, arg):
        await ctx.message.delete()
        r = requests.get(f"https://nekobot.xyz/api/image?type={arg}")
        await ctx.send(r.json()["message"])
