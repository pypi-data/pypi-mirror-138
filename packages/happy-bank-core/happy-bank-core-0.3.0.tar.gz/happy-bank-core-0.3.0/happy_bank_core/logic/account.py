class Account:
    def __init__(self, customer_id: str, full_name: str, balance: float):
        """Gets customer's data"""
        self.id = customer_id
        self.name = full_name
        self.deposit = balance

    def __str__(self):
        return f"Customer ID: {self.id};\n Name: {self.name};\n " f"Balance: {self.deposit}"
