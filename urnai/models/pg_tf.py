import tensorflow as tf
import numpy as np
import random
import os
from .base.abmodel import LearningModel
from agents.actions.base.abwrapper import ActionWrapper
from agents.states.abstate import StateBuilder


class PolicyGradientTF(LearningModel):
    def __init__(self, action_wrapper: ActionWrapper, state_builder: StateBuilder, save_path, learning_rate=0.01, gamma=0.95, name='PolicyGradient'):
        super(PolicyGradientTF, self).__init__(action_wrapper, state_builder, gamma, learning_rate, save_path, name)

        # Initializing variables for the model's state, which must be reset every episode
        self.episode_states, self.episode_actions, self.episode_rewards = [], [], []  # Records all states, actions and rewards for an episode
        
        tf.reset_default_graph()

        # Initializing TensorFlow session
        self.sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))

        self.inputs_ = tf.placeholder(dtype=tf.float32, shape=[None, self.state_size], name='inputs_')

        # Placeholder used to output the probability distribution for the actions
        self.actions_ = tf.placeholder(dtype=tf.float32, shape=[None, self.action_size], name='actions_')
        self.discounted_episode_rewards_ = tf.placeholder(tf.float32, [None, ], name='discounted_episode_rewards')

        # Defining the layers of the neural network
        self.fc1 = tf.contrib.layers.fully_connected(inputs=self.inputs_,
                                                    num_outputs = 10,
                                                    activation_fn = tf.nn.relu,
                                                    weights_initializer = tf.contrib.layers.xavier_initializer())

        self.fc1_1 = tf.contrib.layers.fully_connected(inputs=self.fc1,
                                                    num_outputs = 10,
                                                    activation_fn = tf.nn.relu,
                                                    weights_initializer = tf.contrib.layers.xavier_initializer())

        self.fc2 = tf.contrib.layers.fully_connected(inputs=self.fc1_1,
                                                    num_outputs = self.action_size,
                                                    activation_fn = tf.nn.relu,
                                                    weights_initializer = tf.contrib.layers.xavier_initializer())

        self.fc3 = tf.contrib.layers.fully_connected(inputs=self.fc2,
                                                        num_outputs = self.action_size,
                                                        activation_fn = None,
                                                        weights_initializer = tf.contrib.layers.xavier_initializer())

        self.output_layer = tf.nn.softmax(self.fc3)


        self.neg_log_prob = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.fc3, labels=self.actions_)
        self.loss = tf.reduce_mean(self.neg_log_prob * self.discounted_episode_rewards_)
        self.optimizer = tf.train.AdamOptimizer(self.learning_rate).minimize(self.loss)

        self.sess.run(tf.global_variables_initializer())

        self.saver = tf.train.Saver()
        self.load()


    def learn(self, s, a, r, s_, done, is_last_step: bool):
        self.episode_states.append(s)
        # For actions, we'll record a one-hot vector correspondent to the chosen action
        action_ = np.zeros(self.action_size)
        action_[a] = 1
        self.episode_actions.append(action_)
        self.episode_rewards.append(r)

        if done or is_last_step:
            discounted_episode_rewards = self.__discount_and_normalize_rewards(self.episode_rewards)

            # Calculating the loss and training our parameters using the current episode's outputs,
            # that is, feedforward, gradient and backpropagation steps.
            loss_, _ = self.sess.run([self.loss, self.optimizer],
                                        feed_dict={self.inputs_: np.vstack(np.array(self.episode_states)),
                                                    self.actions_: np.vstack(np.array(self.episode_actions)),
                                                    self.discounted_episode_rewards_: discounted_episode_rewards})

            # Resetting the stores before beginning a new episode
            self.episode_states, self.episode_actions, self.episode_rewards = [], [], []


    def __discount_and_normalize_rewards(self, episode_rewards):
        discounted_episode_rewards = np.asarray(np.zeros_like(self.episode_rewards))  # Empty numpy array with the same size of our rewards
        cumulative = 0.0
        
        # We're taking the sum of all rewards discounted by gamma, in reversed order.
        for i in reversed(range(len(self.episode_rewards))):
            cumulative = cumulative * self.gamma + self.episode_rewards[i]
            discounted_episode_rewards[i] = cumulative
        
        # Normalizes the rewards by subtracting them to their mean and dividing the result by the standard deviation.
        mean = np.mean(discounted_episode_rewards)
        std = np.std(discounted_episode_rewards)

        if std == 0:
            std = 1

        discounted_episode_rewards = (discounted_episode_rewards - mean) / (std)
        
        return discounted_episode_rewards


    def choose_action(self, state, excluded_actions=[]):
        action_probability_distribution = self.sess.run(self.output_layer,
                                                        feed_dict={self.inputs_: state})

        action = np.random.choice(range(action_probability_distribution.shape[1]), p=action_probability_distribution.ravel())
        
        return action
        

    def predict(self, state):
        q_values = self.sess.run(self.output_layer, feed_dict={self.inputs_: state})
        action_idx = np.argmax(q_values)
        action = self.actions[int(action_idx)]
        return action

    def save(self):
        print()
        print("> Saving the model!")
        print()
        self.saver.save(self.sess, self.save_path)

    def load(self):
        exists = os.path.isfile(self.save_path + '.meta')
        if exists:
            print()
            print("> Loading saved model!")
            print()
            self.saver.restore(self.sess, self.save_path)
