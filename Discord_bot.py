import discord
import random
from discord.ext import commands
import discord.utils
import requests
import youtube_dl
import os
import sqlite3
from translate import Translator
import datetime
import schedule


dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
TOKEN = "ODMxOTEzMDA5ODY1MTYyNzUy.YHcJXQ.ij7L_yhL6Cc8pztzWMlTHK46PWk"


class Multi_Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help1', aliases=["h"])
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


    @commands.command(aliases=['p'])
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

    @commands.command(aliases=["ps"])
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")

    @commands.command(aliases=["r"])
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

    @commands.command(aliases=["s"])
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()

    @commands.command(aliases=["q"])
    async def quit(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(aliases=["us"])
    async def usless(self, ctx):
        id = random.randint(1, 10)
        con = sqlite3.connect("data/tabels/useless_site.db")
        cur = con.cursor()
        result = cur.execute(f"SELECT url FROM useless WHERE id = {id}").fetchall()
        for elem in result:
            await ctx.send(str(elem[0]))
        con.close()

    @commands.command(aliases=["a_r"])
    async def add_rang(self, ctx, *arg):
        con = sqlite3.connect("data/tabels/rangs.db")
        cur = con.cursor()
        result = cur.execute(
            f"SELECT login FROM logins WHERE rang_id = (SELECT id FROM rangs WHERE rang LIKE 'admin')"
        ).fetchall()
        admins = []
        for elem in result:
            admins.append(elem[0])
        print(str(ctx.message.author), admins)
        do_comand = True
        if str(ctx.message.author) in admins:
            if len(arg) == 1:
                await ctx.send("Ошибка при вводе команды(недостаточно аргументов)")
                return
            for i in range(len(arg)):
                if "#" in arg[i]:
                    login = " ".join(arg[:i + 1])
                    print(login)
                    newrang = str(arg[i + 1])
                    if len(arg) > i + 2:
                        do_comand = False
            print(newrang)
            result = cur.execute(
                f"SELECT id FROM rangs WHERE rang LIKE '{newrang}'"
            ).fetchall()
            if len(result) == 0:
                await ctx.send("Ошибка при вводе команды(не существующий ранг)")
                return
            result = cur.execute(
                f"SELECT login FROM logins WHERE rang_id = (SELECT id FROM rangs WHERE rang LIKE '{newrang}')"
            ).fetchall()
            print(result)
            rang_users = []
            for elem in result:
                rang_users.append(elem[0])
            if login in rang_users:
                await ctx.send("Ошибка при вводе команды(у этого человека уже есть этот ранг)")
                return
            result = cur.execute(
                f"SELECT id FROM logins WHERE login = '{login}'"
            ).fetchall()
            if len(result) != 0:
                cur.execute(f"""UPDATE logins SET rang_id = (SELECT id FROM rangs WHERE rang = '{newrang}')
                            WHERE login = '{login}'""").fetchall()
                con.commit()
                con.close()
                await ctx.send("Операция прошла успешно)")
                return
            if do_comand:
                rang_id = cur.execute(f"SELECT id FROM rangs WHERE rang = '{newrang}'").fetchall()
                if len(rang_id) == 1:
                    cur.execute(f"INSERT INTO logins (login, rang_id) VALUES ('{login}', {rang_id[0][0]})")
                    con.commit()
                    await ctx.send("Операция прошла успешно)")
                else:
                    await ctx.send("Введен несуществующий ранг(")
            else:
                await ctx.send("Ошибка при вводе команды(возможно вы передали недостаточно аргументов)")
        else:
            await ctx.send("У вас нет прав на выполнение данной команды")
        con.close()

    @commands.command(aliases=["en"])
    async def en_ru(self, ctx, *args):
        txt = str(" ".join(args))
        translator = Translator(to_lang="Russian")
        translation = translator.translate(txt)
        await ctx.send(translation)

    @commands.command(aliases=["ru"])
    async def ru_en(self, ctx, *args):
        txt = str(" ".join(args))
        translator = Translator(from_lang="Russian", to_lang="English")
        translation = translator.translate(txt)
        await ctx.send(translation)

    @commands.command(aliases=["t"])
    async def timer(self, ctx, *args):
        time = ''.join(args).lower()
        if ':' in time:
            t = time.split(":")
            hours = t[0]
            minutes = t[1]
            while True:
                if int(datetime.datetime.now().strftime("%H")) == int(hours)\
                        and int(datetime.datetime.now().strftime("%M")) == int(minutes):
                    await ctx.send(f'⏰ Time X has come!')
                    break

        else:
            hours = int(time.split('hours')[0])
            minutes = int(time.split('hours')[1].split('minutes')[0])
            flag = True
            time_now = datetime.datetime.now()
            await ctx.send(f'The timer should start in {hours} hours and {minutes} minutes.')
            if flag:
                while True:
                    delta = datetime.datetime.now() - time_now
                    if delta.seconds >= hours * 3600 + minutes * 60:
                        hours, minutes, flag = 0, 0, False
                        time = None
                        break
                await ctx.send(f'⏰ Time X has come!')


bot = commands.Bot(command_prefix='-')
bot.add_cog(Multi_Bot(bot))
bot.run(TOKEN)