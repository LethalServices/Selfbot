from colorama import Fore
from random import choice
from discord import Webhook
from discord.ext import commands

from mod.notifier import notify
from mod.error import CustomLogger
from mod.db import DatabaseManager

import discord, os, subprocess, socket, aiohttp, logging, re, datetime, httpx, asyncio

class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager("./Modules/database/lethal.db")
        self.custom_logger = CustomLogger('Events', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()
        self.GiftPattern = re.compile("(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")
        self.token =  self.db_manager.execute_read_one_query("SELECT token FROM auth;")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"Logged in as {self.bot.user.name} ({self.bot.user.id})")
        self.logger.info(f"Guild Count (servers): {len(self.bot.guilds)}")
        self.logger.info(f"Friend Count: {len(self.bot.friends)}")
        self.logger.info(f"Command Count: {len(self.bot.commands)}")
        self.logger.info(f"Latency: {round(self.bot.latency * 1000)}ms")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            self.logger.info('You are missing input requirements.')
        elif isinstance(error, discord.HTTPException):
            self.logger.info('You are ratelimited.')
        elif isinstance(error, commands.CommandNotFound):
            self.logger.info(f'That is not a command. Do {self.bot.command_prefix}help for commands')
        else:
            self.logger.error(f'{error}')

    @commands.Cog.listener()
    async def on_message(self, message):
        blacklist = self.db_manager.execute_read_all_query("SELECT member_id FROM blacklist;")
        afk = self.db_manager.execute_read_one_query("SELECT Afk FROM config;")
        sniper_webhook = self.db_manager.execute_read_one_query("SELECT sniper_wh FROM webhooks;")

        if message.author == self.bot.user:
            return

        await self.bot.process_commands(message)
        
        if blacklist is not None:
            for i in blacklist:
                if message.author.id == int(i[0]):
                    if isinstance(message.channel,discord.DMChannel):
                        return
                    elif isinstance(message.channel, discord.GroupChannel):
                        return

                    await message.delete()
                    self.logger.info(f'{message.author} Has tried to send a message | Message: {message.content}')

        if afk[0] == 'on':
            if isinstance(message.channel, discord.GroupChannel):
                return

            if isinstance(message.channel, discord.DMChannel):
                response2 = ["Sorry, I am currently away from my keyboard. I will get back to you as soon as possible.", "Away from my desk right now, please leave a message and I'll respond when I return.", "I am not available at the moment. Please leave a message and I will reply when I am back.", "Currently away, but I will be back shortly. Thanks for your patience!", "I am taking a break from my computer. Please expect a delay in my response.", "I am AFK, but I will return shortly. Please hold tight!", "Out of my room right now, I will reply to your message as soon as I can.", "I am away from my computer at the moment. If you need urgent assistance, please contact someone else on my team.", "I am currently away and unable to respond. I will get back to you as soon as possible.", "Sorry, I am not available to chat right now. Please leave a message and I'll reply as soon as I can."]
                async with message.channel.typing():
                    await message.channel.send(choice(response2), delete_after=5)
                    await asyncio.sleep(2)

        if self.GiftPattern.search(message.content):
            code = self.GiftPattern.search(message.content).group(2)
            start_time = datetime.datetime.now()
            headers = {'authority': 'discord.com','authorization': self.token[0],'accept-language': 'en-US','user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9010 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36','content-type': 'application/json','accept': '*/*','origin': 'https://discord.com','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty'}
            data = '{"channel_id":null,"payment_source_id":null}'
            async with httpx.AsyncClient() as client:
                response = await client.post(f'https://discordapp.com/api/v9/entitlements/gift-codes/{code}/redeem', headers=headers, data=data.replace("lethal", str(message.channel.id)))

            embed = discord.Embed(title='Lethal Nitro Sniper', color=0x7289da)
            embed.set_author(name=f'Account: {self.bot.user}', url='https://discord.gg/lethals', icon_url=self.bot.user.avatar)
            if response.status_code == 200:
                embed.description = 'Successfully Redeemed'
                if message.guild == None:
                    embed.add_field(name="Sent By:", value=f"{message.channel}")
                    self.logger.info(f'[Sniper] Code: {code} | Successfully Redeemed | DelayOf: {(datetime.datetime.now() - start_time).total_seconds():.2f} seconds | Sent By: {message.channel}')
                else:
                    embed.add_field(name="Guild:", value=f"{message.author.guild}")
                    embed.add_field(name="Sent By:", value=f"{message.author.mention}")
                    self.logger.info(f'[Sniper] Code: {code} | Successfully Redeemed | DelayOf: {(datetime.datetime.now() - start_time).total_seconds():.2f} seconds | Sent By: {message.author} | Guild: {message.author.guild}')
            else:
                embed.description = 'Failed To Redeem'
                if message.guild == None:
                    embed.add_field(name="Sent By:", value=f"{message.channel}")
                    self.logger.info(f'[Sniper] Code: {code} | Failed To Redeem | DelayOf: {(datetime.datetime.now() - start_time).total_seconds():.2f} seconds | Sent By: {message.channel}')
                else:
                    embed.add_field(name="Guild:", value=f"{message.author.guild}")
                    embed.add_field(name="Sent By:", value=f"{message.author.mention}")
                    self.logger.info(f'[Sniper] Code: {code} | Failed To Redeem | DelayOf: {(datetime.datetime.now() - start_time).total_seconds():.2f} seconds | Sent By: {message.author} | Guild: {message.author.guild}')
            embed.add_field(name="Code:", value=code)
            embed.add_field(name="DelayOf:", value=f"{(datetime.datetime.now() - start_time).total_seconds():.2f} seconds")
            embed.set_footer(text="© 2022 - 2023 Lethal Services ™ | All rights reserved.")
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(sniper_webhook[0], session=session)
                try:
                    await webhook.send(embed=embed, username='Lethal')
                except:
                    self.logger.error('Invalid Webhook.')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        message_logger = self.db_manager.execute_read_one_query(f"SELECT message_logger FROM config;")
        message_webhook = self.db_manager.execute_read_one_query(f"SELECT message_wh FROM webhooks;")

        if isinstance(message.channel,discord.DMChannel):
            if message.author == self.bot.user:
                return
            
            if message_logger[0] == "on":
                webhook = Webhook.from_url(f"{message_webhook[0]}", session=session)
                embed=discord.Embed(title='Message Logger', description=f'{message.channel}', color=0x7289da)
                embed.set_author(name=f'Account: {self.bot.user}', url='https://discord.gg/lethals', icon_url=self.bot.user.avatar)
                if message.attachments:
                    if message.content:
                        embed.add_field(name='Message Deleted:', value=f'{message.content}')
                        embed.add_field(name='File Deleted:', value=f"[Download]({message.attachments[0]})")  
                    else:
                        embed.add_field(name='File Deleted:', value=f"[Download]({message.attachments[0]})") 
                else:
                    embed.add_field(name='Message Deleted:', value=f'{message.content}') 
                embed.add_field(name='Deleted By:', value=f'{message.author.mention}', inline=False)
                embed.set_footer(text="© 2022 - 2023 Lethal Services ™ | All rights reserved.")
                async with aiohttp.ClientSession() as session:
                    try:
                        await webhook.send(embed=embed, username='Lethals Log')
                    except:
                        self.logger.error('Invalid Webhook.')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        message_logger = self.db_manager.execute_read_one_query(f"SELECT message_logger FROM config;")
        message_webhook = self.db_manager.execute_read_one_query(f"SELECT message_wh FROM webhooks;")

        if after.author.id == self.bot.user.id:
            return

        if message_logger[0] == "on":
            if before.content != after.content and isinstance(after.channel, discord.DMChannel):
                webhook = Webhook.from_url(f"{message_webhook[0]}", session=session)
                embed=discord.Embed(title='Message Logger', description=f'Message Edited In {after.channel}', color=0x7289da)
                embed.set_author(name=f'Account: {self.bot.user}', url='https://discord.gg/lethals', icon_url=self.bot.user.avatar)
                embed.add_field(name='Message Edited:', value=f'{before.content} -> {after.content}')
                embed.add_field(name='Edited By:', value=f'{after.author.mention}', inline=False)  
                embed.set_footer(text="© 2022 - 2023 Lethal Services ™ | All rights reserved.")
                async with aiohttp.ClientSession() as session:
                    try:
                        await webhook.send(embed=embed, username='Lethals Log')
                    except:
                        self.logger.error('Invalid Webhook.')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        antistaff = self.db_manager.execute_read_one_query("SELECT antistaff FROM config;")
        blacklist = self.db_manager.execute_read_all_query("SELECT member_id FROM blacklist;")

        if isinstance(before.channel, discord.GroupChannel) or isinstance(after.channel, discord.GroupChannel):
            return

        if isinstance(before.channel, discord.DMChannel) or isinstance(after.channel, discord.DMChannel):
            return

        if member.id == self.bot.user.id:
            return

        if blacklist is not None:
            for i in blacklist:
                if not before.channel and after.channel and isinstance(member, discord.Member) and member.id == int(i[0]):
                    await member.move_to(None)
                    self.logger.info(f'{member} Has Tried To Join VC!')

        if antistaff[0] == "on":
            bot = self.bot.get_guild(member.guild.id).me
            bot_voice_state = bot.voice
            if before.channel != after.channel:
                if bot_voice_state and bot_voice_state.channel == after.channel:
                    if member.guild_permissions.administrator:
                        notify("Lethals Alert", f'Admin Has Joined Your Call\nTop Role: {member.top_role.name}\nUsername: {member}\nUserid: {member.id}')

                    elif member.guild_permissions.kick_members or member.guild_permissions.ban_members:
                        notify("Lethals Alert", f'Moderator Has Joined Your Call\nTop Role: {member.top_role.name}\nUsername: {member}\nUserid: {member.id}')
                    else:
                        self.logger.info(f'{member}{Fore.WHITE} Has Joined Your Call |{Fore.LIGHTMAGENTA_EX} ID:{Fore.WHITE} {member.id} |{Fore.LIGHTMAGENTA_EX} Top Role:{Fore.WHITE} {member.top_role.name}')
            
                if bot_voice_state and bot_voice_state.channel == before.channel and before.channel is not None and after.channel is None:
                    if member.guild_permissions.administrator:
                        notify("Lethals Alert", f'Admin Has Left Call\nTop Role: {member.top_role.name}\nUsername: {member}\nUserid: {member.id}')
                    elif member.guild_permissions.kick_members or member.guild_permissions.ban_members:
                        notify("Lethals Alert", f'Moderator Has Left Call\nTop Role: {member.top_role.name}\nUsername: {member}\nUserid: {member.id}')
                    else:
                        self.logger.info(f'{member} Has Left The Call | {Fore.LIGHTMAGENTA_EX} ID: {Fore.WHITE}{member.id} | Top Role: {Fore.WHITE}{member.top_role.name}')

                if bot_voice_state and bot_voice_state.channel == before.channel:
                    if after.channel is None or before.channel is None:
                        return

                    if member.guild_permissions.administrator:
                        notify("Lethals Alert", f'Admin Has Moved To Channel: {after.channel}\nTop Role: {member.top_role.name}\nUsername: {member}\nUserid: {member.id}')
                    elif member.guild_permissions.kick_members or member.guild_permissions.ban_members:
                        notify("Lethals Alert", f'Moderator Has Moved To Channel: {after.channel}\nTop Role: {member.top_role.name}\nUsername: {member}\nUserid: {member.id}')
                    else:
                        self.logger.info(f'{member} Has Moved to {after.channel} | {Fore.LIGHTMAGENTA_EX} ID: {Fore.WHITE}{member.id} |{Fore.LIGHTMAGENTA_EX} Top Role:{Fore.WHITE} {member.top_role.name}')
                
            if before.self_deaf != after.self_deaf and before.channel is not None and bot_voice_state and bot_voice_state.channel == before.channel:
                if before.channel == after.channel:
                    if after.self_deaf:
                        self.logger.info(f'{member} Has Deafened |{Fore.LIGHTMAGENTA_EX} ID: {Fore.WHITE}{member.id} |{Fore.LIGHTMAGENTA_EX} Top Role:{Fore.WHITE} {member.top_role.name}')
                    
                    elif before.self_deaf:
                        self.logger.info(f'{member} Has Undeafened |{Fore.LIGHTMAGENTA_EX} ID: {Fore.WHITE}{member.id} |{Fore.LIGHTMAGENTA_EX} Top Role:{Fore.WHITE} {member.top_role.name}')
        
            elif before.self_mute != after.self_mute:
                if before.channel is not None and bot_voice_state and bot_voice_state.channel == before.channel:
                    if before.channel == after.channel and after.self_mute:
                        self.logger.info(f'{member} Has Muted |{Fore.LIGHTMAGENTA_EX} ID:{Fore.WHITE} {member.id} |{Fore.LIGHTMAGENTA_EX} Top Role:{Fore.WHITE} {member.top_role.name}')
                    
                    elif before.channel == after.channel and before.self_mute:
                        self.logger.info(f'{member} Has Unmuted |{Fore.LIGHTMAGENTA_EX} ID:{Fore.WHITE} {member.id} |{Fore.LIGHTMAGENTA_EX} Top Role:{Fore.WHITE} {member.top_role.name}')

    @commands.Cog.listener()
    async def on_group_remove(self, channel, member):
        groupchat_blacklist = self.db_manager.execute_read_all_query("SELECT member_id FROM blacklist;")
        if groupchat_blacklist is not None:
            for i in groupchat_blacklist:
                if member.id == int(i[0]):
                    await channel.add_recipients(member)
                    self.logger.info(f'{member} Has tried to leave the groupchat.')
