"""Policy Network class"""

import numpy as np
import tensorflow as tf


ATARI_DIMS = [210, 160, 3]


class Policy:
    """Atari policy network."""

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

    def forward(self, state):
        """Computes a forward pass through the policy graph, returns an action.

        Args:
            state (np.ndarray): The [210, 160, 3] Atari game state.

        Returns:
            action: The chosen integer action.
        """
        with tf.Session() as sess:
            a = sess.run(self.action, feed_dict={self.input: np.expand_dims(state, 0)})

        action = a[0][0]
        return action

    def set_weights(self, seeds, strength):
        """Sets the graph weights given a sequence of random seeds to do so.

        Args:
            seeds (list of ints): The list of integer random seeds to use for
                random perturbation of the network weights.
            strength (float): The mutation strength or random scale.
        """
        size = [4434944 + 256*self.n_actions]
        w = np.zeros(size)

        for s in seeds:
            np.random.seed(s)
            w += np.random.normal(0, strength, size=size)

        with tf.Session() as sess:
            sess.run(self.weights.assign(w))
