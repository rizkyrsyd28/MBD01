class Transaction:
    def __init__(self, name: str):
        self.name = name
        self.operations: list[tuple(str, str, int)]  = []
        print(f"[Transaction] T{name} created")

    def getLastOperation(self) -> (str, str, int):
        return self.operations[len(self.operations)-1]
    
    def getFirstOperation(self) -> (str, str, int):
        return self.operations[0]