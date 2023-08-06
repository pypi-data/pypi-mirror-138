from account import Account


class TransactionException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Transaction:
    @staticmethod
    def check_balance(customer: Account, amount: float) -> bool:
        """Verifies if customer has enough money to transfer"""
        balance = customer.deposit
        return 0 < amount <= balance

    @staticmethod
    def transfer(sender: Account, recipient: Account, amount: float) -> tuple | Exception:
        """Ensures transfer between 2 accounts"""
        if sender.id == recipient.id:
            raise TransactionException("Sender and recipient ids should have different values")
        elif not Transaction.check_balance(sender, amount):
            raise TransactionException("Insufficient balance or transfer amount <= 0")

        sender.deposit = round((sender.deposit - amount), 2)
        recipient.deposit = round((recipient.deposit + amount), 2)
        print(
            f"Following amount {amount} has been transferred "
            f"from account {sender.id} to account {recipient.id}\n"
            f"Current {sender.id} balance: {sender.deposit}\n"
            f"Current {recipient.id} balance: {recipient.deposit}\n"
            f"---------------------------------------------------"
        )
        return sender, recipient
