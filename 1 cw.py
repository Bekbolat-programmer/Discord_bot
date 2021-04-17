import discord
import random
from discord.ext import commands
import discord.utils
import requests
import youtube_dl
import os

dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
TOKEN = "ODMxOTEzMDA5ODY1MTYyNzUy.YHcJXQ.guyhjdTzngHnTg_HHFQknlw2oCI"


class Multi_Bot(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @commands.command(name='help1')
    async def help1(self, ctx, *arg):
        await ctx.send(str(ctx.message.author) + "\u2680")

    @commands.command(name='roll_dice')
    async def roll_dice(self, ctx, count, *arg):
        if len(arg) != 0:
            await ctx.send("Лишний аргумент")
        else:
            res = [random.choice(dashes) for _ in range(int(count))]
            await ctx.send(" ".join(res))

    @commands.command(name='cat')
    async def cat(self, ctx, *arg):
        if len(arg) != 0:
            await ctx.send("Лишний аргумент")
        else:
            response = requests.get("https://api.thecatapi.com/v1/images/search")
            data = response.json()
            await ctx.send(data[0]['url'])

    @commands.command(name='dog')
    async def dog(self, ctx, *arg):
        if len(arg) != 0:
            await ctx.send("Лишний аргумент")
        else:
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            data = response.json()
            await ctx.send(data['message'])






    @commands.command()
    async def play(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Music')
            await voiceChannel.connect()
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        # if voice.is_connected():
        #     await voice.disconnect()
        # else:
        #     await ctx.send("The bot is not connected to a voice channel.")


bot = commands.Bot(command_prefix='-')
bot.add_cog(Multi_Bot(bot))
bot.run(TOKEN)