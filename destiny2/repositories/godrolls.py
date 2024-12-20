import psycopg2
import psycopg2.extras
from settings import DB_CONFIG

def get_godrolls():
    print("Getting godrolls")
    query = "SELECT * FROM v_god_rolls;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
        
def get_godroll_prepositions():
    print("Getting godroll prepositions")
    query = "SELECT * FROM v_godroll_prepositions;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
        
def approve_godroll(id):
    print("Approving godroll")
    query = "CALL approve_godroll(%(id)s);"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"id": id})
        
def insert_godroll(id, user_id, author, description, barrel, magazine, first_column_perk, second_column_perk):
    print("Inserting godroll")
    query = "CALL submit_godroll(%(id)s::BIGINT, %(user_id)s::BIGINT, %(author)s::text, %(description)s::text, %(barrel_id)s::BIGINT, %(magazine_id)s::BIGINT, %(first_column_id)s::BIGINT, %(second_column_id)s::BIGINT);"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"id": id, "user_id": user_id, "author": author, "description": description, "barrel_id": barrel, "magazine_id": magazine, "first_column_id": first_column_perk, "second_column_id": second_column_perk})