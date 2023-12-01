class Version:
    def __init__(self, item_name, number, rts=0, wts=0, created_by=None):
        self.name = item_name + str(number)
        self.number = number
        self.rts = rts
        self.wts = wts
        self.created_by = created_by
        self.transactions = {created_by}
        self.is_active = True

    def __str__(self):
        return f"Version: {self.number}, RTS: {self.rts}, WTS: {self.wts}, Created By: {self.created_by}"

    def add_transaction(self, transaction):
        self.transactions.add(transaction)
        # print("Version", self.number, "added transaction", transaction.name)

    def set_rts(self, timestamp):
        self.rts = timestamp
        print(f"[Version] RTS({self.name}) = {timestamp}")

    def set_wts(self, timestamp):
        self.wts = timestamp
        print(f"[Version] WTS({self.name}) = {timestamp}")

    def remove_transaction(self, transaction):
        self.transactions.remove(transaction)
        # print("Version", self.number, "removed transaction", transaction.name)


class Item:
    def __init__(self, name):
        self.name = name
        self.versions = []
        self.add_version()

    def __str__(self):
        return f"Item: {self.name}, Versions: {self.versions}"

    def add_version(self, rts=0, wts=0, created_by=None):
        next_version = len(self.versions)
        new_version = Version(self.name, next_version, rts, wts, created_by)
        self.versions.append(new_version)
        if created_by is not None:
            print(f"[Item] T{created_by.name}", end=" ")
        print(
            f"[Item] Create {new_version.name}. RTS({new_version.name}) = {rts}, WTS({new_version.name}) = {wts}")

        return new_version

    def get_highest_write(self, timestamp):
        for version in reversed(self.versions):
            if version.is_active and version.wts <= timestamp:
                return version

    def get_version(self, version_number):
        return self.versions[version_number]
