from TransactionManager import TransactionManager

t_timestamps = ["TS(T1) = 5", "TS(T2) = 10"]
tests = ["R1(X)", "W1(X)",  "R2(X)", "W2(X)", "R1(X)", "W1(X)", "W2(X)"]

new_t = ["TS(T1) = 1", "TS(T2) = 2", "TS(T3) = 3"]
operations = [
    "R1(A)",
    "R2(A)",
    "R3(B)",
    "R1(B)",
    "W3(C)",
    "W2(C)",
    "R1(C)",
    "C1",
    "R2(D)",
    "W3(B)",
    "C3",
    "W2(D)",
    "C2"
]

tm = TransactionManager(t_timestamps, tests)
tm.execute()
