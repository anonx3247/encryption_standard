package main

import (
	"fmt"
	"math"
	"math/bits"
	"math/rand"
	"runtime"
	"sort"
	"sync"
	"time"
)

const (
	SIZE         = 64
	INPUT_SIZE   = 1 << (SIZE - 1)
	N            = 10000
	K            = 10000
	SEARCH_SPACE = 1 << 12
	TEST_COUNT   = 100
)

var UNCERTAINTY = 1.0 / math.Sqrt(float64(SEARCH_SPACE))

type Number interface {
	uint32 | uint64 | uint16
}
type Pair[T Number] struct {
	input  T
	output T
	prob   float64
}

type Test[T Number] struct {
	a                  T
	b                  T
	c                  T
	d                  T
	differential_pairs []Pair[T]
	linear_pairs       []Pair[T]
}

var (
	a   uint64 = 11109033717525269061
	b   uint64 = 10403331604385742251
	a32 uint32 = 1110903371
	b32 uint32 = 1040333161
	a16 uint16 = 11109
	b16 uint16 = 10403
)

var operations = []struct {
	op   func(uint64) uint64
	cost int
}{
	{func(x uint64) uint64 { return x + a }, 3},
	{func(x uint64) uint64 { return x + x + x }, 6},
	{func(x uint64) uint64 { return x ^ b }, 2},
	{func(x uint64) uint64 { return x + b }, 3},
	{func(x uint64) uint64 { return x + x + x + x + x }, 9},
	{func(x uint64) uint64 { return x ^ a }, 2},
	{func(x uint64) uint64 { return bitRotate(x, 19) }, 10},
	{func(x uint64) uint64 { return bitRotate(x, 13) }, 10},
	{func(x uint64) uint64 { return x * x }, 50},
}

func sBox(x uint16) uint16 {
	x = bits.RotateLeft16(x, 13)
	x = ^(x ^ b16)
	x *= a16
	x = ^(x ^ a16)
	x *= b16
	x = bits.RotateLeft16(x, 7)
	return x
}

func bitRotate(x uint64, n int) uint64 {
	n64 := uint64(n)
	nInv := uint64(64 - n)
	return ((x << n64) | (x >> nInv))
}

func bitRotate32(x uint32, n int) uint32 {
	n32 := uint32(n)
	nInv := uint32(32 - n)
	return ((x << n32) | (x >> nInv))
}

func buildSbox() func(uint64) uint64 {
	totalCost := 0
	var ops []func(uint64) uint64
	for totalCost < 32 {
		idx := rand.Intn(len(operations))
		op := operations[idx].op
		cost := operations[idx].cost
		totalCost += cost
		ops = append(ops, op)
	}
	if totalCost > 100 {
		ops = ops[:len(ops)-1]
	}

	return func(x uint64) uint64 {
		for _, op := range ops {
			x = op(x)
		}
		return x
	}
}

func sequentialEvaluator(sbox func(uint64) uint64) float64 {
	inputs := make([]uint64, 1000)
	for i := range inputs {
		inputs[i] = uint64(i)
	}
	outputs := make([]uint64, 1000)
	for i, x := range inputs {
		outputs[i] = sbox(x)
	}
	diff := uint64(0)
	for i := 0; i < len(inputs)-1; i++ {
		diff += outputs[i] ^ outputs[i+1]
	}
	return float64(diff) / float64(len(inputs))
}

func findGoodSbox() func(uint64) uint64 {
	rand.Seed(time.Now().UnixNano())
	for i := 0; i < 10000; i++ {
		sbox := buildSbox()
		score := sequentialEvaluator(sbox)
		if score < 20 {
			return sbox
		}
	}
	panic("Failed to find a good sbox")
}

