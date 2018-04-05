package main

import (
	"log"
	"net"
	"time"

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

	// Background save task
	ticker := time.NewTicker(time.Minute)
	go func() {
		for {
			<-ticker.C
			_ = s.Save()
			// save the bytes timestamped to s3
		}
	}()

	srv := grpc.NewServer()
	proto.RegisterNeuroServer(srv, s)
	if err := srv.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
