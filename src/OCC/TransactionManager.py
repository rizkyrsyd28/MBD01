from Transaction import Transaction

class TransactionManager:
    def __init__(self, operations: list[str]) -> None:
        self.currentIndex = 0
        self.operations = operations
        self.transactions: list[Transaction] = []
        self.result: list[(str, str, str)] = []

        self.parse()
        
    def parse(self) -> None:
        i = 1
        for op in self.operations:
            if(op[2] == "("):
                transName = op[1:2]
                var = op[3:4]
            else:
                transName = op[1:3]
                var = op[4:5]
            index = self.getTransactionIndexByName(transName)
            if(index == -1):
                newTrans = Transaction(transName)
                self.transactions.append(newTrans)
            self.transactions[index].operations.append((op[0:1], var, i))
            self.result.append((transName, op[0:1], var))
            i += 1

    def getTransactionIndexByName(self, name: str) -> int:
        i = 0
        for trans in self.transactions:
            if(trans.name == name):
                return i
            i += 1
        return -1
    
    def start(self) -> None:
        length = len(self.transactions)
        # sort by commit
        # for i in range(length):
        #     for j in range(i+1, length):
        #         if(self.transactions[i].getLastOperation()[2] > self.transactions[j].getLastOperation()[2]):
        #             tmp = self.transactions[i]
        #             self.transactions[i] = self.transactions[j]
        #             self.transactions[j] = tmp

        while self.currentIndex < length:
            print(f">>> Transactions: {self.transactions[self.currentIndex].name}")
            if not self.isValid():
                print(f"T{self.transactions[self.currentIndex].name} Roll Back")
                self.rollBack()
            print(f"T{self.transactions[self.currentIndex].name} commited\n")
            self.currentIndex += 1
        
        print(">>> Final Result")
        for op in self.result:
            print(f"{op[1]}{op[0]}({op[2]})")

    def isValid(self) -> bool:
        # if not first commited transaction
        if(self.currentIndex != 0):
            # loop for each commited transaction
            for i in range(self.currentIndex):
                # check if current transaction started after commited transaction
                if(self.transactions[i].getLastOperation()[2] > self.transactions[self.currentIndex].getFirstOperation()[2]):
                    # loop for each write operation in each commited transaction
                    for opW in self.transactions[i].operations:
                        if(opW[0] == 'W'):
                            # loop for each read operation in current transaction that read before write by commited transaction
                            for opR in self.transactions[self.currentIndex].operations:
                                if(opR[0] == 'R' and opR[1] == opW[1] and opR[2] < opW[2]):
                                    print(f"Invalid: R{self.transactions[self.currentIndex].name}({opR[1]}) read the variable that written by W{self.transactions[i].name}({opW[1]})")
                                    return False
        print("Valid")
        return True

    def rollBack(self) -> None:
        name = self.transactions[self.currentIndex].name
        length = len(self.result)
        j = 0
        # delete all operations from rolled back transaction
        for i in range(length):
            if self.result[j][0] == name:
                self.result.remove(self.result[j])
                j -= 1
            j += 1

        # update commited transaction time
        for i in range(self.currentIndex):
            transName = self.result[i][0]
            j = 0
            for k in range(len(self.result)):
                if self.result[k][0] == transName:
                    self.transactions[i].operations[j] = (self.transactions[i].operations[j][0], self.transactions[i].operations[j][1], k+1)
                    j += 1

        length  = len(self.transactions[self.currentIndex].operations)
        # update current transaction
        lastIdx = self.getLastCommitedIndex()
        for i in range(length):
            self.result.insert(lastIdx+i, (name, self.transactions[self.currentIndex].operations[i][0], self.transactions[self.currentIndex].operations[i][1]))
            self.transactions[self.currentIndex].operations[i] = (self.transactions[self.currentIndex].operations[i][0], self.transactions[self.currentIndex].operations[i][0], lastIdx+1+i)

    def getLastCommitedIndex(self):
        lastIdx = -1
        for i in range(self.currentIndex):
            if(self.transactions[i].getLastOperation()[2] > lastIdx):
                lastIdx = self.transactions[i].getLastOperation()[2]
        return lastIdx
