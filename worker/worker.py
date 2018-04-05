"""The worker run script."""
import grpc
import gym

from google.protobuf import empty_pb2
from proto.neuroevolution_pb2 import Evaluation, Individual
from proto.neuroevolution_pb2_grpc import NeuroStub
from worker.policy import Policy


HOST = 'localhost:8080'

ENVIRONMENT = 'SpaceInvaders-v1'
STRENGTH = 0.005


def main():
    chan = grpc.insecure_channel(HOST)
    stub = NeuroStub(chan)

    e = gym.make(ENVIRONMENT)
    p = Policy(e.action_space.n)

    while True:
        ind = stub.Seek(empty_pb2.Empty())
        p.set_weights(ind.seeds, STRENGTH)

        r = 0
        i = 0
        done = False
        state = e.reset()
        while not done:
            action = p.forward(state)
            state, reward, done, _ = e.step(action)
            r += reward
            if i > 20000:
                break

        stub.Show(Evaluation(
            individual=Individual(
                seeds=ind.seeds,
            ),
            score=r,
        ))


if __name__ == '__main__':
    main()