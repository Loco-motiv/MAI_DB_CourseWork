import psycopg2
import psycopg2.extras
from settings import DB_CONFIG


def get_armor() -> list[dict]:
    print("Getting armor")
    query = "SELECT * FROM v_armor_page;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
