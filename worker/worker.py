"""The Worker class, which manages running policy evaluations."""
import grpc
import gym
import os

from google.protobuf import empty_pb2
from proto.neuroevolution_pb2 import Evaluation, Individual
from proto.neuroevolution_pb2_grpc import NeuroStub
from worker.policy import Policy


ENVIRONMENT = os.getenv("ENVIRONMENT", "Pong-v4")
HOST = os.getenv("HOST", "127.0.0.1:8080")
DEFAULT_STRENGTH = 0.005


class Worker:
    """Worker manages the evaluation of candidate policies from the master server.

    Attributes:
        client (NeuroStub): The client stub to the master server.
        env (gym.Env): The gym environment being evaluated.
        policy (Policy): The policy network, with changeable weights.
        strength (float): The genetic mutation strength.
    """

    def __init__(self, env_name=ENVIRONMENT, strength=DEFAULT_STRENGTH, host=HOST):
        """Creates a Worker instance.

        Args:
            env (string): The valid gym environment name.
            host (string): The hostname of the master server.
            strength (float): The genetic mutation strength.
        """
        self.client = NeuroStub(grpc.insecure_channel(host))
        self.env = gym.make(env_name)
        self.policy = Policy(self.env.action_space.n)
        self.strength = strength

    def seek(self):
        """Gets a new set of seeds to try from the master server.

        Returns:
            seeds (list of ints): The seed sequence defining the next policy
                to try out.
        """
        return self.client.Seek(empty_pb2.Empty()).seeds

    def show(self, seeds, score):
        """Sends the seeds and corresponding score to the master server.

        Args:
            seeds (list of ints): The seed sequence defining a policy.
            score (float): The score it achieved on the environment.
        """
        self.client.Show(Evaluation(
            individual=Individual(
                seeds=seeds,
            ),
            score=score,
        ))

    def run_one(self):
        """Gets, evaluates, and reports a policy."""
        seeds = self.seek()
        self.policy.set_weights(seeds, self.strength)
        i = 0
        score = 0
        done = False
        state = self.env.reset()
        while not done:
            action = self.policy.act(state)
            state, reward, done, _ = self.env.step(action)
            score += reward
            if i >= 20000:
                break
        self.show(seeds, score)
        print(score, seeds)

    def run(self):
        """Repeatedly gets, evaluates, and reports a policy."""
        while True:
            self.run_one()
