import sqlite3
from sqlite3 import Error

import main


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)

    return connection


def create_table(conn):
    create_table_sql = """ CREATE TABLE IF NOT EXISTS blockchain (
                        number integer PRIMARY KEY,
                        nonce integer NOT NULL,
                        previous_hash text NOT NULL,
                        data text NOT NULL
                    );"""
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)


def insert_new_data(connection, network_blockchain):
    sql = ''' INSERT INTO blockchain(number,nonce,previous_hash,data)
                 VALUES(?,?,?,?) '''
    for block in network_blockchain.chain:
        cursor = connection.cursor()
        cursor.execute(sql, (block.number, block.nonce, str(block.previous_hash), str(block.data)))
        connection.commit()


def get_data(connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM blockchain;")

    rows = cur.fetchall()
    return rows


def replace_data(network_blockchain):
    connection = create_connection(main.DB_FILE)
    sql = 'DELETE FROM blockchain;'
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)

    sql = 'VACUUM;'
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)

    insert_new_data(connection, network_blockchain)


def clean_database():
    pass
