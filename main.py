import random
import telebot
import data
import buttons
import mobs

bot = telebot.TeleBot('5842917493:AAGGg8sbA7cuq4XuITc640zVSsvHpkvMpsU')

if data.check_hero_db(67821449):
    pass
else:
    data.create_new_hero(67821449, 'Админ', 'Амир', 'none', 10, 12, 10000, 'None', 1000)

@bot.message_handler(commands=['start'])
def start_message(message):
    id = message.from_user.id
    if data.check_hero_db(id):
        hello_to_user = random.choice((f"Привет {data.hero_info(id)[1]}", f"Приветствую {data.hero_info(id)[1]}",
                                       f"Это же {data.hero_info(id)[1]}! Пошли пить!", "Да я слышу слышу",
                                       f'Хочешь в данж?', f'Как жизнь {data.hero_info(id)[1]}?'))
        bot.send_message(id, hello_to_user, reply_markup=buttons.start_buttons())

    else:
        text = f'Здравтвуй, меня зовут *Густав*, на всем твоей пути я буду помогать тебе.\n\n' \
               f'*{message.from_user.first_name}* конечно круто звучит, но давай подберем тебе что-то более героическое.'
        text2 = 'Отправь свое новое имя:'

        bot.send_message(id, text, parse_mode='Markdown')
        bot.send_message(id, text2)
        bot.register_next_step_handler(message, register_step1, id)

#-------------------------------------------------------------------------------ЗНАКОМСТВО С ИГРОЙ
def register_step1(message, id):
    name = message.text
    text = f'{name}, другое дело!\nИмя доброе, а главное православное.'
    text2 = 'А теперь скажи пару слов о себе и о своей истории чтобы другие герои могли лучше понимать кто ты.'
    bot.send_message(id, text)
    bot.send_message(id, text2)
    bot.register_next_step_handler(message, register_step2, id, name)

def register_step2(message, id, name):
    bio = message.text
    data.create_new_hero(id, name, message.from_user.first_name, message.from_user.username, info=bio)
    text = 'Не бойся, у тебя будет возможность изменить свое имя и био'
    text2 = f'А пока у меня к тебе главный вопрос\n{name} ты готов к приключениям?'
    bot.send_message(id, text)
    bot.send_message(id, text2, reply_markup=buttons.lesgooo())
    bot.register_next_step_handler(message, register_step3, id)

def register_step3(message, id):
    if message.text == 'Вперед, я готов!':
        bot.send_message(id, 'Покажи богам чего ты достоин', reply_markup=buttons.pon('', ""))
        bot.register_next_step_handler(message, register_step4, id)
    elif message.text == 'Можно я пойду домой?':
        bot.send_message(id, 'ХАХАХА КОНЕЧНО НЕТ, вперед вперед!', reply_markup=buttons.pon('ОК🗿', "Зачем спрашивать?"))
        bot.register_next_step_handler(message, register_step4, id)

def register_step4(message, id):
    bot.send_message(id, 'Ты здесь новенький, по этому давай проведу небольшой экскурс')
    bot.send_message(id, 'В разделе "Помощь" ты сможешь ознакомится со всеми правилами этого мира')
    bot.send_message(id, 'Так что давай начнем сразу с подземелья', reply_markup=buttons.begin_dungeon())
    bot.register_next_step_handler(message, begin_dungeon, id)
#------------------------------------------------------------------------------ГЛАВНОЕ МЕНЮ

