import os
import sqlhelpers
from blockchain import get_local_blockchain, get_network_blockchain, Blockchain

DB_FILE = 'database.db'


def get_transaction_list():
    return [{'sender': 'BANK', 'recipient': 'user2', 'amount': '3'},
            {'sender': 'BANK', 'recipient': 'user1', 'amount': '3'},
            {'sender': 'user1', 'recipient': 'user2', 'amount': '2'},
            {'sender': 'user2', 'recipient': 'user1', 'amount': '3'}]


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
    blockchain.print_last(4)
    # transaction_list = get_transaction_list()
    # for transaction in transaction_list:
    #     block = Block(data=transaction)
    #     try:
    #         blockchain.mine(block=block)
    #     except transactions.InvalidTransaction:
    #         pass
    #     except transactions.InsufficientFunds:
    #         pass
    #     else:
    #         pass
    #

if __name__ == '__main__':
    main()
