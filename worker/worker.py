"""The Worker class, which manages running policy evaluations."""
import datetime
import grpc
import gym
import os

from google.protobuf import empty_pb2
from proto.neuroevolution_pb2 import Evaluation, Individual
from proto.neuroevolution_pb2_grpc import NeuroStub
from worker.policy import Policy


ENVIRONMENT = os.getenv("ENVIRONMENT", "Venture-v4")
HOST = os.getenv("HOST_ADDRESS", "127.0.0.1") + ":" + os.getenv("HOST_PORT", "8080")
MUTATION_STRENGTH = float(os.getenv("MUTATION_STRENGTH", "0.005"))


class Worker:
    """Worker manages the evaluation of candidate policies from the master server.

    Attributes:
        client (NeuroStub): The client stub to the master server.
        env (gym.Env): The gym environment being evaluated.
        policy (Policy): The policy network, with changeable weights.
        strength (float): The genetic mutation strength.
    """

    def __init__(self, env_name=ENVIRONMENT, strength=MUTATION_STRENGTH, host=HOST):
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

        print("Host:", host)
        print("Environment:", env_name)
        print("Mutation Strength:", strength)

    def seek(self):
        """Gets a new set of seeds to try from the master server.

        Returns:
            seeds (list of ints): The seed sequence defining the next policy
                to try out.
        """
        return self.client.Seek(empty_pb2.Empty(), timeout=30).seeds

    def show(self, seeds, score):
        """Sends the seeds and corresponding score to the master server.

        Args:
            seeds (list of ints): The seed sequence defining a policy.
            score (float): The score it achieved on the environment.
        """
        self.client.Show(
            Evaluation(
                individual=Individual(
                    seeds=seeds,
                ),
                score=score,
            ),
            timeout=30,
        )

    def run_one(self):
        """Gets, evaluates, and reports a policy."""
        t = datetime.datetime.now()
        seeds = self.seek()
        self.policy.set_weights(seeds, self.strength)
        setup_time = datetime.datetime.now() - t
        t = datetime.datetime.now()
        i = 0
        score = 0
        done = False
        state = self.env.reset()
        while not done:
            action = self.policy.act(state)
            state, reward, done, _ = self.env.step(action)
            score += reward
            i += 1
            if i >= 20000:
                break
        self.show(seeds, score)
        run_time = datetime.datetime.now() - t
        print(
            "Score: ", score,
            "Seeds: ", seeds,
            "Frames: ", i,
            "Setup Time: ", setup_time,
            "Run Time: ", run_time,
            "FPS during run: ", i / run_time.total_seconds()
        )

    def run(self):
        """Repeatedly gets, evaluates, and reports a policy."""
        while True:
            self.run_one()
