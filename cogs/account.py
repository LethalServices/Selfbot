from discord.ext import commands

from mod.error import CustomLogger
from mod.db import DatabaseManager

import discord, json, logging, asyncio

class AccountCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_logger = CustomLogger('Account', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    @commands.command()
    async def whois(self, ctx, member: discord.Member):
        await ctx.message.delete()
        await ctx.send(f"***Lethals | Whois {member.mention}***\n```ini\n[Member ID] {member.id}\n[Display Name] {member.name}\n[Created Account On] {member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC')}\n[Banner URL] {member.banner_url}\n[Member color] {member.color}\n[Profile Picture URL] {member.display_avatar.url} ```")

    @commands.command()
    async def status(self, ctx, option):
        await ctx.message.delete()
        if option.lower() == "online":
            await self.change_presence(status=discord.Status.online) 
            await ctx.send(f"***Lethals | Status: Online***", delete_after=2) 
        elif option.lower() == "idle":
            await self.change_presence(status=discord.Status.idle) 
            await ctx.send(f"***Lethals | Status: Idle***", delete_after=2) 
        elif option.lower() == "dnd":
            await self.change_presence(status=discord.Status.do_not_disturb)
            await ctx.send(f"***Lethals | Status: Do Not Disturb***", delete_after=2) 
        elif option.lower() == "inv":
            await self.change_presence(status=discord.Status.invisible) 
            await ctx.send(f"***Lethals | Status: Invisible***", delete_after=2)        
        elif option.lower() == "offline":
            await self.change_presence(status=discord.Status.offline)  
            await ctx.send(f"***Lethals | Status: Offline***", delete_after=2)

    @commands.command()
    async def cleardm(self, ctx, limit: int):
        await ctx.message.delete()

        def member_message(message):
            return message.author == ctx.author and message.channel == ctx.channel

        messages = []
        async for message in ctx.channel.history(limit=limit):
            if member_message(message):
                messages.append(message)

        messages_to_delete = []
        for message in messages:
            messages_to_delete.append(message)
            await message.delete()
            await asyncio.sleep(3)

        count = len(messages_to_delete)
        self.logger.info(f'{count} messages have been deleted.')

    @commands.command()
    async def clearalldm(self, ctx):
        await ctx.message.delete()

        def member_message(message):
            return message.author == ctx.author and message.channel == ctx.channel
    
        messages = []
        async for message in ctx.channel.history():
            if member_message(message):
                messages.append(message)
    
        messages_to_delete = []
        for message in messages:
            messages_to_delete.append(message)
            await message.delete()
            await asyncio.sleep(3)
    
        count = len(messages_to_delete)
        self.logger.info(f'{count} messages have been deleted.')
