from urnai.utils.error import DifferentModelSizeError
from .abneuralnetwork import ABNeuralNetwork
import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.compat.v1 import Session,ConfigProto,placeholder,layers,train,global_variables_initializer
import os

class TensorflowDeepNeuralNetwork(ABNeuralNetwork):
    """
    Implementation of a Generic Deep Neural Network using Tensorflow

    This class inherits from ABNeuralNetwork, so it already has all abstract methods
    necessary for learning, predicting outputs, and building a model. All that this
    class does is implement those abstract methods, and implement the methods necessary
    for adding Neural Network layers, such as add_input_layer(), add_output_layer(),
    add_fully_connected_layer(), add_convolutional_layer() etc.

    This class also implements the methods necessary for saving and loading the model
    from local memory.

    Parameters:
        action_output_size: int
            size of our output
        state_input_shape: tuple
            shape of our input
        build_model: Python dict
            A dict representing the NN's layers. Can be generated by the 
            ModelBuilder.get_model_layout() method from an instantiated ModelBuilder object.
        gamma: Float
            Gamma parameter for the Deep Q Learning algorithm
        alpha: Float
            This is the Learning Rate of the model
        seed: Integer (default None)
            Value to assing to random number generators in Python and our ML libraries to try 
            and create reproducible experiments
        batch_size: Integer
            Size of our learning batch to be passed to the Machine Learning library
    """

    def __init__(self, action_output_size, state_input_shape, build_model, gamma, alpha, seed = None, batch_size=32):     
        self.sess = None
        super().__init__(action_output_size, state_input_shape, build_model, gamma, alpha, seed, batch_size)
        #Setup output qsa layer and loss
        self.tf_qsa = placeholder(shape=[None, self.action_size], dtype=tf.float32)
        self.loss = tf.losses.mean_squared_error(self.tf_qsa, self.model[-1])
        self.optimizer = train.AdamOptimizer(self.learning_rate).minimize(self.loss)
        
        self.sess.run(global_variables_initializer())
        self.saver = train.Saver()

    def add_input_layer(self, idx):
        layer_model = self.build_model[idx]
        self.model.append(
                placeholder(dtype=tf.float32,
                shape=layer_model['shape'], name='inputs_')
                )

    def add_output_layer(self, idx):
        self.model.append(
                layers.dense(inputs=self.model[-1], 
                units=self.action_size,activation=None)
                )

    def add_fully_connected_layer(self, idx):
        layer_model = self.build_model[idx]
        self.model.append(
                layers.dense(inputs=self.model[-1], 
                units=layer_model['nodes'], 
                activation=tf.nn.relu, name=layer_model['name'])
                )

    def update(self, state, target_output):
        self.sess.run(self.optimizer, feed_dict={self.model[0] : state, self.tf_qsa: target_output})

    def get_output(self, state):
        return self.sess.run(self.model[-1], feed_dict={self.model[0]: state})

    def create_base_model(self):
        ops.reset_default_graph()
        tf.compat.v1.disable_eager_execution()
        self.sess = Session(config=ConfigProto(allow_soft_placement=True))

        model = []
        return model

    def save_extra(self, persist_path):
        self.saver.save(self.sess, self.get_full_persistance_tensorflow_path(persist_path))

    def load_extra(self, persist_path):
        #Makes model, needed to be done before loading tensorflow's persistance
        self.make_model()
        #Check if tf file exists
        exists = os.path.isfile(self.get_full_persistance_tensorflow_path(persist_path) + ".meta")
        #If yes, load it
        if exists:
            self.saver.restore(self.sess, self.get_full_persistance_tensorflow_path(persist_path))
            #is this needed?
            self.set_seeds()
    
    def copy_model_weights(self, model_to_copy):
        #need to test
        if len(model_to_copy) == len(self.model):
            for i in range(len(model_to_copy)):
                self.model[i].set_weights(model_to_copy[i].get_weights())
        else:
            raise DifferentModelSizeError("Model to copy has a different number of layers compared to target model.")

    def set_seed(self, seed) -> None:  
        if seed != None:
            tf.random.set_seed(seed)
        return seed
