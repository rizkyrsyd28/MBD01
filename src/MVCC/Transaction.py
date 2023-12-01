from Item import Item, Version


class RolledbackException(Exception):
    def __init__(self, transaction):
        super().__init__(f"T{transaction.name} ROLLBACK")

        self.transaction = transaction


class Transaction:
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp
        self.operations = []
        self.items = {}
        self.created_versions = []
        self.is_committed = False
        print(f"[Transaction] T{name} created with timestamp {timestamp}")

    def __str__(self):
        return f"Transaction: {self.name}, Timestamp: {self.timestamp}"

    def rollback(self):
        raise RolledbackException(self)

    def add_operation(self, operation):
        self.operations.append(operation)

    def commit(self):
        self.is_committed = True
        print(f"[Transaction] T{self.name} committed")

    def execute(self, operation: str, item: Item):
        if operation == "C":
            self.commit()
            return
        if item.name not in self.items:
            latest_version: Version = item.get_highest_write(self.timestamp)
            if latest_version is None:
                item.add_version(self.timestamp, self.timestamp, self)
                latest_version = item.get_highest_write(self.timestamp)

            self.items[item.name] = latest_version

        self.add_operation(f"{operation}{self.name}({item.name})")
        if operation == "R":
            self.read(item)
        elif operation == "W":
            self.write(item)

    def read(self, item: Item):
        version: Version = self.items[item.name]
        version.add_transaction(self)
        print(f"[Transaction] Execute R{self.name}({version.name})")
        if version.rts < self.timestamp:
            print(
                f"[Transaction] RTS({version.name}) = {version.rts} < TS(T{self.name}) = {self.timestamp}")
            version.set_rts(self.timestamp)

    def write(self, item: Item):
        version: Version = self.items[item.name]
        if (self.timestamp < version.rts):
            print(
                f"[Transaction] T{self.name} is not allowed to write {version.name} because TS(T{self.name}) = {self.timestamp} < RTS({version.name}) = {version.rts}")
            self.rollback()
            return
        if (self.timestamp == version.wts):
            print(f"[Transaction] T{self.name} overwrites {version.name}")
            version.set_wts(max(self.timestamp, version.wts))
            return

        print(
            f"[Transaction] TS(T{self.name}) = {self.timestamp} > RTS({version.name}) = {version.rts}. Create new version")
        new_version = item.add_version(self.timestamp, self.timestamp, self)
        self.created_versions.append(new_version)
        self.items[item.name] = new_version
