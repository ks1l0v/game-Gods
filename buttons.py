from telebot import types
import mobs
from data import show_all_friends, hero_info
def start_buttons():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    dungeon = types.KeyboardButton('⚔️ Данж ⚔️')
    invent = types.KeyboardButton('💼Инвентарь')
    me = types.KeyboardButton('Обо мне')
    help = types.KeyboardButton('❓Помощь')
    hram = types.KeyboardButton('⛪️Храм Богов')
    friends = types.KeyboardButton('Друзья')

    kb.row(dungeon)
    kb.add(invent, me, help, hram, friends)

    return kb
def hram():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    retur = types.KeyboardButton('Вернуться в меню')
    kb.add(retur)
    for i in mobs.gods:
        kb.add(i['name'])
    return kb

def hram_buy(cos):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    buy = types.KeyboardButton(f'Купить Руну за {cos} медалей')
    exit = types.KeyboardButton('Вернуться в Храм')
    kb.add(buy, exit)
    return kb

def lesgooo():
    kb = types.ReplyKeyboardMarkup()

    go = types.KeyboardButton('Вперед, я готов!')
    noo = types.KeyboardButton('Можно я пойду домой?')
    kb.add(go, noo)

    return kb

def about_me():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    go = types.KeyboardButton('Изменить имя')
    noo = types.KeyboardButton('Изменить био')
    no = types.KeyboardButton('Вернуться назад')
    kb.add(go, noo)
    kb.row(no)

    return kb

def friends():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    g = types.KeyboardButton('Добавить')
    n = types.KeyboardButton('Показать')
    w = types.KeyboardButton('Удалить')
    o = types.KeyboardButton('Cообщение')
    b = types.KeyboardButton('Вернуться назад')

    kb.add(g, n, w, o)
    kb.row(b)
    return kb

def friend_accept():
    rep = types.InlineKeyboardMarkup()

    yes = types.InlineKeyboardButton(text='Принять', callback_data='yes')
    no = types.InlineKeyboardButton(text='Отказать', callback_data='no')

    rep.add(yes, no)

    return rep

def friends_message(id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in show_all_friends(id):
        kb.add(hero_info(i)[1])
    retur = types.KeyboardButton('Вернуться назад')
    kb.add(retur)
    return kb

def delele_fb():
    kb = types.ReplyKeyboardMarkup(row_width=2)

    go = types.KeyboardButton('Да!')
    go2 = types.KeyboardButton('Он не достоин!')
    noo = types.KeyboardButton('Я думаю он \nисправится')
    noo3 = types.KeyboardButton('Конечно нет!')
    kb.add(go, noo, go2, noo3)

    return kb

def dungeon(id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    go = types.KeyboardButton(f'Уровень {hero_info(id)[4]}')
    kb.add(go)
    if hero_info(id)[4] >= 10:
        afina = types.KeyboardButton(f'Зал Афины')
        kb.add(afina)
    menu = types.KeyboardButton('Вернуться назад')
    kb.add(menu)

    return kb

def begin_dungeon():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    go = types.KeyboardButton('Уровень 0')
    kb.add(go)

    return kb

def lesgo():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    go = types.KeyboardButton('Вперед!')
    nah = types.KeyboardButton('Я передумал')
    kb.add(go, nah)

    return kb
def atac():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    go = types.KeyboardButton('Атаковать')
    no = types.KeyboardButton('Сдаться')
    kb.add(go, no)

    return kb

def pon(question1, question2):
    kb = types.ReplyKeyboardMarkup()

    go = types.KeyboardButton(question1)
    go2 = types.KeyboardButton(question2)
    kb.add(go, go2)

    return kb

def admin():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    go = types.KeyboardButton('Удалить юзера')
    go1 = types.KeyboardButton('Отправить медали')
    go4 = types.KeyboardButton("Сколько юзеров")
    go5 = types.KeyboardButton("Инфа по id")
    go6 = types.KeyboardButton("Назад в меню")
    kb.add(go, go1, go4, go5, go6)

    return kb

def otmena():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    go = types.KeyboardButton('Отмена')
    kb.add(go)

    return kb

def pokaz():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    go = types.KeyboardButton('Посмотреть в инвентарь')
    kb.add(go)
    return kb

def vper():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    go = types.KeyboardButton('Спуститься в дажн')
    kb.add(go)
    return kb

def afina():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    go = types.KeyboardButton('Войти в зал Афины')
    kb.add(go)
    return kb