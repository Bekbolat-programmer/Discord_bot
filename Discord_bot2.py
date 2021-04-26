# Тут изменения начинаются
import random
from discord.ext import commands
import discord
from discord.ext.commands import Bot
import discord.utils
import requests
import youtube_dl
import sqlite3
from translate import Translator
import datetime
import os
import json
# Тут изменения заканчиваются


dashes = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
TOKEN = "токен"
ban_words = ["политика", "мачу-пикчу", "чихуа-хуа"]
support = ["Поздравляем", "Молодец", "Ююююхууууу"]
# Тут изменения начинаются
hello = ['Приветсвую', 'Давно не виделись', 'Специальное электронное приветсвие для', 'Hello']


def parse_city_json(json_file='russia.json'):
    p_obj = None
    try:
        js_obj = open(json_file, "r", encoding="utf-8")
        p_obj = json.load(js_obj)
    except Exception as err:
        print(err)
        return None
    finally:
        js_obj.close()
    return [city['city'].lower() for city in p_obj]


def get_city(city):
    normilize_city = city.strip().lower()[1:]
    if is_correct_city_name(normilize_city):
        if is_correct_city(normilize_city):
            if get_city.previous_city != "" and normilize_city[0] != get_city.previous_city[-1]:
                return 'Город должен начинаться на "{0}" 🥴'.format(get_city.previous_city[-1])

            if normilize_city not in cities_already_named:
                cities_already_named.append(normilize_city)
                last_latter_city = normilize_city[-1]
                proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities))
                if proposed_names:
                    for city in proposed_names:
                        if city not in cities_already_named:
                            cities_already_named.append(city)
                            get_city.previous_city = city
                            return city.capitalize()
                return 'Я не знаю города на эту букву😔. Ты выиграл🥳'
            else:
                return 'Город уже был🥴. Повторите попытку'
        else:
            return 'Прости я не знаю такого города😓 Убедись, что город написан правильно и является городом России'
    else:
        return 'Некорректное название города🥴. Повторите попытку'


get_city.previous_city = ""
cities = parse_city_json()[:3500]
cities_already_named = []
gamestart = [0]


def is_correct_city_name(city):
    return city[-1].isalpha() and city[-1] not in ('ь', 'ъ')


def is_correct_city(city):
    a = False
    for i in cities:
        if city.lower() == i.lower():
            a = True
            break
    return a
# Тут изменения заканчиваются


