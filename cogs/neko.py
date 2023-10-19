from discord.ext import commands

import discord, json, requests

class NekoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cry(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/cry")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def happy(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/happy")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def laugh(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/laugh")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def thumbsup(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/thumbsup")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def smile(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/smile")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def bored(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/bored")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def sleep(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/sleep")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def wave(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/wave")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def wink(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/wink")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def think(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/think")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def nom(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/nom")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def nope(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/nope")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def nod(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/nod")
        await ctx.send(r.json()["results"][0]["url"])

    @commands.command()
    async def yeet(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.best/api/v2/yeet")
        await ctx.send(r.json()["results"][0]["url"])
