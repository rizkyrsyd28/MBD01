package TwoPhaseLock

import (
	types "TwoPhaseLock/TwoPhaseLock/Types"
	"errors"
	"fmt"
	"strings"
)

type TwoPhaseLock struct {
	Schedule  []types.Operation
	Remainder []types.Operation
	LockTable types.LockTable
	WaitQueue []types.Operation
	Verbose   bool
}

func (c *TwoPhaseLock) Execute(input []types.Operation) {
	(*c).LockTable.New()
	(*c).Remainder = input

	for len(c.Remainder) != 0 {
		ops := pop(&c.Remainder, 0)
		if ops.Action == "R" {
			(*c).Read(ops)
		} else if ops.Action == "W" {
			(*c).Write(ops)
		} else if ops.Action == "C" {
			(*c).Commit(ops)
		}
		if c.Verbose {
			c.print(ops)
		}
	}

	// idx := 0
	for len(c.WaitQueue) != 0 {
		ops := pop(&c.WaitQueue, 0)
		if ops.Action == "R" {
			(*c).Read(ops)
		} else if ops.Action == "W" {
			(*c).Write(ops)
		} else if ops.Action == "C" {
			(*c).Commit(ops)
		}
		if c.Verbose {
			c.print(ops)
		}
		// idx++
		// if idx == 10 {
		// 	break
		// }

	}
}

func (c *TwoPhaseLock) addWaitSchedule(operation types.Operation) {
	// Rollback
	var buffer []int
	for idx, ops := range (*c).Remainder {
		if ops.Transaction == operation.Transaction && ops.Action != operation.Action {
			buffer = append(buffer, idx)
		}
	}
	for i, idx := range buffer {
		popOps := pop(&c.Remainder, idx-i)
		(*c).WaitQueue = append((*c).WaitQueue, popOps)
	}
}

func (c *TwoPhaseLock) rollback(operation types.Operation) {
	// Rollback
	var buffer []int
	for idx, ops := range (*c).Schedule {
		if ops.Transaction == operation.Transaction {
			buffer = append(buffer, idx)
		}
	}
	for i, idx := range buffer {
		popOps := pop(&c.Schedule, idx-i)
		if popOps.Action == "SL" || popOps.Action == "XL" {
			(*c).LockTable.Unlock(popOps)
		} else {
			(*c).WaitQueue = append((*c).WaitQueue, popOps)
		}
	}
}

func (c *TwoPhaseLock) Commit(operation types.Operation) {
	var buffer []types.Operation

	for key := range (*c).LockTable.Map {
		for _, lock := range (*c).LockTable.Map[key] {
			buffer = append(buffer, lock.ToOperation(key))
		}
	}

	for _, ops := range buffer {
		(*c).LockTable.Unlock(ops)
		ops.Action = "UL"
		(*c).Schedule = append((*c).Schedule, ops)
	}

	(*c).Schedule = append((*c).Schedule, operation)
}

func (c *TwoPhaseLock) Read(operation types.Operation) {
	var lock types.Lock

	locks, found := c.LockTable.GetResourceLock(operation)

	if found || len(locks) != 0 {
		// lock yang ada punya transaksi yang lagi jalan
		if l := types.GetLockTransaction(operation, locks); l.TypeLock != "" {
			lock = l
		} else {
			// lock yang ada bukan punya transaksi yang sedang jalan exclusive
			l = types.GetOtherLockTransaction(operation, locks)
			if l.IsExclusive() {
				(*c).deadlockPrevention(operation, l)
				return
			} else if l.IsShared() {
				lock = types.Lock{Transaction: operation.Transaction, TypeLock: "SL"}
				locks = append(locks, lock)
				c.LockTable.SetLock(operation.Resource, locks)
				(*c).Schedule = append((*c).Schedule, lock.ToOperation(operation.Resource))
			}
		}
	}

	if !found || len(locks) == 0 {
		// belum ada lock
		lock = types.Lock{Transaction: operation.Transaction, TypeLock: "SL"}
		locks = append(locks, lock)
		c.LockTable.SetLock(operation.Resource, locks)
		c.Schedule = append(c.Schedule, lock.ToOperation(operation.Resource))
	}

	(*c).Schedule = append((*c).Schedule, operation)
}