@bot.message_handler(content_types= ['text'])
def heroes_menu(message):

    if message.text == '⚔️ Данж ⚔️':
        data.exist_fight(message.from_user.id)
        if data.hero_info(message.from_user.id)[4] < 0:
            bot.send_message(message.from_user.id, 'Пройди это первый раз', reply_markup=buttons.begin_dungeon())
            bot.register_next_step_handler(message, dungeon_start)
        else:
            bot.send_message(message.from_user.id, 'Подземелье - место где тебя не услышат боги',
                             reply_markup=buttons.dungeon(message.from_user.id))
            bot.register_next_step_handler(message, dungeon)

    elif message.text == '💼Инвентарь':
        bot.send_message(message.from_user.id, 'Густав протягиват вам вашу сумку', reply_markup=buttons.pokaz())
        bot.register_next_step_handler(message, invent)

    elif message.text == 'Обо мне':
        id = message.from_user.id
        user = data.hero_info(id)
        bot.send_message(id, 'Информация о тебе:', reply_markup=buttons.about_me())
        bot.send_message(id, f'Твое имя: *{user[1]}*\nМедали: *{user[8]}*\nСила: *{user[6]}*\nМин-Шанс: '
                             f'*{user[5]}*%\nУровень: *{user[4]}*\nБио: {user[7]}', parse_mode='Markdown')
        bot.register_next_step_handler(message, me_info)

    elif message.text == '❓Помощь':
        keyboard = telebot.types.InlineKeyboardMarkup()
        url_button = telebot.types.InlineKeyboardButton(text="Зайти в зал Тот'а", url="https://telegra.ph/Geroi-Olimpa-11-23")
        keyboard.add(url_button)
        bot.send_message(message.from_user.id, 'Тот - бог знаний, дает тебе возможность узнать секреты мироздания',
                         reply_markup=keyboard)

    elif message.text == '⛪️Храм Богов':
        bot.send_message(message.from_user.id,
                         '*Храм богов* - священное место где каждый смертный может найти связь с богами',
                         parse_mode='Markdown', reply_markup=buttons.hram())
        bot.register_next_step_handler(message, hram_shop)

    elif message.text == 'Друзья':
        bot.send_message(message.from_user.id,
                         random.choice(('А вот твои друзья ходят в бар', 'Новые знакомства всегда хорошо',
                                        'Это что, средневековая соц сеть?')),
                         reply_markup=buttons.friends())
        bot.register_next_step_handler(message, friends)

    elif message.text == 'Админ' and message.from_user.id == 67821449:
        bot.send_message(message.from_user.id, 'Опять ты, что на этот раз?', reply_markup=buttons.admin())
        bot.register_next_step_handler(message, admin)

#--------------------------------------------------------------------------------------ДАНЖ

def dungeon(message):
    txt = message.text
    id = message.from_user.id
    data.exist_fight(id)
    if txt == f'Уровень {data.hero_info(id)[4]}':
        bot.send_message(id, 'Если что, я тебя вытащю', reply_markup=buttons.vper())
        bot.register_next_step_handler(message, dungeon_start)
    elif txt == 'Зал Афины' and data.hero_info(id)[4] >= 10:
        bot.send_message(id, 'Зал Афины - за каждый спаринг с воином богини вы получите 1 медаль',
                         reply_markup=buttons.afina())
        bot.register_next_step_handler(message, afina)
    elif txt == 'Вернуться назад':
        bot.send_message(id, 'Ну и славненько, пошли в бар', reply_markup=buttons.start_buttons())

def dungeon_start(message):
    id = message.from_user.id
    lvl = data.hero_info(id)[4]
    if lvl <= 0:
        bot.send_message(id, 'Не прошел обучение, как мило, давай заново', reply_markup=buttons.pon('Так у меня с самого начала не было выбора', "Хехе"))
        bot.register_next_step_handler(message, begin_dungeon, id)
    else:
        enemy = random.choice(mobs.mobs)
        en = lvl * (lvl * 0.2)
        enemy_power = round(en)
        enemy_hp = 120 * (lvl * 0.2)
        hp = data.hero_info(id)[6] * (lvl * 0.2)

        data.fight(id, round(hp), enemy["name"], round(enemy_hp))

        text = f'Сила врагов на уровне - {enemy_power}'
        bot.send_message(id, text, reply_markup=buttons.lesgo())
        bot.register_next_step_handler(message, dungeon_start_fight, id, enemy, enemy_power)