class Multi_Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Тут изменения начинаются
    @commands.Cog.listener()
    async def on_message(self, message):
        for i in ban_words:
            if i in message.content.lower():
                await message.delete()
                await message.channel.send(f'{str(message.author)} ваше сообщение было удаленно '
                                           f'из-за нарушений правил чата🤬\nСтарайтесь больше'
                                           f' не нарушать правила чата🤐')
        if "ура" in message.content.lower():
            await message.channel.send(random.choice(support))
        if 'привет' in message.content.lower():
            if message.author != bot.user:
                await message.channel.send(f'{random.choice(hello)} {str(message.author)}')
        if gamestart[0] == 1:
            if message.content.startswith('!'):
                response = get_city(message.content)
                await message.channel.send(response)

    @commands.command(name='game_city')
    async def game_city(self, ctx, *arg):
        gamestart.append(1)
        del gamestart[0]
        await ctx.send('Я очень люблю игры! Одной из моих любимых является Doom, но к сожалению я всего лишь бот'
                       ' и не могу в неё играть. Но мы можем скоротать время в города. Правила очень простые, думаю'
                       ' ты их знаешь. Только я расскажу про пару условностей. Все города которые ты мне отправляешь'
                       ' должны начинаться с восклицательного знака и являться городами России матушки. '
                       'Нельзя дважды называть один и тот же город. Если'
                       ' ты захочешь начать с начала, то введи команду -restart, а если захочешь прекратить играть'
                       ' введи команду -stop_city')
        await ctx.send('Начинаем игру, ты первый')

    @commands.command(name='restart')
    async def restart(self, ctx, *arg):
        cities = parse_city_json()[:3500]
        cities_already_named.clear()
        get_city.previous_city = ""
        await ctx.send('Начинаем играть заново, ты первый')

    @commands.command(name='stop_city')
    async def stop_city(self, ctx, *arg):
        gamestart.append(0)
        del gamestart[0]
        cities = parse_city_json()[:3500]
        cities_already_named.clear()
        get_city.previous_city = ""
        await ctx.send('Игра закончилась, было весело🤪')
    @commands.command(aliases=["g"])
    async def game(self, ctx, *args):
        print(len(args), args)
        if len(args) != 0:
            genre = " ".join(args).lower()
            con = sqlite3.connect("data/tabels/games.db")
            cur = con.cursor()
            result = cur.execute(f"SELECT id FROM genres WHERE genre LIKE '%{genre}%'").fetchall()
            if len(result) != 0:
                games = cur.execute(f"SELECT * FROM games WHERE genre_id = {result[0][0]}").fetchall()
                game = random.randint(0, len(games))
                for i in range(1, len(games[game])):
                    if i == 2:
                        pass
                    else:
                        await ctx.send(games[game][i])
                cur.close()
            else:
                games = cur.execute(f"SELECT * FROM games").fetchall()
                game = random.randint(0, len(games))
                await ctx.send("Извините у нас нет игры в таком жанре 😞")
                await ctx.send("❗_Но мы можем предложить:_❗")
                for i in range(1, len(games[game])):
                    if i == 1:
                        await ctx.send(f'`{games[game][i]}`')
                    elif i == 2:
                        pass
                    else:
                        await ctx.send(games[game][i])
                cur.close()
        else:
            con = sqlite3.connect("data/tabels/games.db")
            cur = con.cursor()
            games = cur.execute(f"SELECT * FROM games").fetchall()
            game = random.randint(0, len(games))
            await ctx.send("❗_Вот что мы можем предложить_❗(надеемся вы хорошо проведете время):")
            for i in range(1, len(games[game])):
                if i == 1:
                    await ctx.send(f'`{games[game][i]}`')
                elif i == 2:
                    pass
                else:
                    await ctx.send(games[game][i])
            cur.close()

    @commands.command(aliases=["b"])
    async def book(self, ctx, *args):
        print(len(args), args)
        if len(args) != 0:
            genre = " ".join(args).lower()
            con = sqlite3.connect("data/tabels/books.db")
            cur = con.cursor()
            result = cur.execute(f"SELECT id FROM genres WHERE genre LIKE '%{genre}%'").fetchall()
            if len(result) != 0:
                books = cur.execute(f"SELECT * FROM books WHERE genre_id = {result[0][0]}").fetchall()
                book = random.randint(0, len(books))
                for i in range(1, len(books[book])):
                    if i == 2:
                        pass
                    else:
                        await ctx.send(books[book][i])
                cur.close()
            else:
                books = cur.execute(f"SELECT * FROM books").fetchall()
                book = random.randint(0, len(books))
                await ctx.send("Извините у нас нет книги в таком жанре 😞")
                await ctx.send("❗_Но мы можем предложить:_❗")
                for i in range(1, len(books[book])):
                    if i == 1:
                        await ctx.send(f'`{books[book][i]}`')
                    elif i == 2:
                        pass
                    else:
                        await ctx.send(books[book][i])
                cur.close()
        else:
            con = sqlite3.connect("data/tabels/books.db")
            cur = con.cursor()
            books = cur.execute(f"SELECT * FROM books").fetchall()
            book = random.randint(0, len(books))
            await ctx.send("❗_Вот что мы можем предложить_❗(надеемся вы хорошо проведете время):")
            for i in range(1, len(books[book])):
                if i == 1:
                    await ctx.send(f'`{books[book][i]}`')
                elif i == 2:
                    pass
                else:
                    await ctx.send(books[book][i])
            cur.close()

