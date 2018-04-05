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
        weights (tf.Variable): The global network weights variable.
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

        # Global weights Variable
        w = tf.Variable(tf.ones([4434944+256*n_actions]), trainable=False)
        conv1 = tf.reshape(w[0:3072], [8, 8, 3, 16])
        conv2 = tf.reshape(w[3072:11264], [4, 4, 16, 32])
        dens1 = tf.reshape(w[11264:4434944], [17280, 256])
        dens2 = tf.reshape(w[4434944:4434944+256*n_actions], [256, n_actions])
        self.weights = w

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
        self.sess.run(tf.global_variables_initializer())

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

        Iterates through the seed list, generates a normal draw with the specified
        mutation strength, and adds it to the weight tensor. Then sets the weight
        tensor in the tf graph.

        Args:
            seeds (list of ints): The list of integer random seeds to use for
                random perturbation of the network weights.
            strength (float): The mutation strength or random scale.
        """
        size = [4434944 + 256*self.n_actions]
        w = np.zeros(size)

        for s in seeds:
            r = np.random.RandomState(s)
            w += r.normal(0, strength, size=size) # 50ns per float, slow :(

        self.sess.run(self.weights.assign(w))
