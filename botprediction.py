import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import scipy
import tensorflow as tf


# from statistics import mean, stdev
# %matplotlib inline
# %matplotlib notebook

class BotPrediction(object):

    def __init__(self):

        # Input Variable
        self.look_back = 300
        self.f_horizon = 5
        self.stride = 1    
        self.keep_prob_dropout_fc_1 = .1
        self.lowerSTDthreshold = 1e-10

        # Network hyperparamter
        self.learning_rate = 1*1e-5
        self.num_channels = 1

        # Network Design Parameter
        self.num_of_layer = 3
        self.num_of_filter_layer_1 = 16  # 16
        self.num_of_filter_layer_2 = 36  # 36
        self.num_of_filter_layer_3 = 32  # 72

        # Normalization
        self.norm_ways = 1 # 1: (x-mu)/std, 2: x-mu, 3: (x-min(x))/(max(x) - min(x))

        #################################### Neural Network Design


        self.x = tf.placeholder(tf.float32, shape=[None, self.look_back], name='x')
        self.x_tf = tf.reshape(self.x, [-1, self.look_back, self.num_channels])
        self.y_true = tf.placeholder(tf.float32, shape=[None, self.f_horizon], name='y_true')

        # In[8]:
        self.x_t = tf.slice(self.x, [ 0, self.look_back-1], [-1, 1])  ## t_th time data

        # In[9]:
        # Convolution layer 1
        net = tf.layers.conv1d(inputs=self.x_tf, name='layer_conv1', padding='same',
                               filters= self.num_of_filter_layer_1, kernel_size=5, activation=tf.nn.relu)
        layer_conv1 = net
        net = tf.layers.max_pooling1d(inputs=net, pool_size=2, strides=2)

        # In[10]:
        # Convolution layer 2
        if self.num_of_layer > 1:
            net = tf.layers.conv1d(inputs=net, name='layer_conv2', padding='same',
                                   filters=self.num_of_filter_layer_2, kernel_size=5, activation=tf.nn.relu)
            layer_conv2 = net
            net = tf.layers.max_pooling1d(inputs=net, pool_size=2, strides=2)
          
        # In[11]:
        # Convolution layer 3
        if self.num_of_layer > 2:
            net = tf.layers.conv1d(inputs=net, name='layer_conv3', padding='same',
                                   filters=self.num_of_filter_layer_3, kernel_size=5, activation=tf.nn.relu)
            layer_conv3 = net
            net = tf.layers.max_pooling1d(inputs=net, pool_size=2, strides=2)
         
        # In[12]:
        flat_layer = tf.contrib.layers.flatten(net)

        # In[13]:
        # Fully Connect
        fc_1 = tf.layers.dense(inputs=flat_layer, name='layer_fc1',
                              units=128, activation=tf.nn.relu)
        fc_1 = tf.layers.dropout(inputs=fc_1, rate = self.keep_prob_dropout_fc_1)
        self.y_predict = tf.layers.dense(inputs=fc_1, name='layer_fc2',
                              units=self.f_horizon, activation=None)

        # In[14]:
        # Trying Different Loss functions
        return_true = (self.y_true - self.x_t)
        return_true_percent = tf.abs(tf.divide(self.y_true - self.x_t, self.x_t))
        return_expected = (self.y_predict -  self.x_t)


        # In[23]:

        saver = tf.train.Saver()
        self.session = tf.Session()
        # self.session = session

        self.session.run(tf.global_variables_initializer())  # initialize with saved weights
        saver.restore(self.session, "Model_saved/FuturePred_280000")

        # session.close()

    def evaluateNNPrediction(self, prices):
        # session = tf.Session()
        norm_prices, param1, param2 = self.create_normalized_dataset(prices)

        # Check input data working
        # trailX = np.zeros([1,300])
        feed_dict = {self.x: norm_prices}
        norm_pred = self.session.run(self.y_predict, feed_dict=feed_dict)
        # session.close()

        return self.create_not_normalized_dataset(norm_pred, param1, param2)


    # Create Normalized Dataset
    def create_normalized_dataset(self,a1): 

        param1 = 0
        param2 = 0  
        a = a1  

        if self.norm_ways == 1: ## normalized by removing the mean and dividing by std
            param1 = np.mean(a1)
            param2 = np.std(a1)            
            if np.std(a1) > self.lowerSTDthreshold:
                a = (a1 - np.mean(a1))/np.std(a1)
                
            else:
                a = a1/np.mean(a1)
            
        elif self.norm_ways == 2: ## normalized by removing the mean
            a = (a1 - np.mean(a1))            
            
        elif self.norm_ways == 3:  ##### normalized data by min and max value

            param1 = np.min(a1)
            param2 = np.max(a1)

            if np.max(a1) - np.min(a1) > self.lowerSTDthreshold:
                a = (a1 - np.min(a1))/(np.max(a1) - np.min(a1))
               
            else:
                a = a1/np.mean(a1)               
            
            
        return a, param1, param2

    # Create Normalized Dataset
    def create_not_normalized_dataset(self,b1, param1, param2):  
        b = b1   

        if self.norm_ways == 1: ## normalized by removing the mean and dividing by std
                       
            if param2 > self.lowerSTDthreshold:
                b = b1*param2 + param1 #(a1 - np.mean(a1))/np.std(a1)
                
            else:
                b = b1*param1
            
        elif self.norm_ways == 2: ## normalized by removing the mean
            b = b1 + param1           
            
        elif self.norm_ways == 3:  ##### normalized data by min and max value           

            if param2 - param1 > self.lowerSTDthreshold:
                b = b1*(param2 - param1) + param1 # (a1 - np.min(a1))/(np.max(a1) - np.min(a1))
               
            else:
                b = b1*param1               
            
        return b

 