def dungeon_start_fight(message, id, enemy, enemy_power):
    if message.text == 'Вперед!':
        text = f'На вас напал {enemy["name"]}'
        hp_info = f'Ваше HP: {data.get_fight_info(id)[1]}\n' \
               f'{data.get_fight_info(id)[2]}: {data.get_fight_info(id)[3]}'
        bot.send_message(id, text, reply_markup=buttons.atac())
        bot.send_message(id, hp_info)
        bot.register_next_step_handler(message, fight, id, enemy, enemy_power)
    elif message.text == 'Я передумал':
        bot.send_message(id, 'Густав телепортировал вас назад', reply_markup=buttons.start_buttons())

def fight(message, id, enemy, enemy_power):
    min = data.hero_info(id)[5] * (data.hero_info(id)[6] / 100)
    damage = random.randint(min, data.hero_info(id)[6])
    damage_enemy = random.randint(0, enemy_power)
    data.fight_minus_hp(id, 'hp', damage_enemy)
    data.fight_minus_hp(id, 'enemy_hp', damage)
    if data.get_fight_info(id)[3] > 0 and data.get_fight_info(id)[1] > 0:
        if message.text == 'Атаковать':
            text = f'Вы наносите врагу *{damage}* единиц урона\n' \
                   f'Враг использует {random.choice(enemy["attacks"])}\n' \
                   f'Тем самы нанося вам  *{damage_enemy}* единиц урона' \
                   f'{enemy["name"]} говорит: {random.choice(enemy["speak"])}\n\n' \
                   f'Ваше HP: {data.get_fight_info(id)[1]}         HP Врага: {data.get_fight_info(id)[3]}'
            bot.send_message(id, text, parse_mode='Markdown')
            bot.register_next_step_handler(message, fight, id, enemy, enemy_power)
        elif message.text == 'Сдаться':
            data.exist_fight(id)
            bot.send_message(id, 'Не падай духом', reply_markup=buttons.start_buttons())

        else:
            bot.send_message(id, 'Не время отвлекаться')
            bot.register_next_step_handler(message, fight, id, enemy, enemy_power)
    elif data.get_fight_info(id)[3] <= 0:
        data.exist_fight(id)
        data.winner_winner(id, 2)
        if data.hero_info(id)[4] == 10:
            bot.send_message(id, 'Афина поражена вашими успехами в подземелье, и просит вас тренировать ее солдат\n\n'
                                 'За каждый спаринг с воином Афин вы получите 1 медаль')
        bot.send_message(id, f'Вы нанесли финальные {damage} единиц урона и убили врага!\n'
                         f'Боги благодарны вам за сделанную работу и одарили вас *2 медалями*!',
                         reply_markup=buttons.start_buttons(), parse_mode='Markdown')
    else:
        bot.send_message(id, '*Густав перемещает вас в последний момент на поверхность*', parse_mode='Markdown')
        bot.send_message(id, 'В следующий раз будь осторожнее', reply_markup=buttons.start_buttons())

def begin_dungeon(message, id):
    bot.send_message(id, "Сейчас мы на самой верхушке подземелья")
    bot.send_message(id, "Главное помнить - чем выше уровень, тем сильнее враги",
                     reply_markup=buttons.pon('Мне страшно', "Как драться?"))
    bot.register_next_step_handler(message, begin_dungeon2, id)

def begin_dungeon2(message, id):
    if message.text == 'Мне страшно':
        bot.send_message(id, 'Понимаю, с таким именем мне бы тоже было страшно')
        bot.send_message(id, 'Но поворачивать назад уже поздно')
        bot.send_message(id, 'В двух словах, бой зависит от твоей удачи, ладно это уже четые слов',
                         reply_markup=buttons.pon("Никогда не поздно", "Их было пять..."))
        bot.register_next_step_handler(message, begin_dungeon3, id)

    elif message.text == 'Как драться?':
        bot.send_message(id, 'Хороший вопрос, ответ еще лучше - с Божьей помощью')
        bot.send_message(id, 'Сила твоего удара зависит от твоей максимальной силы и удачи',
                         reply_markup=buttons.pon("Ясно, мне конец", "Внушает доверие"))
        bot.register_next_step_handler(message, begin_dungeon3, id)

