package master

import (
	"context"
	"fmt"
	"net"

	"github.com/cshenton/neuroevolution/proto"
	"github.com/golang/protobuf/ptypes/empty"
	"google.golang.org/grpc"
)

const eliteSize = 10
const genSize = 5000

// Server is the genetic algorithm server.
type Server struct {
	*Population
}

// New creates and returns a new server with an initialized population.
func New() (s *Server) {
	p := NewPopulation(eliteSize, genSize)
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
	em = &empty.Empty{}
	return em, nil
}

// Status shows the top individual
func (s *Server) Status(c context.Context, em *empty.Empty) (t *proto.Top, err error) {
	t = s.Top()
	return t, nil
}

// Run constructs and runs the NeuroServer grpc server.
func (s *Server) Run(port string) (err error) {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		return err
	}

	srv := grpc.NewServer()
	proto.RegisterNeuroServer(srv, s)
	fmt.Println("running")
	err = srv.Serve(lis) // this will block
	return err
}
