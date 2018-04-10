"""Simple monitoring script for a run."""
import grpc
import time

from google.protobuf import empty_pb2
from proto.neuroevolution_pb2_grpc import NeuroStub
from proto.neuroevolution_pb2 import Top


HOST = "ec2-13-211-134-103.ap-southeast-2.compute.amazonaws.com:8080"

client = NeuroStub(grpc.insecure_channel(HOST))

while True:
    top = client.Status(empty_pb2.Empty())
    print(
        "i: {} \t Top score: {} \t Top seed: {}".format(
        top.num_iter, top.top_score, top.top_individual.seeds)
    )
    time.sleep(15)