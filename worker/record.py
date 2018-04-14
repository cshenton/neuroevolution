import gym
import os
from worker.policy import Policy

def record_episode(env_name, seed):
    """Records and saves an episode on the specified environment.

    Args:
        env_name (string): The valid gym environment name to run.
        seed (list of ints): The seed sequence defining the policy.
    """
    env = gym.wrappers.Monitor(
        env=gym.make(env_name),
        directory=os.path.join(os.getcwd(), "video"),
        video_callable=lambda i: True,
        force=True,
    )
    p = Policy(env.action_space.n)
    p.set_weights(seed, 0.005)

    done = False
    state = env.reset()
    while not done:
        action = p.act(state)
        state, reward, done, _ = env.step(action)
