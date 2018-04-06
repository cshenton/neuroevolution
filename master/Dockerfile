FROM golang:latest AS build-env

ENV GOPATH=/go
ENV GOOS=linux
ENV GOARCH=amd64
ENV CGO_ENABLED=0

ADD master/ /go/src/github.com/cshenton/neuroevolution/master/
ADD proto/neuroevolution.pb.go /go/src/github.com/cshenton/neuroevolution/proto/neuroevolution.pb.go
RUN cd /go/src/github.com/cshenton/neuroevolution && \
    go get ./... && \
    go build -a -v -o ./runmaster ./master/main/main.go


FROM alpine
WORKDIR /
COPY --from=build-env /go/src/github.com/cshenton/neuroevolution/runmaster /master

ENV BUCKET experiment-bucket
ENV NAME atari-experiment
ENV PORT :8080
ENV REGION ap-southeast-2

ENTRYPOINT ./master