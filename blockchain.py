import json
from hashlib import sha256
import sqlhelpers


def get_local_blockchain(connection):
    data = sqlhelpers.get_data(connection)
    blockchain = Blockchain()
    for block_data in data:
        block = Block(number=block_data[0], nonce=block_data[1], previous_hash=block_data[2],
                      data=json.dumps(block_data[3]))
        blockchain.add(block)
    blockchain.length = len(blockchain.chain)
    return blockchain


def get_network_blockchain():
    database = [{'sender': 'BANK', 'recipient': 'user2', 'amount': '3'},
                {'sender': 'BANK', 'recipient': 'user1', 'amount': '3'},
                {'sender': 'user1', 'recipient': 'user2', 'amount': '2'},
                {'sender': 'user2', 'recipient': 'user1', 'amount': '3'},
                {'sender': 'BANK', 'recipient': 'user1', 'amount': '2'},
                ]
    blockchain = Blockchain()
    for data in database:
        blockchain.mine(Block(data=data))
    return blockchain


def sync_blockchain(network_blockchain):
    sqlhelpers.replace_data(network_blockchain)


class Block:
    data = {}
    number = 0
    nonce = 0

    def __init__(self, data={}, number=None, nonce=0, previous_hash="0" * 64):
        self.number = number
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.data = data

    @staticmethod
    def _update_hash(*args):
        hashing_text = ""
        h = sha256()

        # loop through each argument and hash
        for arg in args:
            hashing_text += str(arg)

        h.update(hashing_text.encode('utf-8'))
        return h.hexdigest()

    def hash(self):
        return self._update_hash(self.previous_hash, self.data, self.nonce, self.number)

    def get_hash(self):
        return self.hash()

    def __str__(self):
        return str("Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" % (
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce,
        ))


class Blockchain:
    difficulty = 3
    chain = []
    length = 0

    def __init__(self):
        self.chain = []

    def add(self, block: Block):
        block.hash_string = block.hash()
        self.chain.append(block)

    def last_block_hash(self):
        try:
            return self.chain[-1].hash()
        except IndexError:
            # This will only happen for the genesis block
            pass

    def is_local_blockchain_valid(blockchain):
        # Consensus algorithm here

        # First check length
        # Check validity
        # If both are the same length keep yours and mine next block, repeat

        # The network will consider the longest valid blockchain the valid one.

        # With enough difficulty,
        # it's impossible for multiple blockchains to be the same length, and valid at the same time

        # network_blockchain = get_network_blockchain()
        # if network_blockchain is None:
        #     return True
        # if network_blockchain.length > blockchain.length and network_blockchain.is_blockchain_valid():
        #     return False
        # return True

        return True

    def mine(self, block):
        self.length += 1
        block.number = self.length
        if len(self.chain) == 0:
            self.add(block)
        else:
            block.previous_hash = self.last_block_hash()
            while True:
                hashed_string = block.hash()[:self.difficulty]
                if hashed_string == "0" * self.difficulty:
                    if self.is_local_blockchain_valid():
                        self.add(block)
                    else:
                        print("Block has already been mined, replacing local blockchain")
                        sync_blockchain(get_network_blockchain())
                        break
                    break
                else:
                    block.nonce += 1

    def print_last(self, size=10):
        if size > self.length:
            print("Not that many blocks")
        else:
            for block in self.chain[-size:]:
                print(block)

    def is_blockchain_valid(self):
        # loop through blockchain
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash
            _current = self.chain[i - 1].hash()
            # compare the previous hash to the actual hash of the previous block
            if _previous != _current or _current[:self.difficulty] != "0" * self.difficulty:
                return False
        return True

    def replace_blockchain(self):
        pass
