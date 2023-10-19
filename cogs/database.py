from discord.ext import commands

from mod.error import CustomLogger
from mod.db import DatabaseManager

import discord, json, logging, requests

class DatabaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager("./Modules/database/lethal.db")
        self.custom_logger = CustomLogger('Database', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    @commands.command()
    async def update(self, ctx, option, value): 
        await ctx.message.delete()  
        if option == "msg_wh":
            try:
                self.db_manager.execute_query(f"UPDATE webhooks SET message_wh='{value}';")
                await ctx.send("***Lethals | Database***\nUpdated Database, Message Webhook has been updated!\n***NOTE: You might have to restart the bot***", delete_after=2)
            except:
                self.logger.error('Something went wrong.')
        elif option == "sniper_wh":
            try:
                self.db_manager.execute_query(f"UPDATE webhooks SET sniper_wh='{value}';")
                await ctx.send("***Lethals | Database***\nUpdated Database, Sniper Webhook has been updated!\n***NOTE: You might have to restart the bot***", delete_after=2)
            except:
                self.logger.error('Something went wrong.')
        elif option == "prefix":
            try:
                self.db_manager.execute_query(f"UPDATE config SET prefix='{value}';")
                await ctx.send("***Lethals | Database***\nUpdated Database, prefix has been updated!\n***NOTE: You might have to restart the bot***", delete_after=2)
            except:
                self.logger.error(f'Something went wrong.')

    @commands.command()
    async def add(self, ctx, member: discord.Member):
        await ctx.message.delete()
        try:
            self.db_manager.execute_query(f"INSERT INTO blacklist (member_id) VALUES ('{member.id}');")
            await ctx.send(f'***Lethals | Added Member***\n{member.name}({member.id}) has been added to the blacklist.', delete_after=2)
        except:
            self.logger.error('Something went wrong.')

    @commands.command()
    async def remove(self, ctx, member: discord.Member): 
        await ctx.message.delete() 
        self.db_manager.execute_query(f"DELETE FROM blacklist WHERE member_id = '{member.id}';")
        await ctx.send(f'***Lethals | Removed Member***\n{member.name} has been removed from the blacklist.', delete_after=2)

    @commands.command()
    async def removeall(self, ctx): 
        await ctx.message.delete() 
        blacklist = self.db_manager.execute_read_all_query(f"SELECT member_id FROM blacklist;")
        if blacklist is None:
            return await ctx.send('***Lethals | No Members***', delete_after=2)

        for i in blacklist:
            self.db_manager.execute_query(f"DELETE FROM blacklist WHERE member_id = '{str(i[0])}';")
            await ctx.send(f'***Lethals | Removed Members***\n `{mlist}`', delete_after=2)

    @commands.command()
    async def show(self, ctx): 
        await ctx.message.delete() 
        blacklist = self.db_manager.execute_read_all_query(f"SELECT member_id FROM blacklist;")
        mlist = []
        if blacklist is None:
            return await ctx.send('***Lethals | No Members***')
        
        for i in blacklist:
            i.appened(mlist)

        await ctx.send(f'***Lethals | Members Inside Database***\n `{mlist}`')

    @commands.command()
    async def antileave(self, ctx, member: discord.Member):
        await ctx.message.delete()
        self.db_manager.execute_query(f"INSERT INTO groupchat (member_id) VALUES ('{member.id}');")
        await ctx.send(f'***Lethal Selfbot | GroupChat Anti-Leave***\n{member.name} has been added to the database.', delete_after=2)

    @commands.command()
    async def remove_antileave(self, ctx, member: discord.Member): 
        await ctx.message.delete() 
        self.db_manager.execute_query(f"DELETE FROM groupchat WHERE member_id = '{member.id}';")
        await ctx.send(f'***Lethals | Removed Member***\n{member.name} has been removed from the database.', delete_after=2)

    @commands.command()
    async def setup(self, ctx):
        await ctx.message.delete()  
        guild = ctx.guild
        name = ['nitro', 'message']
        for n in name:
            ch = discord.utils.get(guild.channels, name=n)
        if ch:
            self.logger.warning(f'[{datetime.now().strftime("%H:%M:%S")}] [{Fore.GREEN}Info{Fore.WHITE}] [+] Log server has already been setup.')
            return
        else:
            category = await guild.create_category("logs")
            overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}
            msg = await category.create_text_channel("Message", overwrites=overwrites)
            mg_webhook = await msg.create_webhook(name=f"{msg}_webhook")
            try:
                self.db_manager.execute_query(f"UPDATE webhooks SET message_wh='{mg_webhook.url}';")
            except:
                print('Please contact lethal support.')
            sniper = await category.create_text_channel("Nitro", overwrites=overwrites)
            sniper_webhook = await sniper.create_webhook(name=f"{sniper}_webhook")
            try:
                self.db_manager.execute_query(f"UPDATE webhooks SET sniper_wh='{sniper_webhook.url}';")
            except:
                print('Please contact lethal support.')

            self.logger.info('[+] Log server has been setup.')
     
    @commands.command()
    async def on(self, ctx, option): 
        await ctx.message.delete() 
        if option.lower() == "logger":
            try:
                self.db_manager.execute_query("UPDATE config SET message_logger='on';")
                await ctx.send("Updated Database, Message Logger Enabled! ***NOTE: You might have to restart the bot***", delete_after=2)
            except:
                self.logger.error('Please contact lethal support.')
        elif option.lower() == "afk":
            try:
                self.db_manager.execute_query("UPDATE config SET Afk='on';")
                await ctx.send("Updated Database, You are now set to Afk. ***NOTE: You might have to restart the bot***", delete_after=2)
            except:
                self.logger.error('Please contact lethal support.')
        elif option.lower() == "antistaff":
            try:
                self.db_manager.execute_query(f"UPDATE config SET antistaff='on';")
                await ctx.send("Updated Database, AntiStaff Enabled!", delete_after=2)
            except:
                self.logger.error('Please contact lethal support.')

    @commands.command()
    async def off(self, ctx, option): 
        await ctx.message.delete()  
        if option.lower() == "logger":
            try:
                self.db_manager.execute_query("UPDATE config SET message_logger='off';")
                await ctx.send("Updated Database, Message Logger Disabled! ***NOTE: You might have to restart the bot***", delete_after=2)
            except:
                self.logger.error('Please contact lethal support.')
        
        elif option.lower() == "afk":
            try:
                self.db_manager.execute_query("UPDATE config SET Afk='off';")
                await ctx.send("Updated Database, You are now out of Afk. ***NOTE: You might have to restart the bot***", delete_after=2)
            except:
                self.logger.error('Please contact lethal support.')
        
        elif option.lower() == "antistaff":
            try:
                self.db_manager.execute_query(f"UPDATE config SET antistaff='off';")
                await ctx.send("Updated Database, AntiStaff Disabled!", delete_after=2)
            except:
                self.logger.error('Please contact lethal support.')