# Тут изменения заканчиваются

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
                    await ctx.send("Введен несуществующий ранг")
            else:
                await ctx.send("Ошибка при вводе команды(возможно вы передали недостаточно аргументов)")
        else:
            await ctx.send("У вас нет прав на выполнение данной команды 🤔")
        con.close()

    @commands.command(aliases=["en"])
    async def en_ru(self, ctx, *args):
        txt = str(" ".join(args))
        translator = Translator(to_lang="Russian")
        translation = translator.translate(txt)
        await ctx.send(translation)

    @commands.command(aliases=["ru"])
    async def ru_en(self, ctx, *args):
        try:
            txt = str(" ".join(args))
            translator = Translator(from_lang="Russian", to_lang="English")
            translation = translator.translate(txt)
            await ctx.send(translation)
        except:
            await ctx.send("Ошибка выполнения команды.😔")
            await ctx.send("Возможно вы перево дите не с русского языка")

    @commands.command(aliases=["t"])
    async def timer(self, ctx, *args):
        try:
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
        except:
            await ctx.send(f'Команды была введена неправильно 😞')
            await ctx.send(f'Воспользуйтесь командой `-help_game`, чтобы сверить запрос')

    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member, reason=None):
        try:
            con = sqlite3.connect("data/tabels/rangs.db")
            cur = con.cursor()
            result = cur.execute(
                f"SELECT login FROM logins WHERE rang_id = (SELECT id FROM rangs WHERE rang LIKE 'admin')"
            ).fetchall()
            admins = []
            for elem in result:
                admins.append(elem[0])
            if str(ctx.message.author) in admins:
                await user.kick(reason=reason)
                await ctx.send(f"Вы успешно кикнули {user} 😞")
            else:
                await ctx.send(f'У вас нет прав на выполнение данной команды 😕')
        except:
            await ctx.send(f'Неверно введен пользователь 🤔')

    @commands.command()
    async def ban(self, ctx, user: discord.Member, *reason):
        try:
            con = sqlite3.connect("data/tabels/rangs.db")
            cur = con.cursor()
            result = cur.execute(
                f"SELECT login FROM logins WHERE rang_id = (SELECT id FROM rangs WHERE rang LIKE 'admin')"
            ).fetchall()
            admins = []
            for elem in result:
                admins.append(elem[0])
            if str(ctx.message.author) in admins:
                await user.ban(reason=" ".join(reason))
                await ctx.send(f"{user} был __успешно__ забанен на сервере 😞")
            else:
                await ctx.send(f'У вас нет прав на выполнение данной команды 😕')
        except:
            await ctx.send(f'Неверно введен пользователь 🤔')

    @commands.command()
    async def unban(self, ctx, user: discord.Member):
        try:
            con = sqlite3.connect("data/tabels/rangs.db")
            cur = con.cursor()
            result = cur.execute(
                f"SELECT login FROM logins WHERE rang_id = (SELECT id FROM rangs WHERE rang LIKE 'admin')"
            ).fetchall()
            admins = []
            for elem in result:
                admins.append(elem[0])
            if str(ctx.message.author) in admins:
                await user.unban()
                await ctx.send(f"Разбан пользователя{user} был __успешно__ выполнен 👏")
            else:
                await ctx.send(f'У вас нет прав на выполнение данной команды 😕')
        except:
            await ctx.send(f'Неверно введен пользователь или данный пользователь не был забанен 😉')

    @commands.command(aliases=["g"])
    async def game(self, ctx, *args):
        print(len(args), args)
        if len(args) != 0:
            genre = " ".join(args).lower()
            con = sqlite3.connect("data/tabels/games.db")
            cur = con.cursor()
            result = cur.execute(f"SELECT id FROM genres WHERE genre LIKE '%{genre}%'").fetchall()
            if len(result) != 0:
                games = cur.execute(f"SELECT * FROM games WHERE genre_id = {result[0][0]}").fetchall()
                game = random.randint(0, len(games))
                for i in range(1, len(games[game])):
                    if i == 2:
                        pass
                    else:
                        await ctx.send(games[game][i])
                cur.close()
            else:
                games = cur.execute(f"SELECT * FROM games").fetchall()
                game = random.randint(0, len(games))
                await ctx.send("Извините у нас нет игры в таком жанре 😞")
                await ctx.send("❗__Но мы можем предложить:__❗")
                for i in range(1, len(games[game])):
                    if i == 1:
                        await ctx.send(f'`{games[game][i]}`')
                    elif i == 2:
                        pass
                    else:
                        await ctx.send(games[game][i])
                cur.close()
        else:
            con = sqlite3.connect("data/tabels/games.db")
            cur = con.cursor()
            games = cur.execute(f"SELECT * FROM games").fetchall()
            game = random.randint(0, len(games))
            await ctx.send("❗__Вот что мы можем предложить__❗(надеемся вы хорошо проведете время):")
            for i in range(1, len(games[game])):
                if i == 1:
                    await ctx.send(f'`{games[game][i]}`')
                elif i == 2:
                    pass
                else:
                    await ctx.send(games[game][i])
            cur.close()


bot = commands.Bot(command_prefix='-')
bot.add_cog(Multi_Bot(bot))
bot.run(TOKEN)
