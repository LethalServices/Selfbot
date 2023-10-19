from discord.ext import commands

from mod.error import CustomLogger

import discord, json, logging, requests

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_logger = CustomLogger('Events', log_level=logging.INFO)
        self.logger = self.custom_logger.get_logger()

    @commands.command()
    async def channels(self, ctx, server_id: int):
        await ctx.message.delete()
        server = self.get_guild(server_id)
        channels = server.channels
        channels_info = ""
        if not server:
            return await ctx.send(f"Server with ID {server_id} not found.")
        for channel in channels:
            channels_info += f"{channel.name} ({channel.id})\n"
        await ctx.send(f"***Lethals | {server.name} Channels:***\n`{channels_info}`")

    @commands.command()
    async def iq(self, ctx, user: discord.Member):
        await ctx.message.delete()
        iq = random.randint(0, 200)
        await ctx.send(f"{user.mention}'s IQ is {iq}.")

    @commands.command()
    async def massreact(self, ctx, emote, amount:int):
        await ctx.message.delete()
        messages = await ctx.message.channel.history(limit=amount)
        for message in messages:
            await message.add_reaction(emote)

    @commands.command()
    async def embed(self, ctx, *, desc):
        await ctx.message.delete()
        hidemsg = '||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||'   
        Base_URL = "https://embedl.ink/"
        params = {'?deg&provider':'', 'author': 'Lethals Embed', 'authorurl': 'https://lethals.org/', 'color': '#5039B0', 'media': 'thumbnail', 'mediaurl': 'https://cdn.discordapp.com/attachments/1086386664714289272/1086759710574772374/Lethal.png', 'desc': desc}
        req = PreparedRequest()
        req.prepare_url(Base_URL, params)
        UrlParams = f'{req.url}%0A%0A%C2%A9%202022%20-%202023%20Lethal%20Services%E2%84%A2%2C%20All%20rights%20reserved'.replace(Base_URL,"")
        headers = {'Host': 'embedl.ink','accept-language': 'n-US,en;q=0.5','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0','content-type': 'application/json; charset=utf-8','accept': 'application/json, text/javascript, */*; q=0.01','origin': 'https://embedl.ink','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty'}
        data = '{"url":"swag"}'.replace("swag", UrlParams) 
        response = requests.post(f'https://embedl.ink/api/create', headers=headers, data=data)
        code = response.json()['code']
        r = requests.get(f'https://tinyurl.com/api-create.php?url=https://embedl.ink/e/{code}').text
        await ctx.send(f'{hidemsg}{r}')
 
    @commands.command()
    async def coinflip(self, ctx):
        await ctx.message.delete()
        await ctx.send(choice(['Heads', 'Tails']))

    @commands.command()
    async def passgen(self, ctx, amount: int = 1):
        try:
            await ctx.message.delete()
            url = f"https://www.passwordrandom.com/query?command=password&format=json&count={amount}"
            response = requests.get(url)
            pwds = []
            if response.status_code == 200:
                passwords = response.json()["char"]
                if amount == 1:
                    await ctx.send(f"Generated Password: {passwords[0]}")
                else:
                    for p in passwords:
                        pwds.append(list(p))
                        await ctx.send("Generated Password:" + pwds)
            else:
                await ctx.send("An error occurred while generating the password(s). Please try again.")
        except requests.RequestException:
            await ctx.send("An error occurred while making the request. Please try again.")

    @commands.command()
    async def gping(self, ctx, user):
        await ctx.message.delete()
        hidemsg = ':pleading_face:||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||'   
        await ctx.send(f'{hidemsg} user')

    @commands.command()
    async def hideinv(self, ctx, invite):
        await ctx.message.delete()
        hidemsg = ':pleading_face:||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||'   
        await ctx.send(f'{hidemsg} {invite}')

    @commands.command()
    async def cat(self, ctx): 
        await ctx.message.delete()
        r = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
        await ctx.send(r)

    @commands.command()
    async def joke(self, ctx):
        await ctx.message.delete()
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code != 200:
            await ctx.send("Failed to retrieve a joke.")

        joke_data = response.json()
        setup = joke_data["setup"]
        punchline = joke_data["punchline"]
        await ctx.send(f"{setup}\n\n{punchline}")

    @commands.command()
    async def dog(self, ctx):
        await ctx.message.delete()
        r = requests.get(f"https://random.dog/woof.json")
        await ctx.send(r.json()["url"])

    @commands.command()
    async def quote(self, ctx):
        await ctx.message.delete()
        r = requests.get(f"https://animechan.vercel.app/api/random")
        await ctx.send(r.json()["quote"])

    @commands.command()
    async def catfact(self, ctx):
        await ctx.message.delete()
        response = requests.get("https://cat-fact.herokuapp.com/facts/random")
        if response.status_code != 200:
            await ctx.send("Failed to retrieve a cat fact.")
        fact_data = response.json()
        fact = fact_data["text"]
        await ctx.send(f"Cat Fact: {fact}")

    @commands.command()
    async def dogfact(self, ctx):
        await ctx.message.delete()
        response = requests.get("https://dog-api.kinduff.com/api/facts")
        if response.status_code != 200:
            await ctx.send("Failed to retrieve a dog fact.")
        fact_data = response.json()
        fact = fact_data["facts"][0]
        await ctx.send(f"Dog Fact: {fact}")

    @commands.command()
    async def insult(self, ctx, user: discord.Member):
        await ctx.message.delete()
        response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
        if response.status_code != 200:
            await ctx.send("Failed to generate an insult.")

        insult_data = response.json()
        insult = insult_data["insult"]
        await ctx.send(f"{user.mention}, {insult}")

    @commands.command()
    async def meme(self, ctx,*, bottom):
        await ctx.message.delete()
        hidemsg = '||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||'   
        message = bottom.replace(" ", "+")
        await ctx.send(f'{hidemsg}\nhttps://apimeme.com/meme?meme=10-Guy&top=&bottom={message}')

    @commands.command()
    async def hs(self, ctx, arg):
        await ctx.message.delete()
        hypesquad = int(arg)
        row = self.db_manager.execute_read_one_query(f"SELECT token FROM auth;")
        listify = list(row)   
        headers = {'authorization': listify[0]}
        body = {'house_id': hypesquad}
        response = requests.post('https://discord.com/api/v9/hypesquad/online', headers=headers, json=body)

        if response.status_code == 204:
            await ctx.send('Changed badge succesfully!', delete_after=2)
        elif response.status_code == 401:
            await ctx.send('Changing badge has failed: 401', delete_after=2)
        elif response.status_code == 429:
            await ctx.send('Changing badge has failed: Rate limited (429)', delete_after=2)

    @commands.command()
    async def eightball(self, ctx, *, question):
        await ctx.message.delete()
        responses = ["Yes", "No", "Maybe", "Ask again later", "Probably", "Certainly not"]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")
    
    @commands.command()
    async def urban(self, ctx, *, term):
        await ctx.message.delete()
        url = f"http://api.urbandictionary.com/v0/define?term={term}"
        response = requests.get(url)
        if response.status_code != 200:
            await ctx.send("Failed to retrieve definition.")
        else:
            definition = response.json()["list"][0]["definition"]
            await ctx.send(f"Definition for {term}: {definition}")
    
    @commands.command()
    async def reverse(self, ctx, *, text: str):
        await ctx.message.delete()
        reversed_text = text[::-1]
        await ctx.send(reversed_text)
