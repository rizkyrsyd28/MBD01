package Types

import "fmt"

type Operation struct {
	Transaction int
	Action      string
	Resource    string
}

func (o *Operation) ToString() string {
	return fmt.Sprintf("%s%d(%s)", o.Action, o.Transaction, o.Resource)
}
