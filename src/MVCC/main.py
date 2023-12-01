from TransactionManager import TransactionManager
import utils.FileReader as FileReader

import sys


def start(filepath: str):
    timestamps, operations = FileReader.read(filepath)

    tm = TransactionManager(timestamps, operations)
    tm.execute()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py [filepath]")
        sys.exit(1)

    start(sys.argv[1])
