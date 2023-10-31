import psycopg2

# создаем соединение
conn = psycopg2.connect(database='netology_db', user='postgres', password='35255')


# создаём функцию для создания таблицы "client"
def create_table_client(conn):
    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE IF NOT EXISTS client(
                            client_id SERIAL PRIMARY KEY,
                            name VARCHAR(255) NOT NULL ,
                            surname VARCHAR(255) NOT NULL ,
                            email VARCHAR(255) NOT NULL,
                            phone VARCHAR(255)
                );
                """)
        conn.commit()

        return "Таблица client успешно создана!"

# создаём функцию, создающую таблицу для хранения телефонных номеров клиентов
def create_table_phone_numbers(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers(
            pn_id SERIAL PRIMARY KEY,
            client_id INT,
            phone_number VARCHAR(255),
            FOREIGN KEY (client_id) REFERENCES client(client_id)
        );
        """)
        conn.commit()

        return "Таблица phone_numbers успешно создана!"


# создаём функцию, создающую таблицу, связывающую таблицу client и таблицу phone_number
def create_table_client_phone_number(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client_pn(
        pn_id INTEGER NOT NULL REFERENCES phone_number(pn_id),
        client_id INTEGER NOT NULL REFERENCES client(client_id),
        PRIMARY KEY (pn_id, client_id)
        )
        """)
        conn.commit()

        return "Таблица client_pn успешно создана!"


# создаём функцию для добавления в таблицу "client" нового клиента
def add_new_client(conn, name, email, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(name, email, phone)
        VALUES(%s, %s, %s)
        """, (name, email, phone))
        conn.commit()

        return f"Клиент {name} успешно добавлен!"


# создаём функцию для добавления номера телефона существующему клиенту
def add_new_phone(conn, client_name, client_surname, phone):
    with conn.cursor() as cur:
        # находим client_id по имени клиента
        cur.execute("""
        SELECT client_id FROM client WHERE name = %s AND surname = %s 
        """, (client_name, client_surname))
        client_id = cur.fetchone()
        if client_id:
            client_id = client_id[0]
            # вставляем номер телефона с указанным client_id
            cur.execute("INSERT INTO phone_numbers (client_id, phone_number)"
                        "VALUES (%s, %s)", (client_id, phone))
            conn.commit()
        else:
            print(f"Клиент с именем {client_surname} {client_name} не найден")


# создаём функцию, которая  изменяет данные клиента
# предполагается, что поиск клиента будет осуществляться по client_id, а замена будет происходить в
# соотв. поле, если его значение не None, то есть, если мы что-то вводим, то это уже новые данные
def change_client_data(conn, client_id, client_name=None, client_surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        if client_name is not None:
            cur.execute("""
            SELECT client_name FROM client WHERE client_id = %s
            """, (client_id))
            new_client_name = cur.fetchone()

            if client_name:
                new_client_name = new_client_name[0]
                cur.execute("UPDATE client SET client_name = new_client_name WHERE client_id = %s", (client_id, ))
            else:
                print(f"Данный пользователь не найден!")

        if client_surname is not None:
            cur.execute("""
                        SELECT client_surname FROM client WHERE client_id = %s
                        """, (client_id, ))
            new_client_surname = cur.fetchone()

            if client_surname:
                new_client_surname = new_client_surname[0]
                cur.execute("UPDATE client SET client_surname = new_client_surname WHERE client_id = %s", (client_id, ))
            else:
                print(f"Данный пользователь не найден!")

        if email is not None:
            cur.execute("""
                        SELECT email FROM client WHERE client_id = %s
                        """, (client_id, ))
            new_client_email = cur.fetchone()

            if email:
                new_client_email = new_client_email[0]
                cur.execute("UPDATE client SET email = new_client_email WHERE client_id = %s", (client_id, ))
            else:
                print(f"Данный пользователь не найден!")

        if phone is not None:
            cur.execute("""
                        SELECT phone FROM client WHERE client_id = %s
                        """, (client_id, ))
            new_client_phone = cur.fetchone()

            if phone:
                new_client_phone = new_client_phone[0]
                cur.execute("UPDATE client SET phone = new_client_phone WHERE client_id = %s", (client_id, ))
            else:
                print(f"Данный пользователь не найден!")


# создаём функцию для удаления телефона существующего клиента
def delete_phone_number(conn, client_name, client_surname, phone):
    with conn.cursor() as cur:
        # проверяем, существует ли клиент с указанными именем и фамилией
        cur.execute("SELECT client_name, client_surname FROM client"
                    " WHERE client_name = %s AND client_surname = %s", (client_name, client_surname))
        client_exists = cur.fetchone()

        if client_exists:
            # проверяем, существует ли номер телефона для данного клиента
            cur.execute("SELECT phone FROM client "
                        "WHERE client_name = %s AND client_surname = %s AND phone = %s",
                        (client_name, client_surname, phone))
            client_phone = cur.fetchone()

            if client_phone:
                # удаляем номер телефона для данного клиента
                cur.execute("DELETE FROM client "
                            "WHERE phone = %s", (client_name, client_surname, phone))
                conn.commit()
                print(f"Номер телефона {phone} успешно удален у клиента {client_name} {client_surname}.")
            else:
                print(f"У клиента {client_name} {client_surname} нет указанного номера телефона.")
        else:
            print(f"Клиент {client_name} {client_surname} не найден.")


# создаём функцию для удаления существующего клиента
def delete_client(conn, client_name, client_surname):
    with conn.cursor() as cur:
        # Проверяем, существует ли клиент с указанными именем и фамилией
        cur.execute("SELECT client_id FROM client "
                    "WHERE client_name = %s AND client_surname = %s", (client_name, client_surname))
        client_id = cur.fetchone()

        if client_id:
            client_id = client_id[0]

            # Удаляем клиента
            cur.execute("DELETE FROM client WHERE client_id = %s", (client_id,))
            conn.commit()
            print(f"Клиент {client_name} {client_surname} успешно удален!")
        else:
            print(f"Клиент {client_name} {client_surname} не найден!")


# создаём функцию, позволяющую найти клиента по его данным: имени, фамилии, email или телефону
# если какое-либо из значений параметров ф-ии != None, мы будем искать клиента по этому параметру
# (предполагается, что поиск не может осуществляться только лишь по имени, следовательно это будет комбинация
# имя + фамилия)
def find_client(conn, client_name=None, client_surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        if client_name is not None and client_surname is not None:
            cur.execute("SELECT client_name, client_surname, mail, phone FROM client "
                        "WHERE client_name = %s AND client_surname = %s", (client_name, client_surname))
            result = cur.fetchall()

            if result:
                print(f"Клиент найден {result}")
            else:
                print("Указанный клиент не найден.")

        if client_surname is not None:
            cur.execute("SELECT client_name, client_surname, mail, phone FROM client "
                        "WHERE client_surname = %s", (client_surname, ))
            result = cur.fetchall()

            if result:
                print(f"Клиент найден {result}")
            else:
                print("Указанный клиент не найден.")

        if email is not None:
            cur.execute("SELECT client_name, client_surname, mail, phone FROM client "
                        "WHERE email = %s", (email, ))
            result = cur.fetchall()

            if result:
                print(f"Клиент найден {result}")
            else:
                print("Указанный клиент не найден.")

        if phone is not None:
            cur.execute("SELECT client_name, client_surname, mail, phone FROM client "
                        "WHERE phone = %s", (phone, ))
            result = cur.fetchall()

            if result:
                print(f"Клиент найден {result}")
            else:
                print("Указанный клиент не найден.")


    conn.close()
