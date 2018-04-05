package master

import (
	"context"

	"github.com/cshenton/neuroevolution/proto"
	"github.com/golang/protobuf/ptypes/empty"
)

const popSize = 25

// Server is the genetic algorithm server.
type Server struct {
	*Population
}

// New creates and returns a new server with an empty population.
func New() (s *Server) {
	p := NewPopulation(popSize)
	s = &Server{
		Population: p,
	}
	return s
}

// Seek returns a new individual to test.
func (s *Server) Seek(c context.Context, em *empty.Empty) (i *proto.Individual, err error) {
	i = s.Select()
	return i, nil
}

// Show shows the performance of an individual to the server.
func (s *Server) Show(c context.Context, e *proto.Evaluation) (em *empty.Empty, err error) {
	s.Evaluate(e)
	return
}
