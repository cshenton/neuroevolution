package main

import (
	"log"
	"os"

	"github.com/cshenton/neuroevolution/master"
)

var (
	bucket = os.Getenv("BUCKET")
	name   = os.Getenv("NAME")
	port   = os.Getenv("PORT")
	region = os.Getenv("REGION")
)

// Runs the server and the saver. Assumes that the ec2 instance / ecs task
// has host level permissions for s3 access.
func main() {
	s := master.New()
	sv, err := master.NewSaver(name, bucket, region)
	if err != nil {
		log.Fatal(err)
	}
	sv.Run(s.Population)
	err = s.Run(port) // should block
	if err != nil {
		log.Fatal(err)
	}
}
