package master

import (
	"math"
	"math/rand"
	"sort"
	"sync"

	"github.com/cshenton/neuroevolution/proto"
)

// Population is a genetic population that exposes threadsafe methods for generating
// new individuals and updating the list of elites.
type Population struct {
	Elites    [][]uint64
	Scores    []float64
	NumElites int

	*sync.Mutex
}

// NewPopulation creates a new, empty population of n elites with empty seeds and worst
// case scores.
func NewPopulation(n int) (p *Population) {
	// Make population of worst case score 'gaia' individuals.
	e := make([][]uint64, n)
	s := make([]float64, n)
	for i := range e {
		e[i] = []uint64{}
		s[i] = math.Inf(-1)
	}

	p = &Population{
		Elites:    e,
		Scores:    s,
		NumElites: n,

		Mutex: &sync.Mutex{},
	}
	return p
}

// Select generates a new individual by randomly selecting an Elite and appending
// a new random seed to it.
func (p *Population) Select() (i *proto.Individual) {
	p.Lock()
	parent := p.Elites[rand.Intn(p.NumElites)]
	i = &proto.Individual{
		Seeds: append(parent, rand.Uint64()),
	}
	p.Unlock()
	return i
}

// Evaluate updates the population with the provided individual, score. If the score
// is less than the worst elite, the individual is discarded, otherwise it is inserted
// into the population, and the worst elite is discarded.
func (p *Population) Evaluate(e *proto.Evaluation) {
	p.Lock()
	defer p.Unlock()
	if e.Score <= p.Scores[0] {
		return
	}
	ins := sort.SearchFloat64s(p.Scores, e.Score)
	p.Scores = append(append(p.Scores[1:ins], e.Score), p.Scores[ins:len(p.Scores)]...)
	p.Elites = append(append(p.Elites[1:ins], e.Individual.Seeds), p.Elites[ins:len(p.Elites)]...)
	return
}
