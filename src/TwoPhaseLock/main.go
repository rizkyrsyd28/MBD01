package main

import (
	"TwoPhaseLock/TwoPhaseLock"
	"os"
	"strconv"
)

func main() {
	var argsRaw = os.Args
	args := argsRaw[1:]

	parseInput := TwoPhaseLock.ParseTxt(args[0])
	verbose := false

	if len(args) > 1 {
		verbose, _ = strconv.ParseBool(args[1])
	}

	t := TwoPhaseLock.TwoPhaseLock{Verbose: verbose}
	t.Execute(parseInput)

	TwoPhaseLock.PrintResult(TwoPhaseLock.ParseTxt(args[0]), t.Schedule)
}
