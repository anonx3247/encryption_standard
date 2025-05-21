package main

import (
	"fmt"
	"math/bits"
	"math/rand"
	"sort"
)

type MatrixEval struct {
	Matrix [64]uint64
	Eval   int
}

// Matrix multiplication for binary 64x64 matrix with 64-bit vectors
func multiplyMatrixVector(matrix [64]uint64, vector uint64) uint64 {
	/*
		This comes down to xoring the colums of the matrix that correspond to the 1s in the vector.
	*/
	var result uint64 = 0
	for j := 0; j < 64; j++ {
		if (vector>>j)&1 == 1 {
			result ^= matrix[j]
		}
	}
	return result
}

func xor(a, b bool) bool {
	return a != b
}

func B_d(L [64]uint64, K int) int {
	B_d := make([]int, K)
	for i := 0; i < K; i++ {
		x := randVector()
		B_d[i] += bits.OnesCount(uint(x))
		y := multiplyMatrixVector(L, x)
		B_d[i] += bits.OnesCount(uint(y))
	}

	sort.Ints(B_d)

	return B_d[0]
}

func findL(N, K int) MatrixEval {
	eval := make([]MatrixEval, N)
	evalChan := make(chan MatrixEval, N)
	for i := 0; i < N; i++ {
		go func() {
			L := randMatrix()
			fmt.Printf("Testing Matrix: %x\n", L[0])
			evalChan <- MatrixEval{L, B_d(L, K)}
		}()
	}

	for i := 0; i < N; i++ {
		eval[i] = <-evalChan
	}

	sort.Slice(eval, func(i, j int) bool {
		return eval[i].Eval > eval[j].Eval
	})

	return eval[0]
}

func randMatrix() [64]uint64 {
	L := [64]uint64{}
	init := rand.Uint64()
	for i := 0; i < 64; i++ {
		L[i] = bits.RotateLeft64(uint64(init), i)
	}
	return L
}

func randVector() uint64 {
	return rand.Uint64()
}

/*
func main() {
	num_matrices := 100000
	num_tests := 100000
	eval := findL(num_matrices, num_tests)
	fmt.Printf("Matrix: %x\n", eval.Matrix[0])
	fmt.Printf("Eval: %d\n", eval.Eval)
}
*/
