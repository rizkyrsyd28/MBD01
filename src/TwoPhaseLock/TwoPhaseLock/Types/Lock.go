package Types

import (
	"errors"
)

/**
* @Class Lock
 */

type Lock struct {
	Transaction int
	TypeLock    string
}

func (l Lock) IsExclusive() bool {
	return l.TypeLock == "XL"
}

func (l Lock) IsShared() bool {
	return l.TypeLock == "SL"
}

func (l *Lock) Upgrade() error {
	if (*l).IsExclusive() {
		return errors.New("already XL")
	}
	(*l).TypeLock = "XL"
	return nil
}

func (l Lock) IsEqualTransaction(operation Operation) bool {
	return l.Transaction == operation.Transaction
}

func (l Lock) ToOperation(resource string) Operation {
	operation := Operation{Transaction: l.Transaction, Action: l.TypeLock, Resource: resource}
	return operation
}

/**
* @Class LockTable
 */

type LockTable struct {
	Map map[string][]Lock
}

func (t *LockTable) New() {
	(*t).Map = make(map[string][]Lock)
}

func (t LockTable) GetResourceLock(operation Operation) ([]Lock, bool) {
	value, found := t.Map[operation.Resource]
	return value, found
}

func (t *LockTable) SetLock(resource string, locks []Lock) {
	(*t).Map[resource] = locks
}

func (t *LockTable) Unlock(operation Operation) {
	locks, found := (*t).Map[operation.Resource]

	if !found {
		return
	}

	curr := -1
	for i, lock := range locks {
		if lock.Transaction == operation.Transaction {
			curr = i
			break
		}
	}

	locks = append(locks[:curr], locks[curr+1:]...)

	(*t).Map[operation.Resource] = locks
}

func GetLockTransaction(operation Operation, locks []Lock) (lock Lock) {
	for _, l := range locks {
		if l.Transaction == operation.Transaction {
			lock = l
		}
	}
	return lock
}

func GetOtherLockTransaction(operation Operation, locks []Lock) (lock Lock) {
	for _, l := range locks {
		if l.Transaction != operation.Transaction {
			lock = l
		}
	}
	return lock
}

func (t *LockTable) UpgradeLock(resource string) error {
	locks := (*t).Map[resource]

	if len(locks) != 1 {
		return errors.New("")
	}

	if err := locks[0].Upgrade(); err != nil {
		return errors.New("")
	}

	(*t).Map[resource] = locks

	return nil
}

//func (t LockTable) CheckAccess(operation Operation) {
//	value, found := t.Map[operation.Resource]
//
//	if !found {
//		lock := Lock{Transaction: operation.Transaction}
//		if operation.Action == "R" {
//			lock.TypeLock = "SL"
//		} else if operation.Action == "W" {
//			lock.TypeLock = "XL"
//		}
//		t.Map[operation.Resource] = lock
//
//		return
//	}
//
//	if value.Transaction == operation.Transaction {
//		if operation.Action == "R" && value.TypeLock == "SL" {
//
//		}
//	}
//}
