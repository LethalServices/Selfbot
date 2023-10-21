from discord.ext import commands

from mod.error import CustomLogger

import discord, json, requests, os, subprocess, socket, requests, logging

class NetworkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_logger = CustomLogger('Network', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    @commands.command()
    async def geo(self, ctx, ip):
        await ctx.message.delete()
        try:
            r = requests.get(url = f'https://ipinfo.io/{ip}/geo')
            await ctx.send(f"***Lethals | Ipinfo***\n*IP:* `{r.json()['ip']}`\n*City:* `{r.json()['city']}`\n*Region:*** `{r.json()['country']}`\n*Location:* `{r.json()['loc']}`\n*Org:*** `{r.json()['org']}`\n*Timezone:* `{r.json()['timezone']}`")
        except:
            self.logger.error(f"Invalid ip.")

    @commands.command()
    async def domainresolve(self, ctx, domain: str):
        await ctx.message.delete()
        try:
            ips = socket.getaddrinfo(domain, None)
            ips = list(set([ip[4][0] for ip in ips]))
            await ctx.send(f"***Lethals | Domain Resolver***\nThe IP addresses of {domain} are {', '.join(ips)}.")
        except socket.gaierror:
            self.logger.error(f"Invalid domain.")

    @commands.command()
    async def ping(self, ctx, ip_address):
        await ctx.message.delete()
        try:
            ping_result = subprocess.run(f"%SystemRoot%\System32\ping.exe {ip_address}", stdout=subprocess.PIPE, shell=True)
            await ctx.send(f"***Lethals | IP Ping***\n`{ping_result.stdout.decode()}`")
        except:
            self.logger.error(f"Invalid ip.")
