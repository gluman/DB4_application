
# Функция, создающая структуру БД (таблицы)  +
# Функция, позволяющая добавить нового клиента  +
# Функция, позволяющая добавить телефон для существующего клиента +
# Функция, позволяющая изменить данные о клиенте
# Функция, позволяющая удалить телефон для существующего клиента
# Функция, позволяющая удалить существующего клиента
# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону) +


import psycopg2
from pprint import pprint as pp


from unidecode import unidecode

run = True
with psycopg2.connect(database="clientdatabase", user="postgres", password="postgres", host='localhost') as conn:
    with conn.cursor() as cur:
        while run:

            def check_exist_client(name, surname, email):
                '''Check exist client in database'''
                cur.execute('''SELECT * FROM clients c
                WHERE c.email= %s
                ''', (email,))
                try:
                    result = cur.fetchone()
                except:
                    result = None
                if result == None:
                    return True    # Check found exist client
                else:
                    return False     # Check is OK

            def check_exist_phonenum(number):
                '''Check exist phone in database'''
                cur.execute('''
                SELECT * FROM phone_numbers pn
                WHERE pn.number = %s;
                ''', (number,))
                try:
                    result = int(cur.fetchone())
                except:
                    result = None
                if type(result) == int:
                    print('phone number alredy exist')
                    return False  # Check is NOT OK
                else:
                    return True  # Check is OK

            def drop_data():
                # удаление таблиц
                cur.execute("""
                DROP TABLE phone_numbers;
                DROP TABLE clients;
                """)
                conn.commit()
                return

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
                return

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
                return

            def add_client():
                name = input('Please, input clients Name: ')
                surname = input('Please, input clients Surname: ')
                email = input('Please, input clients email: ')
                phone = input('Please, input clients phone number(Enter to skip): ')

                check = check_exist_client(name, surname, email)
                if check:
                    cur.execute("""
                    INSERT INTO clients(name, surname, email) 
                    VALUES(%s, %s, %s) 
                    ON CONFLICT
                    DO NOTHING
                    RETURNING id_cl;
                    """, (name, surname, email))
                    try:
                        conn.commit()
                        result = cur.fetchone()[0]
                    except:
                        print('Error! Some wrong with data')
                    if int(result):
                        print(f'Client {name}, {surname}, {email} added id: {result}')
                        add_phone_number(phone, result)
                        return
                    else:
                        return

            def add_phone_number(phone=None, id_cl=None):
                if phone == None:
                    phone = input('input phone number:')
                check_phone = check_exist_phonenum(phone)
                if check_phone == True:
                        if id_cl == None:
                            idcl = True
                            while idcl:
                                mail = input('input clients email(l-show clients):')
                                if mail == 'l':
                                    list_clients()
                                else:
                                    id_cl = find_clinet(mail)[0]
                                    idcl = False
                                    if id_cl == False:
                                        return

                        try:
                            cur.execute("""
                            INSERT INTO phone_numbers(number, id_cl) 
                            VALUES(%s, %s)  
                            ON CONFLICT
                            DO NOTHING
                            RETURNING id_pn;
                            """, (phone, id_cl))
                            conn.commit()
                            id_pn = cur.fetchone()[0]
                            if int(id_pn):
                                print(f'phone {phone} added id:', id_pn)
                            else:
                                return
                        except:
                            print('This phone alredy exist')

            def list_clients():
                cur.execute("""
                         SELECT c.id_cl, c.name, c.surname, c.email, pn.number FROM clients c
                         LEFT JOIN phone_numbers pn ON c.id_cl = pn.id_pn;
                         """)
                conn.commit()
                pp(cur.fetchall(),indent=1)  # извлечь все строки

            def delete_client():
                input_info =True
                while input_info:
                    email = input('input value of client for delete(or l - show all):')
                    if email == 'l':
                        list_clients()
                    else:
                        input_info = False
                print('finded next information:')
                id_cl = find_clinet(email)
                id_del = input('which id of client do you want ti delete?(b - break')
                if id_del == 'b':
                    return
                elif int(id_del) in id_cl:
                    try:
                        cur.execute('''
                        DELETE FROM phone_numbers pn
                        WHERE pn.id_cl = %s 
                        ''', (id_del,))
                        conn.commit()
                        cur.execute('''
                        DELETE FROM clients c
                        WHERE c.id_cl = %s 
                        ''', (id_del,))
                        conn.commit()
                        print('done')
                    except:
                        print('error')
                else:
                    print('wrong id')
                    return

            def find_clinet(value=None):
                find = True
                while find:
                    params = ['name', 'surname', 'email', 'number']
                    if value == None:
                        value = input('input value:')
                    queue = f'''
                    SELECT c.id_cl, c.name, c.surname, c.email, pn.number FROM clients c
                    LEFT JOIN phone_numbers pn ON pn.id_cl = c.id_cl
                    WHERE c.{params[0]} = '{value}' OR c.{params[1]} = '{value}' OR c.{params[2]} = '{value}' OR pn.{params[3]} = '{value}'
                    '''
                    try:
                        cur.execute(queue)
                        result = cur.fetchall()
                        pp(result, indent=1)
                    except:
                        print('error or no data')
                        return
                    id_cl = []
                    for i in result:
                        id_cl.append(i[0])
                    print(id_cl)
                    find = False
                    if len(id_cl) > 0:
                        return id_cl






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