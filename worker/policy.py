"""Policy Network class"""

class Policy:
    """Atari policy network."""

    def __init__(self, n_actions):
        """Creates the policy network graph.

        Args:
            n_actions (int): Dimension of softmax action policy output.
        """
        pass

    def forward(self, state):
        """Computes a forward pass through the policy graph, returns an action.

        Args:
            state (gym.State): The OpenAI gym game state.

        Returns:
            action: The chosen action.
        """
        pass

    def set_weights(self, seeds, strength):
        """Sets the graph weights given a sequence of random seeds to do so.

        Args:
            seeds (list of ints): The list of integer random seeds to use for
                random perturbation of the network weights.
            strength (float): The mutation strength or random scale.
        """
        pass
