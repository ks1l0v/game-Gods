import sqlite3

connection = sqlite3.connect('data.db')
sql = connection.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS heroes ('
            'id INTEGER,'
            'name TEXT,'
            'real_name TEXT,'
            'user TEXT,'
            'lvl INTEGER,'
            'min_power INTEGER,'
            'max_power INTEGER,'
            'info TEXT,'
            'medals INTEGER,'
            'invent TEXT,'
            'friends INTEGER)')

sql.execute('CREATE TABLE IF NOT EXISTS friends ('
            'id INTEGER,'
            'f1 INTEGER,'
            'f2 INTEGER,'
            'f3 INTEGER,'
            'f4 INTEGER,'
            'f5 INTEGER)'
            )

sql.execute('CREATE TABLE IF NOT EXISTS fight ('
            'id INTEGER,'
            'hp INTEGER,'
            'enemy TEXT,'
            'enemy_hp INTEGER)')

def check_hero_db(id):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT id FROM heroes WHERE id=?', (id,)).fetchone()

    if checker:
        return True
    else:
        return False

def create_new_hero(id, name, real_name, user, lvl=0, min_power=0, max_power=50, info=None, medals=0, invent=0, friends=0):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO heroes VALUES(?,?,?,?,?,?,?,?,?,?,?)', (id, name, real_name, user, lvl, min_power, max_power, info, medals, invent, friends))
    connection.commit()

def hero_info(id):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    info = sql.execute('SELECT * FROM heroes WHERE id=?', (id,)).fetchone()
    return info

def buy(id, cos, what, up):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    old_med = sql.execute('SELECT medals FROM heroes WHERE id=?', (id,)).fetchone()
    sql.execute('UPDATE heroes SET medals =? WHERE id=?', (old_med[0]-cos, id))

    old_inv = sql.execute('SELECT invent FROM heroes WHERE id=?', (id,)).fetchone()
    sql.execute('UPDATE heroes SET invent =? WHERE id=?', (old_inv[0]+what, id))

    if type(up) == str:
        old_pow = sql.execute('SELECT min_power FROM heroes WHERE id=?', (id,)).fetchone()
        new_pow = old_pow[0] + int(up)
        sql.execute('UPDATE heroes SET min_power =? WHERE id=?', (new_pow, id))
    else:
        old_pow = sql.execute('SELECT max_power FROM heroes WHERE id=?', (id,)).fetchone()
        new_pow = old_pow[0] + up
        sql.execute('UPDATE heroes SET max_power =? WHERE id=?', (new_pow, id))
    connection.commit()

def check_friends(id, f1=0, f2=0, f3=0, f4=0, f5=0):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT id FROM friends WHERE id=?', (id,)).fetchone()

    if checker:
        pass
    else:
        sql.execute('INSERT INTO friends VALUES(?,?,?,?,?,?)', (id, f1, f2, f3, f4, f5))
        connection.commit()

def adding_friends(id1, id2):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    old_f = sql.execute('SELECT friends FROM heroes WHERE id=?', (id1,)).fetchone()
    new_f1 = old_f[0] + 1
    old_f = sql.execute('SELECT friends FROM heroes WHERE id=?', (id2,)).fetchone()
    new_f2 = old_f[0] + 1

    sql.execute('UPDATE heroes SET friends =? WHERE id=?', (new_f1, id1))
    sql.execute('UPDATE heroes SET friends =? WHERE id=?', (new_f2, id2))
    sql.execute(f'UPDATE friends SET {f"f{new_f1}"}=? WHERE id=?', (id2, id1))
    sql.execute(f'UPDATE friends SET {f"f{new_f2}"}=? WHERE id=?', (id1,id2))

    connection.commit()

def exist_friend(id, id2):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT * FROM friends WHERE id=?', (id,)).fetchone()
    if id2 in checker:
        return True
    else:
        return False

def show_all_friends(id):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    info = sql.execute('SELECT f1, f2, f3, f4, f5 FROM friends WHERE id=?', (id,)).fetchone()
    actual = []
    for i in info:
        if i != 0:
            actual.append(i)
    return actual

