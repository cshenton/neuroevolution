"""The Policy Network class for GA learned policies in the atari domain."""
import numpy as np
import tensorflow as tf


ATARI_DIMS = [210, 160, 3]


class Policy:
    """Atari policy network.

    This matches the network architecture from the original DQN paper, but exposes
    all network weights in a single variable so they can conveniently be swapped
    out to evaluate different policies.

    Attributes:
        n_actions (int): Number of actions in the current atari environment.
        weights (list of tf.Variable): The network weight variables.
        input (tf.Placeholder): The state input placeholder.
        logits (tf.Tensor): The output policy logits.
        action (tf.Tensor): A multinomial draw over the policy logits.
        sess (tf.Session): The session used to run the policy network.
    """

    def __init__(self, n_actions):
        """Creates the policy network graph.

        Args:
            n_actions (int): Dimension of softmax action policy output.
        """
        self.n_actions = n_actions

        # Initializer with fixed seed
        init = tf.contrib.layers.variance_scaling_initializer(seed=42)

        # Weights Variables
        conv1 = tf.Variable(init([8, 8, 3, 16]), trainable=False)
        conv2 = tf.Variable(init([4, 4, 16, 32]), trainable=False)
        dens1 = tf.Variable(init([17280, 256]), trainable=False)
        dens2 = tf.Variable(init([256, n_actions]), trainable=False)
        self.weights = [conv1, conv2, dens1, dens2]

        # Feed forward network defined with functional ops
        self.input = tf.placeholder(tf.float32, [None] + ATARI_DIMS)
        x = self.input
        x = tf.nn.relu(tf.nn.conv2d(x, conv1, [1, 4, 4, 1], "SAME"))
        x = tf.layers.batch_normalization(x)
        x = tf.nn.relu(tf.nn.conv2d(x, conv2, [1, 2, 2, 1], "SAME"))
        x = tf.layers.batch_normalization(x)
        x = tf.layers.flatten(x)
        x = tf.matmul(x, dens1)
        x = tf.nn.relu(tf.layers.batch_normalization(x))
        x = tf.matmul(x, dens2)
        self.logits = x
        self.action = tf.multinomial(self.logits, 1)

        self.sess = tf.Session()

    def act(self, state):
        """Computes a forward pass through the policy graph, returns an action.

        Args:
            state (np.ndarray): The [210, 160, 3] Atari game state.

        Returns:
            action: The chosen integer action.
        """
        a = self.sess.run(self.action, feed_dict={self.input: np.expand_dims(state, 0)})

        action = a[0][0]
        return action

    def set_weights(self, seeds, strength):
        """Sets the graph weights given a sequence of random seeds to do so.

        Reruns the initializer, reads the variable value, adds noise to it in
        numpy according to the provided seeds, strength, then directly loads
        the new value into the Variable.

        It is important that this function does not add ops to the graph.

        Args:
            seeds (list of ints): The list of integer random seeds to use for
                random perturbation of the network weights.
            strength (float): The mutation strength or random scale.
        """
        self.sess.run(tf.global_variables_initializer())
        rands = [np.random.RandomState(s) for s in seeds]

        for w in self.weights:
            new_w = self.sess.run(w)
            size = new_w.shape
            for r in rands:
                new_w += r.normal(0, strength, size=size)
            w.load(new_w, self.sess)