def begin_dungeon3(message, id):
    bot.send_message(id, 'А вот и подходящая цель!')
    bot.send_message(id, 'На вас напал демон')
    bot.send_message(id, 'Ваше HP - 10\nДемон - 10', reply_markup=buttons.pon('Атаковать', 'Плакать'))
    bot.register_next_step_handler(message, begin_dungeon4, id)

def begin_dungeon4(message, id):
    if message.text == 'Плакать':
        bot.send_message(id, 'Слезами горю не поможешь, атакуй')
        bot.register_next_step_handler(message, begin_dungeon4, id)
    elif message.text == 'Атаковать':
        text = f'Вы наносите врагу *5* единиц урона\n' \
                       f'Враг использует удар рукой\n' \
                       f'Тем самы нанося вам  1 единиц урона\n' \
                       f'Демон говорит: ταλαιπωρία\n\n' \
                       f'Ваше HP: 9        HP Врага: 5'
        bot.send_message(id, text, parse_mode='Markdown')
        bot.send_message(id, f'Так держать, {data.hero_info(id)[1]}', reply_markup=buttons.pon('Атаковать', "Да я не хочу драться"))
        bot.register_next_step_handler(message, begin_dungeon5, id)
    else:
        bot.send_message(id, 'Не отвлекайся')
        bot.register_next_step_handler(message, begin_dungeon4, id)

def begin_dungeon5(message, id):
    if message.text == 'Да я не хочу драться' or message.text == 'Атаковать':
        if message.text == 'Да я не хочу драться':
            bot.send_message(id, 'А придется')
            bot.register_next_step_handler(message, begin_dungeon5, id)
        else:
            bot.send_message(id, 'Вот это сила духа')
            text = f'Вы нанесли финальные 5 единиц урона и убили врага!'
            bot.send_message(id, text)
            bot.send_message(id, f'Так держать, {data.hero_info(id)[1]}',
                             reply_markup=buttons.pon('Спасибо', "Я так понимаю у меня и дальше не будет выбора"))
            bot.register_next_step_handler(message, begin_dungeon6, id)
    else:
        bot.send_message(id, 'Не отвлекайся')
        bot.register_next_step_handler(message, begin_dungeon5, id)

def begin_dungeon6(message, id):
    data.winner_winner(id, 0)
    if message.text == "Я так понимаю у меня и дальше не будет выбора":
        bot.send_message(id, 'Ты правильно понимаешь')
    bot.send_message(id, 'В следующий раз ты будешь здесь один, а я буду наверху чтобы в случае чего тебя вытащить')
    bot.send_message(id, 'Ну а пока у меня все, если у тебя есть какие-то вопросы ты можешь обращаться в "Помощь"', reply_markup=buttons.start_buttons())


def afina(message):
    id = message.from_user.id
    lvl = data.hero_info(id)[4]
    enemy = random.choice(mobs.afins)
    en = lvl * (lvl * 0.1)
    enemy_power = round(en)
    enemy_hp = 120 * (lvl * 0.2)
    hp = data.hero_info(id)[6] * (lvl * 0.2)

    data.fight(id, round(hp), enemy["name"], round(enemy_hp))

    text = f'С вами в спаринг встал {enemy["name"]}'
    hp_info = f'Ваше HP: {data.get_fight_info(id)[1]}\n' \
              f'{data.get_fight_info(id)[2]}: {data.get_fight_info(id)[3]}'
    bot.send_message(id, text, reply_markup=buttons.atac())
    bot.send_message(id, hp_info)
    bot.register_next_step_handler(message, afins_fight, id, enemy, enemy_power)

