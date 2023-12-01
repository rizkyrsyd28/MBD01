package TwoPhaseLock

import (
	types "TwoPhaseLock/TwoPhaseLock/Types"
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func ParseInput(raw []string) []types.Operation {
	result := make([]types.Operation, 0)

	pattern := regexp.MustCompile(`^([RW]|XL|SL|UL)(\d+)?\((\w+)\)?$`)
	for _, op := range raw {
		result = append(result, parseRegex(op, pattern))
	}

	return result
}

func parseRegex(raw string, pattern *regexp.Regexp) types.Operation {
	operation := types.Operation{}

	match := pattern.FindStringSubmatch(raw)

	if len(match) > 0 {
		operation.Action = match[1]
		operation.Transaction, _ = strconv.Atoi(match[2])
		operation.Resource = match[3]
	} else if len(raw) == 2 {
		if raw[0] == 'C' {
			operation.Action = string(raw[0])
			operation.Transaction, _ = strconv.Atoi(string(raw[1]))
		}
	}

	return operation
}

func pop(arr *[]types.Operation, i int) (operation types.Operation) {
	if i < 0 || i >= len(*arr) {
		return operation
	}

	operation = (*arr)[i]

	*arr = append((*arr)[:i], (*arr)[i+1:]...)

	return operation
}

func ParseTxt(filepath string) (operation []types.Operation) {
	var raw []string

	file, err := os.Open(filepath)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if !(line[0] == '-' || line[0] == 'T') {
			raw = append(raw, line)
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return ParseInput(raw)
}

func PrintResult(raw []types.Operation, final []types.Operation) {
	builder := strings.Builder{}

	for i, ops := range raw {
		builder.WriteString(fmt.Sprintf(" %s ", ops.ToString()))
		if i != len(raw)-1 {
			builder.WriteString(fmt.Sprint(","))
		}
	}
	fmt.Printf("Input: [%s]\n", builder.String())

	builder = strings.Builder{}

	for i, ops := range final {
		builder.WriteString(fmt.Sprintf(" %s ", ops.ToString()))
		if i != len(final)-1 {
			builder.WriteString(fmt.Sprint(","))
		}
	}

	fmt.Printf("Final: [%s]\n", builder.String())
}
