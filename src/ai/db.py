import psycopg2
from pgvector.psycopg2 import register_vector

import config


def get_connection():
    conn = psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
    )
    register_vector(conn)
    return conn
