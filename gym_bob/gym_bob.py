import gym
from gym import spaces
from gym.utils import seeding

# Store all numbers between 1 and 50 in a list
bowl = list(range(1, 51))


# Get a ball from the bowl 
def draw_ball(np_random):
    ball = int(np_random.choice(bowl))
    bowl.remove(ball)
    return ball

# Draw a hand
def draw_hand(np_random):
    return [draw_ball(np_random), draw_ball(np_random)]

# Put a ball back in the bowl
def put_back(ball):
    bowl.append(ball)



# Check if the hand is a valid hand
def check_hand(hand):
    if len(hand) != 2:
        return False
    return True

# score a hand
def score_hand(hand):
    return abs(hand[0] - hand[1])




# Define the environment    
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
        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


    def step(self, action):
        assert self.action_space.contains(action)
        reward = 0
        done = False
        if action == 0: # action = min
            min_ball=min(self.player)
            put_back(min_ball)
            self.player.remove(min_ball)
            self.player.append(draw_ball(self.np_random))
        elif action == 1: #action = max
            max_ball=max(self.player)
            put_back(max_ball)
            self.player.remove(max_ball)
            self.player.append(draw_ball(self.np_random))
        else:  
            done = True
            """
            Dealer's Algorithm
            If the difference isn't between 5 and 15 then the max. If it is greater than 25 then replace the max
            else replace the min ball

            """
            print("Dealer's turn")
            iteration = 0
            stop = False 
            while( iteration < 3 and stop == False ):
                print("Iteration: ", iteration)
                print("Dealer's hand: ", self.dealer)
                if (score_hand(self.dealer) > 15 or score_hand(self.dealer) < 5):
                    if max(self.dealer) > 25:
                        min_ball=min(self.dealer)
                        put_back(min_ball)
                        self.dealer.remove(min_ball)
                        self.dealer.append(draw_ball(self.np_random))
                        print("Dealer's min ball replaced")
                    else:
                        max_ball=max(self.dealer)
                        put_back(max_ball)
                        self.dealer.remove(max_ball)
                        self.dealer.append(draw_ball(self.np_random))
                        print("Dealer's max ball replaced")
                else:
                    stop=True
                iteration+=1
         
            reward = self.calculate_reward()
           
        return self._get_obs(), reward, done, {}
    


    def _get_obs(self):
        return (min(self.player), max(self.player),score_hand(self.player))


    

    def calculate_reward(self):
        reward = 0
        if (score_hand(self.dealer) > 15 or score_hand(self.dealer) < 5):
            reward = 1 
        elif (score_hand(self.player) > 15 or score_hand(self.player) < 5):
            reward = -1 
        elif(score_hand(self.player) > score_hand(self.dealer)):
            reward = 1 
        elif (score_hand(self.player)== score_hand(self.dealer)):
            if (max(self.player) > max(self.dealer)):
                reward = 1 
            else:
                reward = -1 
        return reward


    # Reset the game
    def reset(self):
        self.player = draw_hand(self.np_random)
        self.dealer = draw_hand(self.np_random)
        return self._get_obs()

