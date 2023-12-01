<div align="center">
  <h1 align="center">Concurrency Control Protocol</h1>
  <p align="center">
    <i>
    Implementation Concurrency Protocol: Two-Phase Locking, Optimistic Concurrency Control, and Multiversion Timestamp Ordering Concurrency Control</i>
    <br />
  </p>
</div>

<p align="center">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
<img src="https://img.shields.io/badge/go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white">
</p>

## Description

The program is a simulation of the implementation of concurrency control in DBMS. In the program there are 3 algorithms used, which are Two-Phase Locking (2PL), Optimistic Concurrency Control (OCC), and Multiversion Timestamp Ordering Concurrency Control (MVCC). The program will receive an input .txt file containing the schedule of transactions and will then display the results of concurrency control on the terminal. This simulation is implemented with programs using Python (OCC, MVCC) and Golang (2PL).

## Feature

1. Two-Phase Locking
2. Optimistic Concurrency Control
3. Multiversion Timestamp Ordering Concurrency Control

## Requirement

1. Python 3
2. Golang 20

## How To Run

### 1. Multiversion Timestamp Ordering Concurrency Control (MVCC)

#### Input format

    The input's format could be seen inside test folder or
    TS(T1) = 5
    TS(T2) = 10
    ---- BEGIN EXECUTION ----
    R1(X)
    R2(X)

#### How To Run

1.  Navigate to root dir
2.  Run

        python3 src/MVCC/main.py [filepath]

    or

        py src/MVCC/main.py [filepath]

    depending on your python3 config, the command might be `python3` or `py` or others. For example `python3 src/MVCC/main.py test/test1.txt`

### 2. Optimistic Concurrency Control (OCC)

#### Input format

    The input's format could be seen inside test folder or
    TS(T1) #ignored
    TS(T2) #ignored
    ---- BEGIN EXECUTION ----
    R1(X)
    R2(X)

#### How To Run

1.  Navigate to root dir
2.  Run

        python3 src/OCC/main.py [filepath]

    or

        py src/OCC/main.py [filepath]

    depending on your python3 config, the command might be `python3` or `py` or others. For example `python3 src/OCC/main.py test/test1.txt`

### 3. Two-Phase Locking (2PL)

#### Input format

    The input's format could be seen inside test folder or
    TS(T1) #ignored
    TS(T2) #ignored
    ---- BEGIN EXECUTION ----
    R1(X)
    R2(X)

#### How To Run

1.  Navigate to root dir
2.  Navigate to `src/TwoPhaseLock`

        cd .\src\TwoPhaseLock

3.  Run

        go run main.go [filepath] [verbose]

    usage: filepath contain relative path to test file ex. `../../test/file.txt`. verbose is boolean, if verbose is true then program will display step by step and the final result, if false, it will only display the final result.

## Author

| Name                     | Task |   NIM    |
| ------------------------ | ---- | :------: |
| Mutawally Nawwar         | OCC  | 13521065 |
| Rizky Abdillah Rasyid    | 2PL  | 13521109 |
| Made Debby Almadea Putri | MVCC | 13521153 |
