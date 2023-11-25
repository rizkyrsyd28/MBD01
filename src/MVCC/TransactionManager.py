import re
from Item import Item
from Transaction import Transaction, RolledbackException


class TransactionManager:
    def __init__(self, transactions, operations):
        self.items = {}
        self.current_index = 0
        self.operations = operations
        self.transactions = {}
        self.largest_timestamp = 0
        self.result = []

        for t in transactions:
            transaction, timestamp = self.parse_timestamp(t)
            new_transaction = Transaction(transaction, timestamp)
            self.transactions[transaction] = new_transaction
            if timestamp > self.largest_timestamp:
                self.largest_timestamp = timestamp

    def add_operation(self, operation):
        self.operations.append(operation)

    def add_rolledback_ops(self, transaction: Transaction):
        '''
            Assumption:
            The transaction that is rolled back is will
            be executed first before the other transactions
        '''
        try:
            print(f"T{transaction.name} ROLLBACK")
            self.result.append(f"A{transaction.name}")
            self.largest_timestamp += 1
            new_timestamp = self.largest_timestamp
            for version in transaction.created_versions:
                transactions = version.transactions
                for t in transactions:
                    if t != transaction:
                        t.rollback()
        except RolledbackException as e:
            self.add_rolledback_ops(e.transaction)

        self.operations = self.operations[0:self.current_index + 1] + \
            transaction.operations + self.operations[self.current_index + 1:]

        self.transactions[transaction.name] = Transaction(
            transaction.name, new_timestamp)

    def execute(self):
        print()
        while True:
            try:
                op = self.operations[self.current_index]
                print("----- Operations:", op, "-----")
                operation, transaction, item = self.parse_transaction(op)
                transaction_obj = self.transactions.get(transaction)

                if item is not None and item not in self.items:
                    new_item = Item(item)
                    self.items[item] = new_item

                transaction_obj.execute(operation, self.items.get(item))

                if operation == "C":
                    self.result.append(f"{operation}{transaction}")
                else:
                    self.result.append(
                        f"{operation}{transaction}({transaction_obj.items.get(item).name})")
                self.current_index += 1
                print()
            except IndexError:
                print("----- No more operations -----")
                break
            except RolledbackException as e:
                self.add_rolledback_ops(e.transaction)
                print()

        print("----- Final Result -----")
        print(self.result)

    def parse_transaction(self, transaction: str):
        commit_pattern = r'C(\d+)'
        match = re.match(commit_pattern, transaction)
        if match:
            return "C", match.group(1), None

        pattern = r'([A-Za-z]+)(\d+)\((\w+)\)'
        match = re.match(pattern, transaction)

        if match:
            operation = match.group(1)
            transaction_number = match.group(2)
            item = match.group(3)
            return operation, transaction_number, item
        else:
            return None

    def parse_timestamp(self, timestamp: str):
        pattern = r'TS\(T(\w+)\) = (\d+)'
        match = re.match(pattern, timestamp)

        if match:
            transaction = match.group(1)
            timestamp = int(match.group(2))
            return transaction, timestamp
        else:
            return None
