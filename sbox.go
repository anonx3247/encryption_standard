package main

import (
	"fmt"
)

type Pair struct {
	input  int
	output int
}

func Sbox(x int) int {
	return x ^ 5
}

func main() {
	testSbox(Sbox)
}

func testSbox(sbox func(int) int) {
	top_pairs := differentialCryptanalysis(sbox)
	top_linear_pairs := linearCryptanalysis(sbox)

	fmt.Println("Top Differential Pairs:")
	for _, pair := range top_pairs {
		fmt.Printf("Input: %d, Output: %d\n", pair.input, pair.output)
	}

	fmt.Println("Top Linear Pairs:")
	for _, pair := range top_linear_pairs {
		fmt.Printf("Input: %d, Output: %d\n", pair.input, pair.output)
	}
}

func differentialCryptanalysis(sbox func(int) int) []Pair {
	/*
		We will use the following approach:
		sample N random pairs of inputs and outputs
	*/
}

func linearCryptanalysis(sbox func(int) int) []Pair {
	/*
		Perform linear cryptanalysis on the Sbox
	*/
}
