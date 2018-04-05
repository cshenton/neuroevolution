"""The worker run script."""
import grpc
import gym

from proto.neuroevolution_pb2_grpc import NeuroStub
from worker.policy import Policy


HOST = 'localhost:8080'

ENVIRONMENT = 'SpaceInvaders-v1'
STRENGTH = 0.005

def main():
    chan = grpc.insecure_channel(HOST)
    stub = NeuroStub(chan)

    e = gym.make(ENVIRONMENT)
    p = Policy(e.num_actions)
    c =

    while True:



if __name__ == '__main__':
    main()