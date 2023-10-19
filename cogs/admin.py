from discord.ext import commands

from mod.error import CustomLogger
from mod.db import DatabaseManager

import discord, json, logging

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_logger = CustomLogger('Admin', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    @commands.command()
    async def setnick(self, ctx, member: discord.Member, nickname):
        await ctx.message.delete()
        if isinstance(ctx.channel, discord.DMChannel):
            return self.logger.warning('Sorry, this command can only be used in a server.')
            
        else:
            await member.edit(nick=nickname)
            await ctx.send(f"{member.mention}'s Username Changed To {nickname}")

    @commands.command()
    async def kick(self, ctx, member : discord.Member, reason = None):
        await ctx.message.delete()
        if isinstance(ctx.channel, discord.DMChannel):
            return self.logger.warning('Sorry, this command can only be used in a server.')
        else:
            if reason == "None":
                await member.kick(reason = "None")
            else:
                await member.kick(reason= reason)
            self.logger.info(f'{member.name} has been kicked.') 
   
    @commands.command()
    async def purge(self, ctx, amount):
        if isinstance(ctx.channel, discord.DMChannel):
            return self.logger.warning('Sorry, this command can only be used in a server.')
            
        else:
            await ctx.channel.purge(limit=int(amount))
            self.logger.info(f'{amount} messages has been delete.')

    @commands.command()
    async def ban(self, ctx, member : discord.Member, reason = None):
        await ctx.message.delete()
        if isinstance(ctx.channel, discord.DMChannel):
            return self.logger.warning(f'Sorry, this command can only be used in a server.')

        if reason == None:
            await member.ban(reason = "None")
        else:
            await member.ban(reason = "None")
        self.logger.info(f'{member.name} has been banned.') 

    @commands.command()
    async def unban(self, ctx, member : discord.Member): 
        await ctx.message.delete()
        if isinstance(ctx.channel, discord.DMChannel):
            return self.logger.warning(f'Sorry, this command can only be used in a server.')

        b = await ctx.guild.bans()
        for i in b:
            u = i.user
            if u.id == id:
                await ctx.guild.unban(u)
                self.logger.info(f'{member.name} has been unbanned.') 

    @commands.command()
    async def clone(self, ctx):
        await ctx.channel.delete()
        if isinstance(ctx.channel, discord.DMChannel):
            return self.logger.warning(f'Sorry, this command can only be used in a server.')

        channel = await ctx.channel.clone()
        self.logger.info(f'{channel} has been cloned.')
