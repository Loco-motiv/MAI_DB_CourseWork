import os
import psycopg2
from psycopg2 import sql
from settings import DB_CONFIG

with psycopg2.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cur:
        dir_path = (os.path.realpath("destiny2/sample_data/"))

        csv_tables = os.listdir(dir_path)

        # for name in csv_tables:
        #     query = sql.SQL("""DROP TABLE {} CASCADE""").format(sql.Identifier(name[:-4]))
        #     cur.execute(query)
            

        with open('destiny2/migrations/ddl.sql', 'r') as sql_file:
            cur.execute(sql_file.read()) 

        for name in csv_tables:
            with open("destiny2/sample_data/" + name, 'r') as f:
                query = sql.SQL("""COPY {} FROM STDIN DELIMITER ',' CSV header""").format(sql.Identifier(name[:-4]))
                cur.copy_expert(query, f)

        with open('destiny2/migrations/dml.sql', 'r') as sql_file:
            cur.execute(sql_file.read()) 