from pytube import YouTube
from discord.ext import commands

import discord, subprocess, os

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ytdownload(self, ctx, url: str, file_type: str = 'mp4'):
        await ctx.message.delete()
        yt = YouTube(url)
        video = None
        out_file = None
        new_file = None

        if file_type == 'mp3':
            video = yt.streams.filter(only_audio=True).order_by('abr').last()
            out_file = video.download(output_path="./Modules/Music")
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            ffmpeg_path = './Modules/ffmpeg/ffmpeg.exe'
            subprocess.run([ffmpeg_path, '-i', out_file, new_file])
            os.remove(out_file)
        else:
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            out_file = video.download(output_path="./Modules/Music")
            new_file = out_file

        await ctx.send(f"{yt.title} has been successfully downloaded and saved to {new_file}.", delete_after=5)

    @commands.command()
    async def musicdb(self, ctx):
        await ctx.message.delete()
        f_path = "./Modules/Music"
        music = []
        for fn in os.listdir(f_path):
            music.append(fn)

        usernames_database = "\n".join(music)
        await ctx.send(f"***Lethals | Music Folder***\n`{usernames_database}`")
