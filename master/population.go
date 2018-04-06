package master

import (
	"fmt"
	"math"
	"math/rand"
	"sort"
	"sync"

	"github.com/cshenton/neuroevolution/proto"
)

// Population is a genetic population that exposes threadsafe methods for generating
// new individuals and updating the list of elites.
type Population struct {
	Elites     [][]uint32 // The current generation's elites
	Scores     []float64  // The corresponding scores of the current elites
	PrevElites [][]uint32 // The previous generation's elites

	EliteSize   int // Size of the elites population
	GenSize     int // Size of a full generation
	GenNum      int // Number generation we're on (starting at 0)
	GenProgress int // Progress through the current generation

	*sync.Mutex
}

// NewPopulation creates a new, empty population of n elites with empty seeds and worst
// case scores.
func NewPopulation(eliteSize, genSize int) (p *Population) {
	// Make population of worst case 'degenerate' individuals.
	e := make([][]uint32, eliteSize)
	s := make([]float64, eliteSize)
	pe := make([][]uint32, eliteSize)
	for i := range e {
		e[i] = []uint32{}
		s[i] = math.Inf(-1)
		pe[i] = []uint32{}
	}

	p = &Population{
		Elites:     e,
		Scores:     s,
		PrevElites: pe,

		EliteSize:   eliteSize,
		GenSize:     genSize,
		GenNum:      0,
		GenProgress: 0,

		Mutex: &sync.Mutex{},
	}
	return p
}

// Select generates a new individual by randomly selecting an Elite from the previous
// generation and appending a new random seed to it.
func (p *Population) Select() (i *proto.Individual) {
	p.Lock()
	parent := p.PrevElites[rand.Intn(p.EliteSize)]
	i = &proto.Individual{
		Seeds: append(parent, rand.Uint32()),
	}
	p.Unlock()
	return i
}

// Evaluate updates the population with the provided individual, score. If the score
// is less than the worst elite, the individual is discarded, otherwise it is inserted
// into the population, and the worst elite is discarded. If this Evaluate completes
// a generation, the elites become the previous elites, and the best invdividual gets
// carried over.
func (p *Population) Evaluate(e *proto.Evaluation) {
	p.Lock()

	p.GenProgress++
	if e.Score > p.Scores[0] {
		ins := sort.SearchFloat64s(p.Scores, e.Score)

		for i := 0; i < ins-1; i++ {
			p.Scores[i] = p.Scores[i+1]
			p.Elites[i] = p.Elites[i+1]
		}
		p.Scores[ins-1] = e.Score
		p.Elites[ins-1] = e.Individual.Seeds
	}

	if p.GenProgress >= p.GenSize {
		// Get best individual, score
		best := p.Elites[p.EliteSize-1]
		bestScore := p.Scores[p.EliteSize-1]
		fmt.Printf("Top in gen: %v, with score %v\n", best, bestScore)

		// Progress a generation
		p.PrevElites = p.Elites
		p.Elites = make([][]uint32, p.EliteSize)
		p.Scores = make([]float64, p.EliteSize)
		for i := range p.Elites {
			p.Elites[i] = []uint32{}
			p.Scores[i] = math.Inf(-1)
		}
		// Carry over best individual automatically
		p.Elites[p.EliteSize-1] = best
		p.Scores[p.EliteSize-1] = bestScore
		// Increment generation counter, reset progress
		p.GenNum++
		p.GenProgress = 0
	}

	p.Unlock()
	return
}

// Count returns the total number of individuals evaluated.
func (p *Population) Count() int {
	return p.GenNum*p.GenSize + p.GenProgress
}

// Top returns the top individual
func (p *Population) Top() (t *proto.Top) {
	p.Lock()
	t = &proto.Top{
		TopIndividual: &proto.Individual{
			Seeds: p.Elites[p.EliteSize-1],
		},
		TopScore: p.Scores[p.EliteSize-1],
		NumIter:  int32(p.Count()),
	}
	p.Unlock()
	return t
}
