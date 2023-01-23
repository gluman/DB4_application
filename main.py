# имя
# фамилия
# email
# телефон
# Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше. А может и вообще не быть телефона (например, он не захотел его оставлять).
# Вам необходимо разработать структуру БД для хранения информации и несколько функций на python для управления данными:
# Функция, создающая структуру БД (таблицы)
# Функция, позволяющая добавить нового клиента
# Функция, позволяющая добавить телефон для существующего клиента
# Функция, позволяющая изменить данные о клиенте
# Функция, позволяющая удалить телефон для существующего клиента
# Функция, позволяющая удалить существующего клиента
# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
# Функции выше являются обязательными, но это не значит что должны быть только они. При необходимости можете создавать дополнительные функции и классы.
# Также предоставьте код, демонстрирующий работу всех написанных функций.
# Результатом работы будет .py файл.

import psycopg2
import pprint as pp

run = True
while run:
    with psycopg2.connect(database="clientdatabase", user="postgres", password="postgres") as conn:
        with conn.cursor() as cur:

            def check_exist_client():
                pass

            def drop_data():
                # удаление таблиц
                cur.execute("""
                DROP TABLE phone_numbers;
                DROP TABLE clients;
                """)

            def show_help():
                print('''
                    c - create tables
                    h - show help
                    a - add client
                    l - list clients
                    e - edit clients information
                    d - delete clients
                    f - find clients
                    x - exit
                    ''')

            def create_tables():
                cur.execute("""
                         CREATE TABLE IF NOT EXISTS phone_numbers(
                             id_pn SERIAL PRIMARY KEY,
                             number VARCHAR(40) UNIQUE,
                             id_cl INTEGER NOT NULL REFERENCES clients(id)
                         );
                         """)
                cur.execute("""
                        CREATE TABLE IF NOT EXISTS clients(
                            id_cl SERIAL PRIMARY KEY,
                            name TEXT NOT NULL,
                            surname TEXT NOT NULL,
                            email VARCHAR(30) UNIQUE,
                            id_pn INTEGER REFERENCES phone_numbers(id_pn)
                                );
                         """)
                conn.commit()  # фиксируем в БД

            def add_client():
                name = input('Please, input clients Name: ')
                surname = input('Please, input clients Surname: ')
                email = input('Please, input clients email: ')
                phone = input('Please, input clients phone number(Enter to skip): ')

                cur.execute("""
                    INSERT INTO client(name, surname,) VALUES('Java') RETURNING id;
                    """)
                pp(cur.fetchone())  # запрос данных автоматически зафиксирует изменения

            def list_clients():
                cur.execute("""
                         SELECT  FROM clients;
                         """)
                pp('fetchall', cur.fetchall())  # извлечь все строки

            def edit_client():
                pass

            def delete_client():
                pass

            def find_clinet():
                pass



    i = input('input command, h - help')
    if i == 'c':
        create_tables()
    if i == 'h':
        show_help()
    if i == 'a':
        add_client()
    if i == 'l':
        list_clients()
    if i == 'e':
        edit_client()
    if i == 'd':
        delete_client()
    if i == 'drop':
        drop_data()
    if i == 'f':
        find_clinet()
    if i == 'x':
        run = False
    conn.close()

    # class Client:
    # def __int__(self, name, surname, email, phone):
    #     self.name = name
    #     self.surname = surname
    #     self.email = email
    #     self.phone = phone
    #
    #
    # def add_new(self, name, surname):
    #
    #
    #     # наполнение таблиц (C из CRUD)
    #     cur.execute("""
    #     INSERT INTO course(name) VALUES('Python');
    #     """)
    #     conn.commit()  # фиксируем в БД
    #
    #     cur.execute("""
    #     INSERT INTO course(name) VALUES('Java') RETURNING id;
    #     """)
    #     print(cur.fetchone())  # запрос данных автоматически зафиксирует изменения
    #
    #     cur.execute("""
    #     INSERT INTO homework(number, description, course_id) VALUES(1, 'простое дз', 1);
    #     """)
    #     conn.commit()  # фиксируем в БД
    #
    #     # извлечение данных (R из CRUD)
    #     cur.execute("""
    #     SELECT * FROM course;
    #     """)
    #     print('fetchall', cur.fetchall())  # извлечь все строки
    #
    #     cur.execute("""
    #     SELECT * FROM course;
    #     """)
    #     print(cur.fetchone())  # извлечь первую строку (аналог LIMIT 1)
    #
    #     cur.execute("""
    #     SELECT * FROM course;
    #     """)
    #     print(cur.fetchmany(3))  # извлечь первые N строк (аналог LIMIT N)
    #
    #     cur.execute("""
    #     SELECT name FROM course;
    #     """)
    #     print(cur.fetchall())
    #
    #     cur.execute("""
    #     SELECT id FROM course WHERE name='Python';
    #     """)
    #     print(cur.fetchone())
    #
    #     cur.execute("""
    #     SELECT id FROM course WHERE name='{}';
    #     """.format("Python"))  # плохо - возможна SQL инъекция
    #     print(cur.fetchone())
    #
    #     cur.execute("""
    #     SELECT id FROM course WHERE name=%s;
    #     """, ("Python",))  # хорошо, обратите внимание на кортеж
    #     print(cur.fetchone())
    #
    #     def get_course_id(cursor, name: str) -> int:
    #         cursor.execute("""
    #         SELECT id FROM course WHERE name=%s;
    #         """, (name,))
    #         return cur.fetchone()[0]
    #     python_id = get_course_id(cur, 'Python')
    #     print('python_id', python_id)
    #
    #     cur.execute("""
    #     INSERT INTO homework(number, description, course_id) VALUES(%s, %s, %s);
    #     """, (2, "задание посложнее", python_id))
    #     conn.commit()  # фиксируем в БД
    #
    #     cur.execute("""
    #     SELECT * FROM homework;
    #     """)
    #     print(cur.fetchall())
    #
    #     # обновление данных (U из CRUD)
    #     cur.execute("""
    #     UPDATE course SET name=%s WHERE id=%s;
    #     """, ('Python Advanced', python_id))
    #     cur.execute("""
    #     SELECT * FROM course;
    #     """)
    #     print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения
    #
    #     # удаление данных (D из CRUD)
    #     cur.execute("""
    #     DELETE FROM homework WHERE id=%s;
    #     """, (1,))
    #     cur.execute("""
    #     SELECT * FROM homework;
    #     """)
    #     print(cur.fetchall())  # запрос данных автоматически зафиксирует изменения

