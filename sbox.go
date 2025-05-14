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
	SEARCH_SPACE = 1 << 16
)

var UNCERTAINTY = 1.0 / math.Sqrt(float64(SEARCH_SPACE))

type Pair struct {
	input  uint64
	output uint64
	prob   float64
}

func Sbox(x uint64) uint64 {
	return x ^ (x >> 1)
}

func main() {
	testSbox(Sbox)
}

func testSbox(sbox func(uint64) uint64) {
	fmt.Println("Testing Sbox")
	top_pairs := differentialCryptanalysis(sbox)
	top_linear_pairs := linearCryptanalysis(sbox)

	fmt.Println("Top Differential Pairs:")
	for _, pair := range top_pairs[:10] {
		fmt.Printf("Input: %d, Output: %d (Prob: %.4f)\n", pair.input, pair.output, pair.prob)
	}

	fmt.Println("Top Linear Pairs:")
	for _, pair := range top_linear_pairs[:10] {
		fmt.Printf("Input: %d, Output: %d, Bias: %.4f ± %.4f\n", pair.input, pair.output, pair.prob-0.5, UNCERTAINTY)
	}
}

func differentialCryptanalysis(sbox func(uint64) uint64) []Pair {
	/*
		We will use the following approach:
		sample N random pairs of inputs and outputs
	*/
	fmt.Println("Differential Cryptanalysis...")

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
		return best_differentials[i].prob > best_differentials[j].prob
	})

	return best_differentials
}

func linearCryptanalysis(sbox func(uint64) uint64) []Pair {
	/*
		Perform linear cryptanalysis on the Sbox
	*/
	fmt.Println("Linear Cryptanalysis...")

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
		return best_linear_pairs[i].prob > best_linear_pairs[j].prob
	})

	return best_linear_pairs
}
