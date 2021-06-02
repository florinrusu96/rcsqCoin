import json
from sqlite3 import Error

import sqlhelpers
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "network.db")


def get_data(connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM blockchain;")
    rows = cur.fetchall()
    return rows


def get_connection():
    connection = sqlhelpers.create_connection(db_file=DB_FILE)
    return connection


def get_network_blockchain_data():
    conn = get_connection()
    data = get_data(conn)
    conn.close()
    return data


def write_to_network_blockchain(blockchain, mined_by):
    local_data = get_network_blockchain_data()
    # Get local network data

    # Act as if the network will take the longest one available


    if blockchain.length > len(local_data):
        connection = get_connection()
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
        sql = ''' INSERT INTO blockchain(number,nonce,previous_hash,data)
                     VALUES(?,?,?,?) '''
        for block in blockchain.chain:
            cursor = connection.cursor()
            cursor.execute(sql, (block.number, block.nonce, str(block.previous_hash), str(block.data)))
            connection.commit()
        connection.close()
        print(f"New block mined by {mined_by}")
        print("Blockchain on the network is:")
        blockchain.print_last(blockchain.length)
