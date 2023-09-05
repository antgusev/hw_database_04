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
        conn.commit()
                       
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phones (
	        phone_id SERIAL PRIMARY KEY,
	        client_id INTEGER NOT NULL REFERENCES clients(client_id),
            phone VARCHAR(12)
            );
        """)
        conn.commit()
        
        cur.execute("""
        INSERT INTO clients (client_id, first_name, last_name, email)
        VALUES (0, 'None', 'None', 'None');
        """)
        conn.commit()

        cur.execute("""
        INSERT INTO phones (phone_id, client_id, phone)
        VALUES (0, 0, '000000000000');
        """)
        conn.commit()    

        # return cur.fetchall()

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cur:

        cur.execute("""
        INSERT INTO clients (client_id, first_name, last_name, email)
        VALUES ((SELECT MAX(client_id) FROM clients)+1, %s, %s, %s)
        RETURNING client_id;
        """, (first_name, last_name, email))
        last_client_id = cur.fetchone()

        cur.execute("""
        INSERT INTO phones (phone_id, client_id, phone)
        VALUES ((SELECT MAX(phone_id) FROM phones)+1, %s, %s);
        """, (last_client_id, phone))
        conn.commit()

        # return cur.fetchall()

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phones (phone_id, client_id, phone)
        VALUES ((SELECT MAX(phone_id) FROM phones)+1,  %s, %s)
        RETURNING phone_id, client_id, phone;
        """, (client_id, phone))
        return cur.fetchone()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        
        cur.execute("""
        UPDATE clients
        SET first_name = %s, last_name = %s, email = %s
        WHERE client_id = %s
        RETURNING client_id, first_name, last_name, email;
        """, (first_name, last_name, email, client_id))

        cur.execute("""
        UPDATE phones
        SET phone = %s
        WHERE client_id = %s
        RETURNING phone_id, client_id, phone;
        """, (phone, client_id))

        return cur.fetchall()

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE client_id = %s AND phone = %s
        RETURNING phone_id, client_id, phone;
        """, (client_id, phone))

        return cur.fetchall()

def delete_client(conn, client_id):
    
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE client_id = %s;
        """, (client_id,))
        conn.commit()
    
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM clients
        WHERE client_id = %s;
        """, (client_id,))
        conn.commit()
        # return cur.fetchall()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        # cur.execute("""
        # SELECT c.first_name, c.last_name, c.email, c.phone FROM clients AS c
        # LEFT JOIN phones AS p ON c.client_id = p.client_id
        # WHERE c.first_name LIKE %s AND c.last_name LIKE %s AND c.email LIKE %s AND c.phone LIKE %s;
        # """, (first_name, last_name, email, phone))
    
        # cur.execute("""
        # SELECT c.first_name, c.last_name, c.email, c.phone FROM clients AS c
        # LEFT JOIN phones AS p ON c.client_id = p.client_id
        # WHERE (c.first_name = %s OR c.first_name = %) THEN
        #     (c.last_name = %s OR c.last_name = %) THEN
        #     (c.email = %s OR c.email = %) THEN
        #     (c.phone = %s OR c.phone = %);
        # """, (first_name, last_name, email, phone))

        cur.execute("""
        SELECT c.first_name, c.last_name, c.email, p.phone FROM clients AS c
        LEFT JOIN phones AS p ON c.client_id = p.client_id
        WHERE (c.first_name = %s OR %s IS NULL) AND
              (c.last_name = %s OR %s IS NULL) AND
              (c.email = %s OR %s IS NULL) AND
              (p.phone = %s OR %s IS NULL);
        """, (first_name, first_name, last_name, last_name, email, email, phone, phone))

        # conn.commit()
        print(cur.fetchone())


with psycopg2.connect(database='db_hw_4', user='postgres', password='postgres') as conn:

    # with conn.cursor() as cur:
    #     cur.execute("""
    #     DROP TABLE phones;
    #     DROP TABLE clients;
    #     """)
    #     conn.commit()

    if __name__ == '__main__':

        create_db(conn)
        # add_client(conn, 'Иван', 'Петров', 'petrov9999@gmail.com')
        # add_client(conn,'Глафира', 'Сидорова', 'sidorova9999@gmail.com', '89876543210')
        # print(add_phone(conn, 1, '899956789'))
        # print(change_client(conn, 1, 'Иван', 'Петров', 'petrov9999@yandex.ru', '89687654344'))
        # print(delete_phone(conn, 2, '89876543210'))
        # delete_client(conn, 2)
        # find_client(conn, 'Иван', None, None, None)

# conn.close()
