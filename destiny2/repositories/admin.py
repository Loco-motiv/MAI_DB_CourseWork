import psycopg2
import psycopg2.extras
from settings import DB_CONFIG


def get_users():
    print("Getting users")
    query = "SELECT * FROM users WHERE role <> 2;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
        
def raise_user(user):
    print("Raising user")
    query = "CALL raise_user(%(user)s);"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"user": user})

def denote_user(user):
    print("Denoting user")
    query = "CALL denote_user(%(user)s);"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"user": user})