def afins_fight(message, id, enemy, enemy_power):
    min = data.hero_info(id)[5] * (data.hero_info(id)[6] / 100)
    damage = random.randint(min, data.hero_info(id)[6])
    damage_enemy = random.randint(0, enemy_power)
    data.fight_minus_hp(id, 'hp', damage_enemy)
    data.fight_minus_hp(id, 'enemy_hp', damage)

    if data.get_fight_info(id)[3] > 0 and data.get_fight_info(id)[1] > 0:
        if message.text == 'Атаковать':
            text = f'Вы наносите врагу *{damage}* единиц урона\n' \
                   f'Враг использует {random.choice(enemy["attacks"])}\n' \
                   f'Тем самы нанося вам  *{damage_enemy}* единиц урона' \
                   f'{enemy["name"]} говорит: {random.choice(enemy["speak"])}\n\n' \
                   f'Ваше HP: {data.get_fight_info(id)[1]}         HP Врага: {data.get_fight_info(id)[3]}'
            bot.send_message(id, text, parse_mode='Markdown')
            bot.register_next_step_handler(message, afins_fight, id, enemy, enemy_power)
        elif message.text == 'Сдаться':
            data.exist_fight(id)
            bot.send_message(id, 'НА сегодня хватит тебе спарингов', reply_markup=buttons.start_buttons())

        else:
            bot.send_message(id, 'Не время отвлекаться')
            bot.register_next_step_handler(message, afins_fight, id, enemy, enemy_power)
    elif data.get_fight_info(id)[3] <= 0:
        data.exist_fight(id)
        data.send_medals(id, 1)
        bot.send_message(id, f'Вы нанесли финальные {damage} единиц урона и повалили врага!\n'
                             f'Афина благодарна вам за мастер класс и даровала вам *1 медаль*!',
                         reply_markup=buttons.start_buttons(), parse_mode='Markdown')
    else:
        bot.send_message(id, '*Вы падаете на землю*', parse_mode='Markdown')
        bot.send_message(id, 'Ученик превзошел учителя', reply_markup=buttons.start_buttons())



#--------------------------------------------------------------------------------------ОБО МНЕ

def me_info(message):
    id = message.from_user.id

    if message.text == 'Изменить имя':
        bot.send_message(id, random.choice(('Пришли новое имя', "Давно этого ждал, на что меняем?",
                                            "Все что угодно кроме прошлого, слушаю новый вариант")),
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, change_name, id)

    elif message.text == 'Изменить био':
        bot.send_message(id, random.choice(('Пришли новое био', "А мне нравилось старое, на что заменим?",
                                            "Давно хотел его поменять")),
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, change_bio ,id)

    elif message.text == 'Вернуться назад':
        bot.send_message(id, 'Да норнальное у тебя имя, пошли в данж', reply_markup=buttons.start_buttons())
    else:
        bot.register_next_step_handler(message, me_info,id)

def change_name(message, id):
    data.change_name(id, message.text)
    bot.send_message(id, f'{message.text}, хорошее имя', reply_markup=buttons.about_me())
    bot.register_next_step_handler(message, me_info)

def change_bio(message, id):
    data.change_bio(id, message.text)
    bot.send_message(id, f'Информативно', reply_markup=buttons.about_me())
    bot.register_next_step_handler(message, me_info)

#--------------------------------------------------------------------------------------ИНВЕНТАРЬ

def invent(message):
    id = message.from_user.id
    inv = data.get_invent(id)
    try:
        invent = []
        text = 'Инвентарь:\n\n'
        for x in inv:
            for i in mobs.gods:
                for god in i['type']:
                    if god == x:
                        invent.append(i['name'])
        gods_count = {}.fromkeys(invent, 0)
        for a in invent:
            gods_count[a] += 1
        for i in gods_count.keys():
            text += f'*Руна*, {gods_count[i]} шт, хозяин {i}\n'
        bot.send_message(id, text, reply_markup=buttons.start_buttons(), parse_mode='Markdown')
    except:
        bot.send_message(id, 'Инвентарь:', reply_markup=buttons.start_buttons())


#--------------------------------------------------------------------------------------ХРАМ БОГОВ

