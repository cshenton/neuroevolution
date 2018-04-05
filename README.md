# neuroevolution
Replication of Uber Neuroevolution paper


## Protobufs

Generate python stubs:
```
python -m grpc_tools.protoc -I . proto/neuroevolution.proto --python_out=. --grpc_python_out=.
```

Generate golang stubs:
```
protoc -I . proto/neuroevolution.proto --go_out=plugins=grpc:.
```