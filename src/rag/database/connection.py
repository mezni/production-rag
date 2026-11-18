import os

import psycopg
from pgvector.psycopg import register_vector


def get_connection():

    connection = psycopg.connect(os.environ["DATABASE_URL"])

    register_vector(connection)

    return connection
