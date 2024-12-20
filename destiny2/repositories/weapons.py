import psycopg2
import psycopg2.extras
from settings import DB_CONFIG


def get_weapons() -> list[dict]:
    print("Getting weapons")
    query = "SELECT * FROM v_weapons_page;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

def get_first_column_perks() -> list[dict]:
    print("Getting first_column_perks")
    query = "SELECT * FROM v_first_column;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
        
def get_second_column_perks() -> list[dict]:
    print("Getting second_column_perks")
    query = "SELECT * FROM v_second_column;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
        
def filter_by_two_columns(first_name, second_name) -> list[dict]:
    print("Filtering by_two_columns")
    query = "SELECT * FROM filter_by_two_columns(%(first_name)s, %(second_name)s);"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"first_name": first_name, "second_name" : second_name})
            return cur.fetchall()
        
def filter_by_first_column(name) -> list[dict]:
    print("Filtering by_first_column")
    query = "SELECT * FROM filter_by_first_column(%(name)s);"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"name": name})
            return cur.fetchall()
        
def filter_by_second_column(name) -> list[dict]:
    print("Filtering by_second_column")
    query = "SELECT * FROM filter_by_second_column(%(name)s)"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"name": name})
            return cur.fetchall()
        
def get_weapon_barrel_perks(id) -> list[dict]:
    print("Getting perks")
    query = "SELECT * FROM weapon_barrel_perks(%(id)s)"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"id": int(id)})
            return cur.fetchall()
        
def get_weapon_magazine_perks(id) -> list[dict]:
    query = "SELECT * FROM weapon_magazine_perks(%(id)s)"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"id": int(id)})
            return cur.fetchall()

def get_weapon_first_column_perks(id) -> list[dict]:
    query = "SELECT * FROM weapon_first_column_perks(%(id)s)"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"id": int(id)})
            return cur.fetchall()
    
def get_weapon_second_column_perks(id) -> list[dict]:
    query = "SELECT * FROM weapon_second_column_perks(%(id)s)"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, {"id": int(id)})
            return cur.fetchall()
