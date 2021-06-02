import os
import sqlhelpers
import transactions
from blockchain import get_local_blockchain, get_network_blockchain, Blockchain
from network import network

DB_FILE = 'database3.db'


# Initialize a database for the machine the code will be running on
def initial_setup(connection):
    sqlhelpers.create_table(conn=connection)
    blockchain = get_network_blockchain()
    sqlhelpers.insert_new_data(connection, blockchain)


# Set address for mining
# Consensus algorithm
def main():
    connection = sqlhelpers.create_connection(db_file=DB_FILE)
    # Check if database already exists, if not, create it and get the blockchain from the network.
    if not os.path.exists(DB_FILE):
        print('DATABASE NOT PRESENT, CREATING ---')
        initial_setup(connection=connection)
        sqlhelpers.insert_new_data(connection, get_network_blockchain())
    blockchain: Blockchain = get_local_blockchain(connection)
    transactions.send_currency(blockchain, sender='user1', recipient='user2', amount=1, mined_by="MINER3")
    transactions.send_currency(blockchain, sender='user2', recipient='user1', amount=1, mined_by="MINER3")
    transactions.send_currency(blockchain, sender='user1', recipient='user2', amount=1, mined_by="MINER3")
    transactions.send_currency(blockchain, sender='user2', recipient='user1', amount=1, mined_by="MINER3")


if __name__ == '__main__':
    main()
