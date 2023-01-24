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
    with psycopg2.connect(database="clientdatabase", user="postgres", password="postgres", host='localhost') as conn:
        with conn.cursor() as cur:
            def check_exist_client(name, surname, email):
                '''Check exist client in database'''
                # try:
                cur.execute('''SELECT * FROM clients c
                WHERE (c.name = %s AND c.surname = $s) OR email= %s;
                ''', (name, surname, email))
                conn.commit()
                result = cur.fetchone()[0]
                # except:
                #     return 'miss_data'  # if not rows in table
                # else:
                if result != 0:
                    return False    # Check is NOT OK
                else:
                    return True     # Check is OK

            def check_exist_phonenum(number):
                '''Check exist phone in database'''
                try:
                    cur.execute('''
                    SELECT count(*) FROM phone_numbers pn
                    WHERE pn.number = %s;
                    ''', (number,))
                    result = cur.fetchone()
                except:
                    return 'miss_data'
                else:
                    if result != 0:
                        return False    # Check is NOT OK
                    else:
                        return True     # Check is OK

            def drop_data():
                # удаление таблиц
                cur.execute("""
                DROP TABLE phone_numbers;
                DROP TABLE clients;
                """)
                conn.commit()

            def show_help():
                print('''
                    c - create tables
                    h - show help
                    a - add client
                    ap - add clients phone number 
                    l - list clients
                    e - edit clients information
                    d - delete clients
                    drop - drop tables
                    f - find clients
                    x - exit
                    ''')

            def create_tables():
                cur.execute("""
                        CREATE TABLE IF NOT EXISTS clients(
                            id_cl SERIAL PRIMARY KEY,
                            name TEXT NOT NULL,
                            surname TEXT NOT NULL,
                            email VARCHAR(30) UNIQUE
                            );
                         """)

                cur.execute("""
                         CREATE TABLE IF NOT EXISTS phone_numbers(
                             id_pn SERIAL PRIMARY KEY,
                             number VARCHAR(40) UNIQUE,
                             id_cl INTEGER NOT NULL REFERENCES clients(id_cl)
                         );
                         """)
                conn.commit()  # фиксируем в БД

            def add_client():
                name = input('Please, input clients Name: ')
                surname = input('Please, input clients Surname: ')
                email = input('Please, input clients email: ')
                phone = input('Please, input clients phone number(Enter to skip): ')

                check = check_exist_client(name, surname, email)
                if check != False:
                    cur.execute("""
                        INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s) RETURNING id_cl;
                        """, (name, surname, email))
                    id_cl = cur.fetchone()  # запрос данных автоматически зафиксирует изменения   --- почему то не добавляет запись в бд, только возварщает id
                    conn.commit()
                    add_phone_number(phone, id_cl)
                else:
                    pp('Error! Some wrong with data')

            def add_phone_number(phone, id_cl):
                if phone != '':
                    check_phone = check_exist_phonenum(phone)
                    if check_phone != False:
                        cur.execute("""
                            INSERT INTO phone_numbers(number, id_cl) VALUES(%s, %s) RETURNING id_pn;
                            """, (phone, id_cl))
                        pp('''Client added:''', cur.fetchone())
                        conn.commit()
                        # запрос данных автоматически зафиксирует изменения
                    else:
                        pp('This phone alredy exist')

            def list_clients():
                if check_exist_client() != 'miss_data':
                    cur.execute("""
                             SELECT * FROM clients;
                             """)
                    pp('fetchall', cur.fetchall())  # извлечь все строки
                else:
                    pp('No information in database')

            def edit_client():
                pass

            def delete_client():
                pass

            def find_clinet():
                pass



            i = input('input command, h - help: ')
            if i == 'c':
                create_tables()
            elif i == 'h':
                show_help()
            elif i == 'a':
                add_client()
            elif i == 'ap':
                add_phone_number()
            elif i == 'l':
                list_clients()
            elif i == 'e':
                edit_client()
            elif i == 'd':
                delete_client()
            elif i == 'drop':
                drop_data()
            elif i == 'f':
                find_clinet()
            elif i == 'x':
                run = False
                # else:
                #     pp('unknow command. h - help')
                #     continue


    # conn.close()

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

