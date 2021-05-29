from blockchain import Block, Blockchain, get_local_blockchain


class InvalidTransaction(Exception):
    pass


class InsufficientFunds(Exception):
    pass


def send_currency(blockchain, sender=None, recipient=None, amount=0.0):
    try:
        amount = float(amount)
    except ValueError:
        raise InvalidTransaction()

    if get_ballance(blockchain, sender) < amount and sender != 'BANK':
        raise InsufficientFunds
    elif sender == recipient or amount <= 0.0:
        raise InvalidTransaction
    # More checks here when we implement users
    data = {
        'sender': sender,
        'recipient': recipient,
        'amount': str(amount)
    }
    blockchain.mine(Block(data))


def get_ballance(blockchain, user):
    total = 0
    for block in blockchain.chain[1:]:
        if block.data.get('sender', None):
            if block.data.get('sender') == user:
                total -= float(block.data.get('amount'))
            elif block.data.get('recipient') == user:
                total += float(block.data.get('amount'))

    return total
