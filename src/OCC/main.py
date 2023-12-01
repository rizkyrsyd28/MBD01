from TransactionManager import TransactionManager

operations = ["R1(X)", "W1(X)",  "R2(X)", "W2(X)", "R1(X)", "W1(X)", "W2(X)", "W1(X)", "R3(X)"]

tm = TransactionManager(operations)
tm.start()
