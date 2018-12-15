import gym
from gym import spaces
import random
import numpy as np

class BOBEnv(gym.Env):
    
    """
    Bowl of balls (BOB) is a game where we have a bowl with numbered balls (from 1 till 50).
    The player selects two balls at random (initial state) then calculates the difference between the balls.
    The goal is to have this difference between 5 and 15.
    The player has the right to return one of the two balls (min or max) and get a new one. He can do this up to 3 times.
    
    The player with highest ball difference wins
    In case of draw then the player with highest ball wins.
    
    Action space consists of 3 values:
        0 : Discard min ball
        1 : Discard max ball
        2 : Stand to end player's turn
    The observation of a 3-tuple of: the player's first ball,player's second and the difference between the balls 
    """
    def __init__(self):
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Tuple((
            spaces.Discrete(50),
            spaces.Discrete(50),
            spaces.Discrete(49)
            ))
        

        # Start the first game
        self.reset()


    def step(self, action):
        assert self.action_space.contains(action)
        reward = 0
        done = False
        if action == 0: # action = min
            min_ball=min(self.player)
            self.put_ball(min_ball)
            self.player.remove(min_ball)
            self.player.append(self.draw_ball())
        elif action == 1: #action = max
            max_ball=max(self.player)
            self.put_ball(max_ball)
            self.player.remove(max_ball)
            self.player.append(self.draw_ball())
        else:  
            done = True
            """
            Dealer's Algorithm
            If the difference isn't between 5 and 15 then the max. If it is greater than 25 then replace the max
            else replace the min ball

            """
            iteration = 0
            stop = False 
            while( iteration < 3 and stop == False ):
                if (self.hand_diff(self.dealer) > 15 or self.hand_diff(self.dealer) < 5):
                    if max(self.dealer) > 25:
                        min_ball=min(self.dealer)
                        self.put_ball(min_ball)
                        self.dealer.remove(min_ball)
                        self.dealer.append(self.draw_ball())
                    else:
                        max_ball=max(self.dealer)
                        self.put_ball(max_ball)
                        self.dealer.remove(max_ball)
                        self.dealer.append(self.draw_ball())
                else:
                    stop=True
                iteration+=1
         
            reward = self.calculate_reward()
           
        return self._get_obs(), reward, done, {}
    


    def _get_obs(self):
        return (min(self.player), max(self.player),self.hand_diff(self.player))

    def draw_ball(self):
        random.shuffle(self.bowl)
        return int(self.bowl.pop())
    

    def calculate_reward(self):
        reward = 0
        if (self.hand_diff(self.dealer) > 15 or self.hand_diff(self.dealer) < 5):
            reward = -1 
        elif (self.hand_diff(self.player) > 15 or self.hand_diff(self.player) < 5):
            reward = 1 
        elif(self.hand_diff(self.player) > self.hand_diff(self.dealer)):
            reward = 1 
        elif (self.hand_diff(self.player)== self.hand_diff(self.dealer)):
            if (max(self.player) > max(self.dealer)):
                reward = 1 
            else:
                reward = -1 
        return reward

    def rand(self,start, end):
        answer=list(range(start,end))
        random.shuffle(answer)  
        return answer

    def put_ball(self,ball):
        self.bowl.append(ball)


    def draw_hand(self):
        return [self.draw_ball(), self.draw_ball()]

    def reset(self):
        self.bowl = self.rand(1,50)
        self.dealer = self.draw_hand()
        self.player = self.draw_hand()
        return self._get_obs()

    # Added to allow developers to use while building agents  
    def hash(self):
        return hash(max(self.player)+min(self.player))
    
    def hand_diff(self,hand):
        return max(hand)-min(hand)
