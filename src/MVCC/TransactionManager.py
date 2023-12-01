import re
from Item import Item
from Transaction import Transaction, RolledbackException


class TransactionManager:
    '''
        Manage the transactions and the operations
    '''

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

    def handle_rollback(self, transaction: Transaction):
        '''
            Handle the rollback of a transaction

            Assumption:
            The transaction that is rolled back is will
            be executed first before the other transactions
        '''
        print(f"[Transaction Manager] T{transaction.name} ROLLBACK")
        self.result.append(f"A{transaction.name}")
        self.largest_timestamp += 1
        new_timestamp = self.largest_timestamp
        self.transactions[transaction.name] = Transaction(
            transaction.name, new_timestamp)

        '''
            cascading rollback mechanism
            when Tj read item that has been 
            written by Ti, and Ti is rolled back
        '''
        for version in transaction.created_versions:
            transactions = version.transactions
            for t in transactions:
                if t != transaction and not t.is_committed:
                    print(
                        f"[Transaction Manager] T{t.name} had read {version.name} when T{transaction.name} aborted it cascaded into T{t.name} and T{t.name} aborted")
                    try:
                        t.rollback()
                    except RolledbackException:
                        self.handle_rollback(t)

            print(f"[Transaction Manager] Remove {version.name}")
            self.items.get(
                version.name[:-1]).versions[version.number].is_active = False

        self.operations = transaction.operations + self.operations

    def execute(self):
        '''
            Execute the transactions with
            Multiversion Timestamp Ordering Concurency Control
        '''
        print()
        while True:
            try:
                print("[Transaction Manager] Queue:", self.operations)
                print()
                op = self.operations.pop(0)
                print(">>> Operations:", op)
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
                print(">>> No more operations")
                break
            except RolledbackException as e:
                self.handle_rollback(e.transaction)
                print()

        print(">>> Final Result")
        print()
        print(" ".join(self.result))
        print()

    def parse_transaction(self, transaction: str):
        '''
            Parse the transaction string into
            operation, transaction number, and item

            Return: tuple (operation, transaction number, item) or None
        '''
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
        '''
            Parse the timestamp string into
            transaction number and timestamp

            Return: tuple (transaction number, timestamp) or None
        '''
        pattern = r'TS\(T(\w+)\) = (\d+)'
        match = re.match(pattern, timestamp)

        if match:
            transaction = match.group(1)
            timestamp = int(match.group(2))
            return transaction, timestamp
        else:
            return None