func testSboxes(n int) {
	scoresChan := make(chan float64, n)
	numCPU := runtime.NumCPU()
	chunkSize := n / numCPU
	if chunkSize == 0 {
		chunkSize = 1
	}
	var wg sync.WaitGroup

	for i := 0; i < numCPU && i*chunkSize < n; i++ {
		wg.Add(1)
		workerID := i
		go func() {
			defer wg.Done()
			for j := 0; j < chunkSize && workerID*chunkSize+j < n; j++ {
				sbox := buildSbox()
				fmt.Printf("Testing Sbox %d\n", workerID*chunkSize+j)
				results := differentialCryptanalysis(sbox)
				if len(results) > 0 {
					scoresChan <- results[0].prob
				} else {
					// If no results, send a default value
					scoresChan <- 0.0
				}
			}
		}()
	}

	// Wait for all goroutines to complete in a separate goroutine
	go func() {
		wg.Wait()
		close(scoresChan)
	}()

	scores := make([]float64, 0, n)
	for score := range scoresChan {
		scores = append(scores, score)
	}
	sort.Float64s(scores)

	// Only print scores if we have any
	numToPrint := 10
	if len(scores) < numToPrint {
		numToPrint = len(scores)
	}

	for i := 0; i < numToPrint; i++ {
		fmt.Printf("Sbox %d: %f\n", i, scores[i])
	}
}

func Sbox(x, a, b, c, d uint16) uint16 {
	// b and d must be odd
	if b%2 == 0 {
		b++
	}
	if d%2 == 0 {
		d++
	}
	x = bits.RotateLeft16(x, 13)
	x = ^(x ^ a)
	x *= b
	x = ^(x ^ c)
	x *= d
	x = bits.RotateLeft16(x, 7)
	return x
}

func main() {
	//_ = findGoodSbox()
	//fmt.Println("Found a good S-box!")
	//testSboxes(TEST_COUNT)
	testSbox(sBox, true)
	/*
		tests := make([]Test[uint16], TEST_COUNT)

		// Create a channel to collect results
		resultChan := make(chan struct {
			index int
			test  Test[uint16]
		}, TEST_COUNT)

		// Launch goroutines for each test
		for i := 0; i < TEST_COUNT; i++ {
			go func(index int) {
				a := uint16(rand.Uint64())
				b := uint16(rand.Uint64())
				c := uint16(rand.Uint64())
				d := uint16(rand.Uint64())
				if b%2 == 0 {
					b++
				}
				if d%2 == 0 {
					d++
				}
				f := func(x uint16) uint16 {
					return Sbox(x, a, b, c, d)
				}
				fmt.Printf("Testing Sbox %d with a = %d, b = %d, c = %d, d = %d\n", index, a, b, c, d)
				differential_pairs, linear_pairs := testSbox(f, false)
				fmt.Printf("Done testing Sbox %d\n", index)
				resultChan <- struct {
					index int
					test  Test[uint16]
				}{index, Test[uint16]{a, b, c, d, differential_pairs, linear_pairs}}
			}(i)
		}

		// Collect results
		for i := 0; i < TEST_COUNT; i++ {
			result := <-resultChan
			tests[result.index] = result.test
		}

		// Sorting can't be easily parallelized with the standard library
		sort.Slice(tests, func(j, k int) bool {
			if len(tests[j].differential_pairs) == 0 && len(tests[k].differential_pairs) != 0 {
				return false
			} else if len(tests[j].differential_pairs) != 0 && len(tests[k].differential_pairs) == 0 {
				return true
			} else if len(tests[j].linear_pairs) == 0 && len(tests[k].linear_pairs) != 0 {
				return false
			} else if len(tests[j].linear_pairs) != 0 && len(tests[k].linear_pairs) == 0 {
				return true
			}
			j_dif := tests[j].differential_pairs[0]
			k_dif := tests[k].differential_pairs[0]
			j_lin := tests[j].linear_pairs[0]
			k_lin := tests[k].linear_pairs[0]
			return j_dif.prob+j_lin.prob > k_dif.prob+k_lin.prob
		})

		// Process top 3 results
		for i, test := range tests[:3] {
			fmt.Printf("Test %d: a = %d, b = %d\n", i, test.a, test.b)
			printDifferentialPairs(test.differential_pairs, 3)
			printLinearPairs(test.linear_pairs, 3)
		}

		best := func(x uint16) uint16 {
			return Sbox(x, tests[0].a, tests[0].b, tests[0].c, tests[0].d)
		}
		for i := uint16(0); i < 32; i++ {
			fmt.Printf("%d\n", best(i))
		}
	*/
}