def hram_shop(message):
    id = message.from_user.id
    txt = message.text

    if txt in [x['name'] for x in mobs.gods]:
        for god in mobs.gods:

            if god['name'] == txt:
                type = god['type']
                cos = god['medals']
                up = god['bonus']
                text = f'*Хозяин руны - {god["name"]}*\n\n' \
                       f'*О боге:*\n{god["info"]}\n\n' \
                       f'*Бонус рун:*\n{god["bonus_info"]}\n\n' \
                       f'*Стоимость Руны*: {god["medals"]} медалей\n\n' \
                       f'*Есть*: {data.hero_info(id)[9].count(god["type"])}              ' \
                       f'*Медали*: {data.hero_info(id)[8]}'
                bot.send_message(id, text, parse_mode='Markdown', reply_markup=buttons.hram_buy(god["medals"]))
                bot.register_next_step_handler(message, hram_buy, type, cos, up)

    elif txt == 'Вернуться в меню':
        bot.send_message(id, random.choice(('Я тоже недолюбливаю это место', 'У меня получилось заманить тебя в бар?',
                                            'Пошли отсюда пока Зевс меня не увидел, я украл его тапочки',
                                            'Молиться? Нет спасибо', 'А Афродита обо мне спрашивала?',
                                            'Что? Когда? А, послышалось', 'Зевс больше думает о своей бороде чем о людях',
                                            '')),
                         reply_markup=buttons.start_buttons())
    else:
        bot.send_message(message.from_user.id, 'такого бога нет')
        bot.register_next_step_handler(message, hram_shop)

def hram_buy(message, type, cos, up):
    id = message.from_user.id
    txt = message.text

    if txt == f'Купить Руну за {cos} медалей':

        if data.hero_info(id)[8] >= cos:

            if type == 'G' and data.hero_info(id)[9].count(type) >= 1 or type == 'B' and data.hero_info(id)[9].count(type) >= 3:
                bot.send_message(id, 'Привышен лимит рун', reply_markup=buttons.hram())
                bot.register_next_step_handler(message, hram_shop)

            else:
                data.buy(id, cos, type, up)
                bot.send_message(id, 'Руна куплена, боги одарили вас своим вниманием', reply_markup=buttons.hram())
                bot.register_next_step_handler(message, hram_shop)
        else:
            bot.send_message(id, 'Не хватает медалей', reply_markup=buttons.hram())
            bot.register_next_step_handler(message, hram_shop)

    elif txt == 'Вернуться в Храм':
        bot.send_message(id, 'Опять в храм?', reply_markup=buttons.hram())
        bot.register_next_step_handler(message, hram_shop)

    else:
        bot.register_next_step_handler(message, hram_buy, type, cos, up)

#-------------------------------------------------------------------------------------ДРУЗЬЯ

def friends(message):
    id = message.from_user.id
    txt = message.text
    data.check_friends(id)

    if txt == 'Добавить':
        bot.send_message(id, 'Не забывай: Когда ты оправляешь запрос на дружбу, человек видит твой реальный id')
        if data.hero_info(id)[10] >= 5:
            bot.send_message(id, 'К сожалению лимит друзей 5 человек')
            bot.register_next_step_handler(message, friends)

        else:
            bot.send_message(id, 'Отправь  telegram id своейго друга', reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, friends_add, id)

    elif txt == 'Показать':
        all = data.show_all_friends(id)
        text = f'\n*{random.choice(("Вот они, слева направо:", "Твои друзья:", "Кроме меня у тебя есть:","Люди с которыми лучше не пить:"))}*\n\n\n'
        for i in all:
            her = data.hero_info(i)
            text+=f'Имя: {her[1]}\nУровень: {her[5]}\nМаксимальная сила: {her[6]}\n' \
                  f'био: {her[7]}\n----------------------------\n'
        bot.send_message(id, text, parse_mode='Markdown')
        bot.register_next_step_handler(message, friends)

    elif txt == 'Удалить':
        bot.send_message(id, 'Кто больше не достоин нашей друэжбы?', reply_markup=buttons.friends_message(id))
        bot.register_next_step_handler(message, delite_friends, id)

    elif txt == 'Cообщение':
        bot.send_message(id, 'Кому передать?', reply_markup=buttons.friends_message(id))
        bot.register_next_step_handler(message, friends_message, id)

    elif txt == 'Вернуться назад':
        bot.send_message(id, 'Друзья подождут, пошли убивать монстров', reply_markup=buttons.start_buttons())

    else:
        bot.register_next_step_handler(message, friends)


