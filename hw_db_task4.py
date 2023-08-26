import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
	        client_id SERIAL PRIMARY KEY,
	        first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,        
            email VARCHAR(40) NOT NULL
        );
        """)
                       
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
	        phone_id SERIAL PRIMARY KEY,
	        client_id INTEGER NOT NULL REFERENCES clients(client_id),
            phone INTEGER(12)
        );
        """)
        
        cur.execute("""
        INSERT INTO clients (client_id, first_name, last_name, email)
        VALUES (0, 'None', 'None', 'None');
        );
        """)

        cur.execute("""
        INSERT INTO phones (phone_id, client_id, phone)
        VALUES (0, 0, 000000000000);
        );
        """)    

    return cur.fetchall()

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:

        cur.execute("""
        INSERT INTO clients (client_id, first_name, last_name, email)
        VALUES ((SELECT MAX(client_id) FROM clients)+1, 'first_name', 'last_name', 'email');
        );
        """)

        cur.execute("""
        INSERT INTO phones (phone_id, client_id, phone)
        VALUES ((SELECT MAX(phone_id) FROM phones)+1, 'client_id', 'phone';
        );
        """)

    return cur.fetchall()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phones (phone_id, client_id, phone)
        VALUES ((SELECT MAX(phone_id) FROM phones)+1,  'client_id', 'phone');
        );
        """)
    return cur.fetchall()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        
        cur.execute("""
        UPDATE clients
        SET first_name = 'first_name'
        SET last_name = 'last_name'
        SET email = 'email' 
        WHERE client_id = 'client_id';
        );
        """)

        cur.execute("""
        UPDATE phones
        SET phone = 'phone'
        WHERE client_id = 'client_id';
        );
        """)

    return cur.fetchall()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE client_id = 'client_id';
        );
        """)

    return cur.fetchall()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM clients
        WHERE client_id = 'client_id';
        );
        """)

    return cur.fetchall()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT c.first_name, c.last_name, c.email, c.phone FROM clients AS c
        LEFT JOIN phones AS p ON c.client_id = p.client_id
        WHERE c.first_name LIKE "first_name" OR c.last_name LIKE "last_name" OR c.email LIKE "email" OR c.phone LIKE phone;
        );
        """)
    return cur.fetchall()


with psycopg2.connect(database="db_hw_4", user="postgres", password="postgres") as conn:
    print(create_db(conn))
    print(add_client(conn, 'Иван', 'Петров', 'petrov9999@gmail.com'))
    print(add_client(conn,'Глафира', 'Сидорова', 'sidorova9999@gmail.com', 89876543210))
    print(add_phone(conn, 1, 899956789))
    print(change_client(conn, 1, 'Иван', 'Петров', 'petrov9999@yandex.ru', 89687654344))
    print(delete_phone(conn, 2))
    print(delete_client(conn, 2))
    print(find_client(conn, first_name=None, last_name=None, email=None, phone=None))
