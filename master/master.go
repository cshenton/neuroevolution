package master

import (
	"context"

	"github.com/cshenton/neuroevolution/proto"
	"github.com/golang/protobuf/ptypes/empty"
)

// Server is the genetic algorithm server.
type Server struct {
	*Population
}

// New creates and returns a new server with an empty population.
func New() (s *Server) {
	s = &Server{}
	return s
}

// Seek returns a new individual to test.
func (s *Server) Seek(c context.Context, em *empty.Empty) (i *proto.Individual, err error) {

	// Randomly pick an individual from the current elites
	// Randomly generate a seed and append to that individual
	// Return the constructed individual
	return
}

// Show shows the performance of an individual to the server.
func (s *Server) Show(c context.Context, e *proto.Evaluation) (em *empty.Empty, err error) {
	// If score < min score, bail
	// Otherwise, insert the provided individual into the current elites.
	return
}
