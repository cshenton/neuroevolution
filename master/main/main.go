package main

import (
	"log"

	"github.com/cshenton/neuroevolution/master"
)

var (
	port = ":8080"
)

// Runs the server and the saver. Assumes that the ec2 instance / ecs task
// has host level permissions for s3 access.
func main() {
	s := master.New()
	if err := s.Run(port); err != nil {
		log.Fatal(err)
	}
}
