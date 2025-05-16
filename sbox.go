package main

import (
	"fmt"
	"math"
	"math/bits"
	"math/rand"
	"sort"
)

const (
	SIZE         = 64
	INPUT_SIZE   = 1 << (SIZE - 1)
	N            = 10000
	K            = 10000
	SEARCH_SPACE = 1 << 14
	TEST_COUNT   = 10
)

var UNCERTAINTY = 1.0 / math.Sqrt(float64(SEARCH_SPACE))

type Pair struct {
	input  uint64
	output uint64
	prob   float64
}

type Test struct {
	a                  uint64
	b                  uint64
	differential_pairs []Pair
	linear_pairs       []Pair
}

func Sbox(x, a, b uint64) uint64 {
	// c must be odd
	x = bits.RotateLeft64(x, 32)
	x ^= a
	x = x + x + x
	x ^= b
	return x
}

func main() {
	tests := make([]Test, TEST_COUNT)

	// Create a channel to collect results
	resultChan := make(chan struct {
		index int
		test  Test
	}, TEST_COUNT)

	// Launch goroutines for each test
	for i := 0; i < TEST_COUNT; i++ {
		go func(index int) {
			a := rand.Uint64()
			b := rand.Uint64()
			if b%2 == 0 {
				b++
			}
			f := func(x uint64) uint64 {
				return Sbox(x, a, b)
			}
			fmt.Printf("Testing Sbox %d with a = %d, b = %d\n", index, a, b)
			differential_pairs, linear_pairs := testSbox(f, false)
			fmt.Printf("Done testing Sbox %d\n", index)
			resultChan <- struct {
				index int
				test  Test
			}{index, Test{a, b, differential_pairs, linear_pairs}}
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

	best := func(x uint64) uint64 {
		return Sbox(x, tests[0].a, tests[0].b)
	}
	for i := uint64(0); i < 32; i++ {
		fmt.Printf("%d\n", best(i))
	}
}

func testSbox(sbox func(uint64) uint64, print_results bool) (differential_pairs []Pair, linear_pairs []Pair) {
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

func printDifferentialPairs(pairs []Pair, top_n int) {
	fmt.Println("Top Differential Pairs:")
	for _, pair := range pairs[:top_n] {
		fmt.Printf("Input: %d, Output: %d, Prob: %.4f\n", pair.input, pair.output, pair.prob)
	}
}

func printLinearPairs(pairs []Pair, top_n int) {
	fmt.Println("Top Linear Pairs:")
	for _, pair := range pairs[:top_n] {
		fmt.Printf("Input: %d, Output: %d, Bias: %.4f ± %.4f\n", pair.input, pair.output, pair.prob-0.5, UNCERTAINTY)
	}
}

func differentialCryptanalysis(sbox func(uint64) uint64) []Pair {
	best_differentials := []Pair{}

	for i := 0; i < N; i++ {
		alpha := rand.Uint64()
		beta_counter := make(map[uint64]int)
		for j := 0; j < K; j++ {
			m := rand.Uint64()
			m_prime := m ^ alpha
			beta := sbox(m) ^ sbox(m_prime)
			beta_counter[beta] += 1
		}
		most_common_beta := 0
		best_differential := uint64(0)
		for beta, count := range beta_counter {
			if count > most_common_beta {
				most_common_beta = count
				best_differential = beta
			}
		}
		best_differentials = append(best_differentials, Pair{alpha, best_differential, float64(most_common_beta) / float64(N)})
	}

	sort.Slice(best_differentials, func(i, j int) bool {
		return best_differentials[i].prob < best_differentials[j].prob
	})

	return best_differentials
}

func testDifferential(sbox func(uint64) uint64, alpha, beta uint64) float64 {
	counter := 0
	for i := 0; i < N; i++ {
		m := rand.Uint64()
		m_prime := m ^ alpha
		beta_prime := sbox(m_prime) ^ sbox(m)
		if beta_prime == beta {
			counter++
		}
	}
	return float64(counter) / float64(N)
}

func linearCryptanalysis(sbox func(uint64) uint64) []Pair {

	parity := func(v1, v2 uint64) uint64 {
		return uint64(bits.OnesCount64(v1&v2) & 1)
	}

	bias_approx := func(a, b uint64) float64 {
		// we will do a monte carlo approximation since the input space is too large

		lat_approx := 0
		for i := 0; i < SEARCH_SPACE; i++ {
			x := rand.Uint64()
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

	best_linear_pairs := make([]Pair, 0, N)

	for i := 0; i < N; i++ {
		a := rand.Uint64()
		b := rand.Uint64()

		epsilon := bias_approx(a, b)

		prob_abs_bias := 0.5 + math.Abs(epsilon)

		if epsilon < 0 {
			a = -a
		}

		if math.Abs(epsilon)-UNCERTAINTY > 1e-9 {
			best_linear_pairs = append(best_linear_pairs, Pair{a, b, prob_abs_bias})
		}
	}

	sort.Slice(best_linear_pairs, func(i, j int) bool {
		return best_linear_pairs[i].prob < best_linear_pairs[j].prob
	})

	return best_linear_pairs
}
