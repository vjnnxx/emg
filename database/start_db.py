from database.db import *


def start():

    conn = get_conn()

    create_tables(conn)

    config = ('input_device', '{"id": 1}')

    create_config(conn, config)

