import psycopg2
import psycopg2.extras
from settings import DB_CONFIG

def user_data(login):
    print("Getting password")
    query = "SELECT * FROM user_data(%(login)s);"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"login": login})
            fetch = cur.fetchone()
            if fetch == None:
                return (-1, "", -1)
            else: 
                return fetch
        
def register_user(login, password):
    print("Registering user")
    query = "CALL register_user(%(login)s, %(password)s);"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"login": login, "password": password})