func (c *TwoPhaseLock) Write(operation types.Operation) {
	var lock types.Lock

	locks, found := c.LockTable.GetResourceLock(operation)

	// belum ada lock
	if !found || len(locks) == 0 {
		lock = types.Lock{Transaction: operation.Transaction, TypeLock: "XL"}
		locks = append(locks, lock)
		c.LockTable.SetLock(operation.Resource, locks)
		c.Schedule = append(c.Schedule, lock.ToOperation(operation.Resource))
	}

	if found || len(locks) != 0 {
		// lock yang ada punya transaksi yang lagi jalan
		if l := types.GetLockTransaction(operation, locks); l.TypeLock != "" {
			lock = l
		} else {
			// lock yang ada bukan punya transaksi yang sedang jalan
			(*c).deadlockPrevention(operation, l)
			return
		}
	}

	// transaksi punya shared lock
	if lock.IsShared() {
		// upgrade
		if err := (*c).upgrade(operation); err == nil {
			c.Schedule = append(c.Schedule, types.Operation{Transaction: operation.Transaction, Action: "XL", Resource: operation.Resource})
		}
	}

	(*c).Schedule = append((*c).Schedule, operation)
}

func (c *TwoPhaseLock) deadlockPrevention(operation types.Operation, lock types.Lock) {
	if operation.Transaction < lock.Transaction {
		// wait
		(*c).WaitQueue = append((*c).WaitQueue, operation)
		(*c).addWaitSchedule(operation)
	} else {
		// rollback
		(*c).rollback(operation)
		(*c).WaitQueue = append((*c).WaitQueue, operation)
		(*c).addWaitSchedule(operation)
	}
}

func (c *TwoPhaseLock) upgrade(operation types.Operation) error {
	locks, found := (*c).LockTable.GetResourceLock(operation)

	if !found {
		return errors.New("")
	}

	if len(locks) != 1 {
		for _, l := range locks {
			if operation.Transaction != l.Transaction {
				(*c).deadlockPrevention(operation, l)
				return errors.New("")
			}
		}
	}

	return (*c).LockTable.UpgradeLock(operation.Resource)
}

func (c TwoPhaseLock) printSchedule() string {
	builder := strings.Builder{}

	for i, ops := range c.Schedule {
		builder.WriteString(fmt.Sprintf(" %s ", ops.ToString()))
		if i != len(c.Schedule)-1 {
			builder.WriteString(fmt.Sprint(","))
		}
	}
	return builder.String()
}

func (c TwoPhaseLock) printRemainder() string {
	builder := strings.Builder{}

	for i, ops := range c.Remainder {
		builder.WriteString(fmt.Sprintf(" %s ", ops.ToString()))
		if i != len(c.Remainder)-1 {
			builder.WriteString(fmt.Sprint(","))
		}
	}
	return builder.String()
}

func (c TwoPhaseLock) printWait() string {
	builder := strings.Builder{}

	for i, ops := range c.WaitQueue {
		builder.WriteString(fmt.Sprintf(" %s ", ops.ToString()))
		if i != len(c.WaitQueue)-1 {
			builder.WriteString(fmt.Sprint(","))
		}
	}
	return builder.String()
}

func (c TwoPhaseLock) print(ops types.Operation) {
	fmt.Println("=========================================================")
	fmt.Printf("[On Hand] = %s\n", ops.ToString())
	fmt.Printf("[Schedule] = [%+v]\n", c.printSchedule())
	fmt.Printf("[Remainder] = [%+v]\n", c.printRemainder())
	fmt.Printf("[LockTable] = %+v\n", c.LockTable.Map)
	fmt.Printf("[Wait] = [%+v]\n", c.printWait())
	fmt.Println("=========================================================")
	fmt.Println()
}
