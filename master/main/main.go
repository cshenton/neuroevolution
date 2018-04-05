package main

import (
	"log"
	"net"

	"github.com/cshenton/neuroevolution/master"
	"github.com/cshenton/neuroevolution/proto"
	"google.golang.org/grpc"
)

var port = ":8080"

func main() {
	s := master.New()

	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	srv := grpc.NewServer()
	proto.RegisterNeuroServer(srv, s)
	if err := srv.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