func testSbox[T Number](sbox func(T) T, print_results bool) (differential_pairs []Pair[T], linear_pairs []Pair[T]) {
	if print_results {
		fmt.Println("Testing Sbox")
	}
	differential_pairs = differentialCryptanalysis(sbox)
	linear_pairs = linearCryptanalysis(sbox)

	if print_results {
		printDifferentialPairs(differential_pairs, 10)
		printLinearPairs(linear_pairs, 10)
	}
	return
}

func printDifferentialPairs[T Number](pairs []Pair[T], top_n int) {
	fmt.Println("Top Differential Pairs:")
	for _, pair := range pairs[:top_n] {
		fmt.Printf("Input: %d, Output: %d, Prob: %.4f\n", pair.input, pair.output, pair.prob)
	}
}

func printLinearPairs[T Number](pairs []Pair[T], top_n int) {
	fmt.Println("Top Linear Pairs:")
	for _, pair := range pairs[:top_n] {
		fmt.Printf("Input: %d, Output: %d, Bias: %.4f ± %.4f\n", pair.input, pair.output, pair.prob-0.5, UNCERTAINTY)
	}
}

func differentialCryptanalysis[T Number](sbox func(T) T) []Pair[T] {
	best_differentials := []Pair[T]{}

	for i := 0; i < N; i++ {
		alpha := T(rand.Uint64())
		beta_counter := make(map[T]int)
		for j := 0; j < K; j++ {
			m := T(rand.Uint64())
			m_prime := m ^ alpha
			beta := sbox(m) ^ sbox(m_prime)
			beta_counter[beta] += 1
		}
		most_common_beta := 0
		best_differential := T(0)
		for beta, count := range beta_counter {
			if count > most_common_beta {
				most_common_beta = count
				best_differential = beta
			}
		}
		best_differentials = append(best_differentials, Pair[T]{alpha, best_differential, float64(most_common_beta) / float64(N)})
	}

	sort.Slice(best_differentials, func(i, j int) bool {
		return best_differentials[i].prob < best_differentials[j].prob
	})

	return best_differentials
}

func testDifferential[T Number](sbox func(T) T, alpha, beta T) float64 {
	counter := 0
	for i := 0; i < N; i++ {
		m := T(rand.Uint64())
		m_prime := m ^ alpha
		beta_prime := sbox(m_prime) ^ sbox(m)
		if beta_prime == beta {
			counter++
		}
	}
	return float64(counter) / float64(N)
}

func linearCryptanalysis[T Number](sbox func(T) T) []Pair[T] {
	var parity func(T, T) T
	switch any(T(0)).(type) {
	case uint32:
		parity = func(v1, v2 T) T {
			return T(bits.OnesCount32(uint32(v1)&uint32(v2)) & 1)
		}
	case uint64:
		parity = func(v1, v2 T) T {
			return T(bits.OnesCount64(uint64(v1)&uint64(v2)) & 1)
		}
	case uint16:
		parity = func(v1, v2 T) T {
			return T(bits.OnesCount16(uint16(v1)&uint16(v2)) & 1)
		}
	}

	bias_approx := func(a, b T) float64 {
		lat_approx := 0
		for i := 0; i < SEARCH_SPACE; i++ {
			x := T(rand.Uint64())
			ax_parity := parity(a, x)
			bs_parity := parity(b, sbox(x))

			if (ax_parity ^ bs_parity) == 0 {
				lat_approx++
			} else {
				lat_approx--
			}
		}
		epsilon := float64(lat_approx) / (2.0 * float64(SEARCH_SPACE))
		return epsilon
	}

	best_linear_pairs := make([]Pair[T], 0, N)

	for i := 0; i < N; i++ {
		a := T(rand.Uint64())
		b := T(rand.Uint64())

		epsilon := bias_approx(a, b)
		prob_abs_bias := 0.5 + math.Abs(epsilon)

		if epsilon < 0 {
			a = -a
		}

		if math.Abs(epsilon)-UNCERTAINTY > 1e-9 {
			best_linear_pairs = append(best_linear_pairs, Pair[T]{a, b, prob_abs_bias})
		}
	}

	sort.Slice(best_linear_pairs, func(i, j int) bool {
		return best_linear_pairs[i].prob < best_linear_pairs[j].prob
	})

	return best_linear_pairs
}
