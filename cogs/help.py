from discord.ext import commands

from mod.error import CustomLogger

import discord, logging

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_logger = CustomLogger('Help', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    @commands.command()
    async def help(self, ctx, menu=None):
        await ctx.message.delete()
        if menu is None:
            # Help menu
            await ctx.send(f"***Lethals | Prefix:*** {self.bot.command_prefix}\n"
                           f"`» Account` - Shows all **account** commands.\n"
                           f"`» Admin` - Shows all **admin** commands.\n"
                           f"`» Database` - Shows all **database** commands.\n"
                           f"`» Fun` - Shows all **Fun** commands.\n"
                           f"`» GameCheat` - Shows all **gamecheat** commands.\n"
                           f"`» Help` - Shows all **help** commands. (This Menu)\n"
                           f"`» Malicious` - Shows all **malicious** commands.\n"
                           f"`» Music` - Shows all **music** commands.\n"
                           f"`» Neko` - Shows all **neko** commands.\n"
                           f"`» Network` - Shows all **network** commands.\n"
                           f"`» Nsfw` - Shows all **nsfw** commands.\n"
                           f"`» System` - Shows all **system** commands.")

        elif str(menu).lower() == "account":
            # Account Commands
            await ctx.send(f"***Lethals | » Account Commands***\n"
                           f"`{self.bot.command_prefix} whois <user>` - Check user account info\n"
                           f"`{self.bot.command_prefix} status <online/idle/dnd/inv/offline>` - Set acount status\n"
                           f"`{self.bot.command_prefix} cleardm amount` - Clear a set amount of messages with a user.\n"
                           f"`{self.bot.command_prefix} clearalldm` - Clear all messages with a user.")
        
        elif str(menu).lower() == "admin":
            # Admin commands menu
            await ctx.send(f"***Lethals | » Admin Commands***\n"
                           f"`{self.bot.command_prefix} ban <member>` - Ban a member.\n"
                           f"`{self.bot.command_prefix} kick <member>` - Kick a member.\n"
                           f"`{self.bot.command_prefix} unban <member>` - Unban a member.\n"
                           f"`{self.bot.command_prefix} purge <amount>` - Purge a channel.\n"
                           f"`{self.bot.command_prefix} setnick <name>` - Set members a nickname.\n"
                           f"`{self.bot.command_prefix} clone` - Nuke a channel.\n")

        elif str(menu).lower() == "database":
            # Database commands menu
            await ctx.send(f"***Lethals | » Database Commands***\n"
                           f"`{self.bot.command_prefix} update <msg_wh/sniper_wh/prefix> <value>` - Update the Database\n"
                           f"`{self.bot.command_prefix} add <@user>` - Blacklist a user(Anit-Message).\n"
                           f"`{self.bot.command_prefix} remove <@user>` - Remove a user from the blacklist.\n"
                           f"`{self.bot.command_prefix} removeall` - Remove all users from the blacklist.\n"
                           f"`{self.bot.command_prefix} show` - Show all users in the blacklist.\n"
                           f"`{self.bot.command_prefix} antileave <@user>` - Prevents a user leaving a groupchat(Must be friends).\n"
                           f"`{self.bot.command_prefix} remove_antileave <@user>` - Remove user from antileave.\n"
                           f"`{self.bot.command_prefix} setup` - Setup log server(Must be ran inside a server).\n"
                           f"`{self.bot.command_prefix} on <logger/afk/antistaff>` - Enable Message Logger/AFk Mode/Call Logger.\n"
                           f"`{self.bot.command_prefix} off <logger/afk/antistaff>` - Disable Message Logger/AFk Mode/Call Logger.")

        elif str(menu).lower() == "fun":
            # Fun commands menu
            await ctx.send("***Lethals | » Fun Commands***\n"
                           f"`{self.bot.command_prefix} channels <server_id>` - Show all channels.\n"
                           f"`{self.bot.command_prefix} iq <@user>` - Show a members IQ.\n"
                           f"`{self.bot.command_prefix} massreact <emote> <amount>` - Mass react to messages.\n"
                           f"`{self.bot.command_prefix} embed <message>` - Sends a embed message.\n"
                           f"`{self.bot.command_prefix} coinflip` - Sends a coinflip.\n"
                           f"`{self.bot.command_prefix} passgen <amount>` - Generate a password.\n"
                           f"`{self.bot.command_prefix} gping <@user>` - Ghost ping someone.\n"
                           f"`{self.bot.command_prefix} hideinv <invite>` - Hide a invite link.\n"
                           f"`{self.bot.command_prefix} cat` - Sends a chat photo.\n"
                           f"`{self.bot.command_prefix} joke` - Sends a joke.\n"
                           f"`{self.bot.command_prefix} dog` - Sends a dog photo.\n"
                           f"`{self.bot.command_prefix} quote` - Sends a random quote.\n"
                           f"`{self.bot.command_prefix} catfact` - Sends a random cat fact.\n"
                           f"`{self.bot.command_prefix} dogfact` - Sends a random dog fact.\n"
                           f"`{self.bot.command_prefix} insult <@user>` - insult a member.\n"
                           f"`{self.bot.command_prefix} meme <message>` - Send a custom meme.\n"
                           f"`{self.bot.command_prefix} hs <1, 2 or 3>` - Set hypersquad.")

        elif str(menu).lower() == "gamecheat":
            # GameCheat commands menu
            await ctx.send(f"***Lethals | » GameCheat Commands***\n"
                           f"`{self.bot.command_prefix} gta` - Lunch Kiddons Menu(Must be in game).")
        
        elif str(menu).lower() == "malicious":
            # Malicious commands menu
            await ctx.send(f"***Lethals | » Malicious Commands***\n"
                           f"`{self.bot.command_prefix} turl <url>` - Url shortener.\n"
                           f"`{self.bot.command_prefix} spam <amount> <message>` - Spam a message.\n"
                           f"`{self.bot.command_prefix} gjoin <guid> <channelid>` - Puts your account in a voice channel.\n"
                           f"`{self.bot.command_prefix} raid` - Raid a server(Use at your own risk).")
        
        elif str(menu).lower() == "music":
            # Music commands menu
            await ctx.send(f"***Lethals | » Music Commands***\n"
                           f"`{self.bot.command_prefix} ytdownload <mp4/mp3>` - Downlaod youtube videos.\n"
                           f"`{self.bot.command_prefix} musicdb` - Show all music files.")

        elif str(menu).lower() == "neko":
            # Neko commands menu
            await ctx.send(f"***Lethals | » Neko Commands***\n"
                           f"`{self.bot.command_prefix} cry` - Send a sad photo/gif.\n"
                           f"`{self.bot.command_prefix} sleep` - Send a sleepy photo/gif.\n"
                           f"`{self.bot.command_prefix} happy` - Send a happy photo/gif.\n"
                           f"`{self.bot.command_prefix} laugh` - Send a laughing photo/gif.\n"
                           f"`{self.bot.command_prefix} smile` - Send a smile photo/gif.\n"
                           f"`{self.bot.command_prefix} bored` - Send a bored photo/gif.\n"
                           f"`{self.bot.command_prefix} thumbsup` - Send a thumbsup photo/gif.\n"
                           f"`{self.bot.command_prefix} wave` - Send a wave photo/gif.\n"
                           f"`{self.bot.command_prefix} wink` - Send a wink photo/gif.\n"
                           f"`{self.bot.command_prefix} think` - Send a think photo/gif.\n"
                           f"`{self.bot.command_prefix} nom` - Send a nom photo/gif.\n"
                           f"`{self.bot.command_prefix} nope` - Send a nope photo/gif.\n"
                           f"`{self.bot.command_prefix} nod` - Send a nod photo/gif.\n"
                           f"`{self.bot.command_prefix} yeet` - Send a yeet photo/gif.")

        elif str(menu).lower() == "network":
            # Network commands menu
            await ctx.send(f"***Lethals | » Network Commands***\n"
                           f"`{self.bot.command_prefix} geo <ip>` - Geolocate an ip.\n"
                           f"`{self.bot.command_prefix} domainresolve <domain>` - Resolve a domain.\n"
                           f"`{self.bot.command_prefix} ping <ip>` - Ping an ip.")

        elif str(menu).lower() == "nsfw":
            # NSFW commands menu
            await ctx.send(f"***Lethals | » NSFW Commands***\n"
                           f"`{self.bot.command_prefix} nsfw feet` - Sends nsfw feet content.\n"
                           f"`{self.bot.command_prefix} nsfw ass` - Sends nsfw ass content.\n"
                           f"`{self.bot.command_prefix} nsfw hentai` - Sends hentai (anime porn).\n"
                           f"`{self.bot.command_prefix} nsfw pussy` - Sends pussy.") 

        elif str(menu).lower() == "system":
            # System commands menu
            await ctx.send(f"***Lethals | » System Commands***\n"
                           f"`{self.bot.command_prefix} cls` - Clears console.")
        else:
            await ctx.send("Help Menu Does Not Exist.", delete_after=2)