def friends_add(message, id):
    try:
        friend = int(message.text)

        try:
            if data.exist_friend(id, friend):
                bot.send_message(id, 'Вы уже дружите', reply_markup=buttons.friends())
            else:
                if data.hero_info(friend)[10] >= 5:
                    bot.send_message(id, random.choice(('У твоего друга слишком много друзей, лимит превышен',
                                                        'Не хватает места в его сердечке, у него превышен лимит друзей',
                                                        "Лимит друзей привышен, как печально, пошли лучше в бар")),
                                     reply_markup=buttons.friends())
                else:

                    text = F'*{data.hero_info(id)[1]} хочет с тобой дружить*\n' \
                           F'Био - {data.hero_info(id)[7]}\n' \
                           F'ID - {data.hero_info(id)[0]}'

                    bot.send_message(friend, text, reply_markup=buttons.friend_accept(), parse_mode='Markdown')
                    bot.send_message(id, 'Запрос в друзья отправлен', reply_markup=buttons.start_buttons())

        except:
            bot.send_message(id, 'Не получилось, в принципе не страшно, и без друзей как-то жили', reply_markup=buttons.friends())
    except:
        bot.send_message(id, 'Айди это цифры', reply_markup=buttons.friends())
        bot.register_next_step_handler(message, friends)

def delite_friends(message, id):
    friend = message.text
    if data.all_heroes_by_name(message.text):

        if friend == data.hero_info(data.if_name_in_friends(id, friend))[1]:
            id2 = data.if_name_in_friends(id, friend)
            bot.send_message(id, 'Удаляем?', reply_markup=buttons.delele_fb())
            bot.register_next_step_handler(message, accept_deleting, id2, id)

        else:
            bot.send_message(id, 'Он не является вашим другом', reply_markup=buttons.friends())
            bot.register_next_step_handler(message, friends)
    else:
        bot.send_message(id, 'Такого героя нет', reply_markup=buttons.friends())
        bot.register_next_step_handler(message, friends)

def accept_deleting(message, id2, id):
    txt = message.text
    if txt == 'Он не достоин!' or txt == 'Да!':
        data.deleting(id, id2)
        bot.send_message(id, 'Он мне никогда не нравился', reply_markup=buttons.friends())
        bot.register_next_step_handler(message, friends)
    elif txt == 'Я думаю он исправится' or txt == 'Конечно нет!':
        bot.send_message(id, 'Ваш друг помилован', reply_markup=buttons.friends())
        bot.register_next_step_handler(message, friends)

def friends_message(message, id):
    to_friend = message.text
    if data.all_heroes_by_name(message.text):
        for i in data.show_all_friends(id):
            if data.hero_info(i)[1] == to_friend:
                bot.send_message(id, 'Что передать?', reply_markup=telebot.types.ReplyKeyboardRemove())
                bot.register_next_step_handler(message, send_friend_message, i, id)
    else:
        bot.send_message(id, 'Такого героя нет', reply_markup=buttons.friends())
        bot.register_next_step_handler(message, friends)

def send_friend_message(message, i, id):
    text = f'*{data.hero_info(id)[1]} передал*: {message.text}'
    try:
        bot.send_message(i, text, parse_mode='Markdown')
        bot.send_message(id, 'Передал', reply_markup=buttons.friends())
        bot.register_next_step_handler(message, friends)

    except:
        bot.send_message(id, 'Не получилось', reply_markup=buttons.friends())
        bot.register_next_step_handler(message, friends)




@bot.callback_query_handler(func=lambda call: True)
def friend_accept(call):
    if call.data == 'yes':

        x = str(call.message)
        y = x[x.find('ID -')+5:]
        id1 = y.split("',")[0]
        id2 = call.from_user.id
        data.check_friends(id2)
        data.adding_friends(int(id1), id2)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=random.choice(('Новый друг добавлен', "Может хотя бы он будет пить?")))
        bot.send_message(int(id1), f'{data.hero_info(id2)[1]} принял ваш запрос на дружбу')

    elif call.data == 'no':

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=random.choice(('На нет и суда нет', "Кто это вообще был?", "Даааа, только ты и я",
                                                  "Думаю он сейчас где-то плачет")))
