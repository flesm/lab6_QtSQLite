import sqlite3

insert_questions = [
        ("Назавіце сталіцу Бразіліі:"),
        ("Назавіце сталіцу ЗША:"),
        ("Назавіце сталіцу Паўднёвай Карэі:"),
        ("Назавіце сталіцу Швецыі:"),
        ("Назавіце сталіцу ПалАў:"),
    ]

insert_answers = [
    (1, 'Пекін', 0),
    (1, 'Бразіліа', 1),
    (1, 'Мінск', 0),
    (2, 'Вашынгтон', 1),
    (2, 'Нью-ёрк', 0),
    (2, 'Гаваі', 0),
    (3, 'Рыга', 0),
    (3, 'Алматы', 0),
    (3, 'Сеўл', 1),
    (3, 'Пусан', 0),
    (4, 'Стакгольм', 1),
    (4, 'Осла', 0),
    (4, 'Капенгаген', 0),
    (4, 'Хельсінкі', 0),
    (5, 'Нэйпьіда', 0),
    (5, 'Абуджа', 0),
    (5, 'Дадома', 0),
    (5, 'Мбабане', 0),
    (5, 'Нгерулмуд', 1),
]

with sqlite3.connect('database.db') as db:
    cursor = db.cursor()

    cursor.execute(""" DROP TABLE IF EXISTS Questions """)
    cursor.execute(""" DROP TABLE IF EXISTS Answers """)

    query1 = """ CREATE TABLE IF NOT EXISTS Questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL) """
    query2 = """ CREATE TABLE IF NOT EXISTS Answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                answer TEXT NOT NULL,
                correct INTEGER NOT NULL,
                FOREIGN KEY (question_id) REFERENCES Questions(id)) """

    cursor.execute(query1)
    cursor.execute(query2)

    query3 = """ INSERT INTO Questions(description)
                VALUES (?)"""
    cursor.executemany(query3, [(q,) for q in insert_questions])

    query4 = """INSERT INTO Answers (question_id, answer, correct)
                VALUES (?, ?, ?)"""
    cursor.executemany(query4, insert_answers)

    db.commit()