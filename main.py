# имя
# фамилия
# email
# телефон
# Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше. А может и вообще не быть телефона (например, он не захотел его оставлять).
# Вам необходимо разработать структуру БД для хранения информации и несколько функций на python для управления данными:
# Функция, создающая структуру БД (таблицы) - done
# Функция, позволяющая добавить нового клиента  +-
# Функция, позволяющая добавить телефон для существующего клиента
# Функция, позволяющая изменить данные о клиенте
# Функция, позволяющая удалить телефон для существующего клиента
# Функция, позволяющая удалить существующего клиента
# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)
# Функции выше являются обязательными, но это не значит что должны быть только они. При необходимости можете создавать дополнительные функции и классы.
# Также предоставьте код, демонстрирующий работу всех написанных функций.
# Результатом работы будет .py файл.

import psycopg2
# import pprint as pp

from unidecode import unidecode

run = True
with psycopg2.connect(database="clientdatabase", user="postgres", password="postgres", host='localhost') as conn:
    with conn.cursor() as cur:
        while run:
            def edit_client():

                 def check_exist_client(name, surname, email):
                    '''Check exist client in database'''
                    try:
                        cur.execute('''
                        SELECT count(*) FROM clients c
                        WHERE (c.name = %s AND c.surname = $s) OR email= %s 
                        RETURNING count(*);
                        ''', (name, surname, email))
                        conn.commit()
                        result = cur.fetchone()[0]
                    except:
                        return False
                    if result != 0:
                        return False    # Check is NOT OK
                    else:
                        return True     # Check is OK

            def check_exist_phonenum(number):
                '''Check exist phone in database'''
                try:
                    cur.execute('''
                SELECT count(*) FROM phone_numbers pn
                WHERE pn.number = %s
                RETURNING count(*);
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
                        name VARCHAR(30) NOT NULL,
                        surname VARCHAR(60) NOT NULL,
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

                # check = check_exist_client(name, surname, email)
                try:
                    cur.execute("""
                    INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s) RETURNING id_cl;
                    """, (name, surname, email))
                    id_cl = cur.fetchone()[0]  # запрос данных автоматически зафиксирует изменения   --- почему то не добавляет запись в бд, только возварщает id
                    print(f'Client {name}, {surname}, {email} added id: {id_cl}')
                    conn.commit()

                except:
                    print('Error! Some wrong with data')
                finally:
                    add_phone_number(phone, id_cl)
            def add_phone_number(phone, id_cl):
                if phone != '':
                    # check_phone = check_exist_phonenum(phone)
                    # if check_phone != False:
                    try:
                        cur.execute("""
                        INSERT INTO phone_numbers(number, id_cl) VALUES(%s, %s) RETURNING id_pn;
                        """, (phone, id_cl))
                        id_pn = cur.fetchone()[0]
                        conn.commit()
                        print(f'phone {phone} added id:', id_pn)  # запрос данных автоматически зафиксирует изменения
                    except:
                        print('This phone alredy exist')

            def list_clients():
                cur.execute("""
                         SELECT * FROM clients;
                         """)
                print('fetchall', cur.fetchall())  # извлечь все строки

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