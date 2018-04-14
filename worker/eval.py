import gym
import os
from worker.policy import Policy

def evaluate_policy(env_name, seed, runs=100):
    """Evaluates the given seed on the environment over many runs.

    Args:
        env_name (string): The valid gym environment name to run.
        seed (list of ints): The seed sequence defining the policy.

    Returns:
        float: The average score over the runs.
    """
    env = gym.make(env_name)
    p = Policy(env.action_space.n)
    p.set_weights(seed, 0.005)

    total = 0

    for i in range(runs):
        done = False
        score = 0
        state = env.reset()
        while not done:
            action = p.act(state)
            state, reward, done, _ = env.step(action)
            score += reward
        total += score
        print("Average score over {} runs: {}".format(i+1, total/(i+1)))

    return total / runs
