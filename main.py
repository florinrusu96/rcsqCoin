import os
import threading

import sqlhelpers
import transactions
from blockchain import get_local_blockchain, get_network_blockchain, Blockchain
from network import network

DB_FILE = 'database.db'


# Initialize a database for the machine the code will be running on
def initial_setup(connection):
    sqlhelpers.create_table(conn=connection)
    blockchain = get_network_blockchain()
    sqlhelpers.insert_new_data(connection, blockchain)


# Set address for mining
# Consensus algorithm
def main(mined_by):
    connection = sqlhelpers.create_connection(db_file=DB_FILE)
    # Check if database already exists, if not, create it and get the blockchain from the network.
    if not os.path.exists(DB_FILE):
        print('DATABASE NOT PRESENT, CREATING ---')
        initial_setup(connection=connection)

    blockchain: Blockchain = get_network_blockchain()
    # sqlhelpers.insert_new_data(connection, blockchain)
    transactions.send_currency(blockchain, sender='user1', recipient='user2', amount=1, mined_by=f"MINER{mined_by}")
    transactions.send_currency(blockchain, sender='user2', recipient='user1', amount=1, mined_by=f"MINER{mined_by}")
    transactions.send_currency(blockchain, sender='user2', recipient='user1', amount=1, mined_by=f"MINER{mined_by}")
    transactions.send_currency(blockchain, sender='user1', recipient='user2', amount=1, mined_by=f"MINER{mined_by}")
    transactions.send_currency(blockchain, sender='user2', recipient='user1', amount=1, mined_by=f"MINER{mined_by}")


if __name__ == '__main__':
    threads = []

    for i in range(4):
        t = threading.Thread(target=main, args=(i,))
        t.daemon = True
        threads.append(t)

    for i in range(3):
        threads[i].start()

    for i in range(3):
        threads[i].join()