def all_heroes_by_name(name):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    info = sql.execute('SELECT id FROM heroes WHERE name=?', (name,)).fetchone()
    if info:
        return True
    else:
        return False

def if_name_in_friends(id, name):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    x = show_all_friends(id)
    info = sql.execute('SELECT id FROM heroes WHERE name=?', (name,)).fetchone()
    for i in info:
        if i in x:
            return i

def deleting(id1, id2):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    old_f = sql.execute('SELECT friends FROM heroes WHERE id=?', (id1,)).fetchone()
    new_f1 = old_f[0] - 1
    old_f = sql.execute('SELECT friends FROM heroes WHERE id=?', (id2,)).fetchone()
    new_f2 = old_f[0] - 1

    sql.execute('UPDATE heroes SET friends =? WHERE id=?', (new_f1, id1))
    sql.execute('UPDATE heroes SET friends =? WHERE id=?', (new_f2, id2))

    sql.execute(f'UPDATE friends SET {f"f{show_all_friends(id1).index(id2) + 1}"}=? WHERE id=?', (0, id1))
    sql.execute(f'UPDATE friends SET {f"f{show_all_friends(id2).index(id1) + 1}"}=? WHERE id=?', (0, id2))

    connection.commit()

def fight(id, hp, enemy, enemy_hp):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    sql.execute('INSERT INTO fight VALUES(?,?,?,?)', (id, hp, enemy, enemy_hp))
    connection.commit()

def fight_minus_hp(id, whom, pov):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    old_hp = sql.execute(f'SELECT {whom} FROM fight WHERE id=?', (id,)).fetchone()
    new_hp = old_hp[0] - int(pov)
    sql.execute(f'UPDATE fight SET {whom} =? WHERE id=?', (new_hp, id))
    connection.commit()

def exist_fight(id):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    checker = sql.execute('SELECT id FROM fight WHERE id=?', (id,)).fetchone()

    if checker:
        sql.execute('DELETE FROM fight WHERE id=?', (id,))
        connection.commit()
    else:
        pass

def get_fight_info(id):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    info = sql.execute('SELECT * FROM fight WHERE id=?', (id,)).fetchone()
    return info

def winner_winner(chicken_dinner, med):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    old_med = sql.execute(f'SELECT medals FROM heroes WHERE id=?', (chicken_dinner,)).fetchone()
    new_med = old_med[0] + med
    sql.execute(f'UPDATE heroes SET medals =? WHERE id=?', (new_med, chicken_dinner))

    old_lvl = sql.execute(f'SELECT lvl FROM heroes WHERE id=?', (chicken_dinner,)).fetchone()
    new_lvl = old_lvl[0] + 1
    sql.execute(f'UPDATE heroes SET lvl =? WHERE id=?', (new_lvl, chicken_dinner))

    connection.commit()

def admin_delite(id):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    if check_hero_db(id):
        sql.execute('DELETE FROM heroes WHERE id=?', (id,))
        connection.commit()

def get_all_admin_users():
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    old_hp = sql.execute(f'SELECT COUNT(*) FROM heroes').fetchone()
    return old_hp[0]

def send_medals(id, med):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    old_med = sql.execute(f'SELECT medals FROM heroes WHERE id=?', (id,)).fetchone()
    new_med = old_med[0] + med
    sql.execute(f'UPDATE heroes SET medals =? WHERE id=?', (new_med, id))
    connection.commit()

def change_name(id, name):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    sql.execute(f'UPDATE heroes SET name =? WHERE id=?', (name, id))
    connection.commit()

def change_bio(id, bio):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()
    sql.execute(f'UPDATE heroes SET info=? WHERE id=?', (bio, id))
    connection.commit()

def get_invent(id):
    connection = sqlite3.connect('data.db')
    sql = connection.cursor()

    inv= sql.execute(f'SELECT invent FROM heroes WHERE id=?', (id,)).fetchone()

    return inv[0]