#------------------------------------------------------------------------------------АДМИН ПАНЕЛЬ

def admin(message):
    id = message.from_user.id
    x = message.text
    if x == 'Удалить юзера':
        bot.send_message(id, 'Отправь id для удаления', reply_markup=buttons.otmena())
        bot.register_next_step_handler(message, delite_ad)
    elif x == 'Отправить медали':
        bot.send_message(id, 'Отправь id для добавления', reply_markup=buttons.otmena())
        bot.register_next_step_handler(message, medals_admin)
    elif x == 'Сколько юзеров':
        bot.send_message(id, f'В базе {data.get_all_admin_users()} человек')
        bot.register_next_step_handler(message, admin)
    elif x == 'Инфа по id':
        bot.send_message(id, 'Отправьте id чтобы его проверить', reply_markup=buttons.otmena())
        bot.register_next_step_handler(message, check_admin)
    elif x == 'Назад в меню':
        bot.send_message(id, 'Ок', reply_markup=buttons.start_buttons())

def delite_ad(message):

    if message.text == "Отмена":
        bot.send_message(message.from_user.id, 'Оке', reply_markup=buttons.admin())
        bot.register_next_step_handler(message, admin)
    else:
        try:
            id = int(message.text)
            if data.check_hero_db(id):
                data.admin_delite(id)
                bot.send_message(message.from_user.id, 'удален', reply_markup=buttons.admin())
                bot.register_next_step_handler(message, admin)
        except:
            bot.send_message(message.from_user.id, 'Не понимаю', reply_markup=buttons.admin())
            bot.register_next_step_handler(message, admin)

def medals_admin (message):
    if message.text == "Отмена":
        bot.send_message(message.from_user.id, 'Оке', reply_markup=buttons.admin())
        bot.register_next_step_handler(message, admin)
    else:
        try:
            id = int(message.text)
            if data.check_hero_db(id):
                bot.send_message(message.from_user.id, 'Сколько отправляем')
                bot.register_next_step_handler(message, medals_admin_sum, id)
            else:
                bot.send_message(message.from_user.id, 'Такого нет')
                bot.register_next_step_handler(message, admin)
        except:
            bot.send_message(message.from_user.id, 'Не понимаю', reply_markup=buttons.admin())
            bot.register_next_step_handler(message, admin)

def medals_admin_sum(message, id):
    if message.text == "Отмена":
        bot.send_message(message.from_user.id, 'Оке', reply_markup=buttons.admin())
        bot.register_next_step_handler(message, admin)
    else:
        try:
            sum = int(message.text)
            data.send_medals(id, sum)
            bot.send_message(message.from_user.id, 'Отправил', reply_markup=buttons.admin())
            bot.send_message(id, f'Боги подарили вам {sum} медалей')
            bot.register_next_step_handler(message, admin)
        except:
            bot.send_message(message.from_user.id, 'Не понял', reply_markup=buttons.admin())
            bot.register_next_step_handler(message, admin)

def check_admin(message):
    if message.text == "Отмена":
        bot.send_message(message.from_user.id, 'Оке', reply_markup=buttons.admin())
        bot.register_next_step_handler(message, admin)
    else:
        try:
            id = int(message.text)
            x = data.hero_info(id)
            bot.send_message(message.from_user.id, f'id - {x[0]}\n'
                                                   f'name - {x[1]}\n'
                                                   f'real name - {x[2]}\n'
                                                   f' user - {x[3]}\n'
                                                   f'lvl - {x[4]}\n'
                                                   f'min_power - {x[5]}\n'
                                                   f'max_power - {x[6]}\n'
                                                   f'\info - {x[7]}\n'
                                                   f'medals - {x[8]}\n'
                                                   f'invent - {x[9]}\n'
                                                   f'frinds - {x[10]}',
                             reply_markup=buttons.admin())
            bot.register_next_step_handler(message, admin)
        except:
            bot.send_message(message.from_user.id, 'Не понял', reply_markup=buttons.admin())
            bot.register_next_step_handler(message, admin)





bot.polling(none_stop=True)