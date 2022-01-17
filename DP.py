import itertools
import random
import numpy as np

class DP_Solver(object):

    def __init__(self, horizon):
        # Inputs
        self.num_states = 2
        self.horizon = horizon
        # self.TC = .0025
        # s0 = 0
        self.disFactor = 1
        # self.prices = [5, 5.2, 5.4, 5,5.1,5.6]  # horizon+1, 5 is today's price

    # Function for Dynamic Programming
    def stTran(self,s_t,a_t):
        if s_t == 0:
            s_t1 = a_t
        elif s_t == 1:
            s_t1 = a_t + 1
        return s_t1
               
       
    def stTranInv(self,s_t,s_t1):
        if s_t == 0:
            a_t = s_t1
        elif s_t == 1:
            a_t = s_t1 - 1
        return a_t

    def hFun(self,s_t,a_t):  # for Transaction cost
        if s_t == 0:
            s_t1 = a_t
        elif s_t == 1:
            s_t1 = -a_t
        return s_t1

    def reward(self,s_t,a_t, price_t, price_t1, TC):  # for Transaction cost
        r_t = (price_t1-price_t) * self.stTran(s_t,a_t) - price_t*self.hFun(s_t,a_t)*TC
        return r_t

# All Tree
    def allTree(self):
        possTree = np.zeros([self.num_states**self.horizon,self.horizon])
        counter = 0
        for i in itertools.product(range(self.num_states), repeat = self.horizon):   
            possTree[counter] = np.array(i)
            counter = counter + 1
        return possTree
    

    def evaluateDP(self,s0, prices, TC):

        possTree = self.allTree()
        TotReward = np.zeros(len(possTree))
        # print(TotReward)

        for i in range(len(possTree)):
        #     print('possTree ')
        #     if i == 7:
        #         print('possTree ', possTree[i,0])
            a0 = self.stTranInv(s0, possTree[i,0])
            r0 = self.reward(s0, a0, prices[0], prices[1], TC) 
        #     if i == 7:
        #         print('a0 ', a0)
        #         print('r0 ',r0)
            TotReward[i] = TotReward[i] + r0
           
            for t in range(1,self.horizon): 
        #         if i == 7:
                # print('t ' , t)
        #             print('posstree ', possTree[i,t-1], possTree[i,t])
        #             print('price ', prices[t], prices[t+1])
                at = self.stTranInv(possTree[i,t-1], possTree[i,t])
                rt = self.reward(possTree[i,t-1], at, prices[t], prices[t+1], TC)
               
        #         if i == 7:
        #             print('at rt ', at, rt)
                TotReward[i] = TotReward[i] + rt
               
        # print(TotReward)
        best_soln = np.argmax(TotReward)

        return possTree[best_soln][0]