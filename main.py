import telebot 
from config import token
from random import randint
from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1,10)
        if chance in [1,2,4,5,7,8,10]:
            pokemon = Pokemon(message.from_user.username)
        else:
            chance = randint(1,2)
            if chance == 1:
                pokemon = Wizard(message.from_user.username)
            else:
                pokemon = Fighter(message.from_user.username)
        pokemon_info = pokemon.info()
        pokemon_abilities = ""
        for i in enumerate(pokemon_info["abilities"]):
            ability_name = i[1]
            ability_effect = pokemon_info["abilities"][i[1]].replace("\n\n","\n")
            pokemon_abilities += f"{i[0]+1}. {ability_name}\n — {ability_effect}\n\n"
        # bot.send_message(message.chat.id, f"Имя вашего пакемона: {pokemon_info['name']}\nСпособности:\n{pokemon_abilities}Картинка вашего пакемона:")
        bot.send_photo(message.chat.id, pokemon.show_img(), caption=f"Имя вашего пакемона: {pokemon_info['name']}\nУровень: {pokemon_info['level']}\nОпыт: {pokemon_info['xp_now']}/{pokemon_info['xp_need']}\nСпособности:\n{pokemon_abilities if pokemon_abilities != '' else 'Нет'}")
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['pokemon'])
def pokemon(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        pokemon_info = pokemon.info()
        pokemon_abilities = ""
        for i in enumerate(pokemon_info["abilities"]):
            ability_name = i[1]
            ability_effect = pokemon_info["abilities"][i[1]].replace("\n\n","\n")
            pokemon_abilities += f"{i[0]+1}. {ability_name}\n — {ability_effect}\n\n"
        # bot.send_message(message.chat.id, f"Имя вашего пакемона: {pokemon_info['name']}\nСпособности:\n{pokemon_abilities}Картинка вашего пакемона:")
        bot.send_photo(message.chat.id, pokemon.show_img(), caption=f"Тип покемона: {pokemon_info['type']}\nИмя вашего пакемона: {pokemon_info['name']}\nУровень: {pokemon_info['level']} ({pokemon_info['xp_now']}/{pokemon_info['xp_need']})\nЗдоровье: {pokemon_info['hp']}\nСила атаки: {pokemon_info['power']}\nСпособности:\n{pokemon_abilities if pokemon_abilities != '' else 'Нет'}")
    else:
        bot.reply_to(message, "Ты не создал себе покемона")

@bot.message_handler(commands=['feed'])
def feed(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        xp = randint(10,15)
        bot.send_message(message.chat.id, f"Вы погуляли со своим покемоном и получили {xp} опыта!")
        result = pokemon.uppend_xp(xp)
        if result == 1:
            bot.send_message(message.chat.id, f"Вы достигли необходимого кол-ва опыта и повысили уровень покемона на 1!\nПодробнее -> /pokemon")
    else:
        bot.reply_to(message, "Ты не создал себе покемона")


@bot.message_handler(commands=['atack'])
def atack(message):
    if message.reply_to_message:
        if message.from_user.username in Pokemon.pokemons.keys() and message.reply_to_message.from_user.username in Pokemon.pokemons.keys():
            pokemon_enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pokemon_user = Pokemon.pokemons[message.from_user.username]
            result = pokemon_user.attack(pokemon_enemy)
            bot.send_message(message.chat.id, result)
        else:
            bot.reply_to(message, "Ты не создал себе покемона")
    else:
        bot.reply_to(message, "Нужно ответить на сообщение")


bot.infinity_polling(none_stop=True)

