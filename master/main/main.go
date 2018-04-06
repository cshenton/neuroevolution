package main

import (
	"time"

	"github.com/cshenton/neuroevolution/master"
)

var port = ":8080"

func main() {
	s := master.New()

	// Background save task
	ticker := time.NewTicker(time.Minute)
	go func() {
		for {
			<-ticker.C
			_ = s.Save()
			// save the bytes timestamped to s3
		}
	}()

	s.Run(port)
}
