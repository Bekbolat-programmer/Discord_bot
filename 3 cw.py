import json
import discord
from info import settings

start = 0


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
        if get_city.previous_city != "" and normilize_city[0] != get_city.previous_city[-1]:
            return 'Город должен начинаться на "{0}"!'.format(get_city.previous_city[-1])

        if normilize_city not in cities_already_named:
            cities_already_named.add(normilize_city)
            last_latter_city = normilize_city[-1]
            proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities))
            if proposed_names:
                for city in proposed_names:
                    if city not in cities_already_named:
                        cities_already_named.add(city)
                        get_city.previous_city = city
                        return city.capitalize()
            return 'Я не знаю города на эту букву. Ты выиграл'
        else:
            return 'Город уже был. Повторите попытку'
    else:
        return 'Некорректное название города. Повторите попытку'


get_city.previous_city = ""


def is_correct_city_name(city):
    return city[-1].isalpha() and city[-1] not in ('ь', 'ъ')


def restart():
    cities = parse_city_json()[:1500]
    cities_already_named = set()
    return 'Игра началсь заново'


# def start():
#     start = 1


cities = parse_city_json()[:1500]
cities_already_named = set()
# start = 0
TOKEN = settings['token']
bot = discord.Client()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        if message.content == '!restart':
            restart()
        # elif message.content == '!start':
        #     start()
        else:
            response = get_city(message.content)
            await message.channel.send(response)


bot.run(TOKEN)