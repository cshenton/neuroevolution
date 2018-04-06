package master

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
)

// Saver is responsible for saving progress reports to s3
type Saver struct {
	bucket string
	name   string
	sess   *session.Session
}

// NewSaver creates a progress saver associated with a bucket in a region.
func NewSaver(name, bucket, region string) (s *Saver, err error) {
	sess, err := session.NewSession(&aws.Config{Region: aws.String(region)})
	if err != nil {
		return nil, err
	}

	s = &Saver{
		sess: sess,
	}
	return s, nil
}

// Save saves the current population state to s3
func (s *Saver) Save(p *Population) {
	// Serialise the population as json
	p.Lock()
	b, _ := json.Marshal(p)
	p.Unlock()

	key := s.name + time.Now().String()

	// wtf is this API aws!?
	_, err := s3.New(s.sess).PutObject(&s3.PutObjectInput{
		Bucket:        aws.String(s.bucket),
		Key:           aws.String(key),
		Body:          bytes.NewReader(b),
		ContentLength: aws.Int64(int64(len(b))),
		ContentType:   aws.String(http.DetectContentType(b)),
	})

	if err != nil {
		log.Print(err)
	}
	return
}

// Run runs save once per minute in the background, logs any save failures.
func (s *Saver) Run(p *Population) {
	// Background save task
	ticker := time.NewTicker(time.Minute)
	go func() {
		for {
			<-ticker.C
			s.Save(p)
		}
	}()
}
