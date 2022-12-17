import gym
from gym import spaces
import random
import numpy as np 

# Define the environment    
class BOBEnv(gym.Env):
    
    """
    A custom gym environment for the Bowl of Balls (BOB) game.
    
    In the BOB game, the player has a bowl with numbered balls (from 1 till 50).
    The player selects two balls at random (initial state) then calculates the difference between the balls.
    The goal is to have this difference between 5 and 15.
    The player has the right to return one of the two balls (min or max) and get a new one. He can do this up to 3 times.
    
    The player with the highest ball difference wins.
    In case of a draw, the player with the highest ball wins.
    
    The action space consists of 3 values:
        0 : Discard the min ball.
        1 : Discard the max ball.
        2 : Stand to end the player's turn.
        
    The observation of a 3-tuple of: the player's first ball, player's second ball, and the difference between the balls.
    """
    def __init__(self):
        # Initialize bowl with numbered balls from 1 to 50
        self.bowl = list(range(1, 51))

        # Initialize empty lists for player and dealer balls
        self.player_balls = []
        self.dealer_balls = []

        # Maximum number of replacement rounds
        self.max_player_rounds = 3
        # Current round
        self.current_round = 0
        # Whether the game is finished
        self.done = False

        # Define action space as a discrete space with 3 values
        self.action_space = spaces.Discrete(3)
        # Define observation space as a continuous box space with 3 values
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0]),
            high=np.array([50, 50, 50]),
            dtype=np.int
        )



    def reset(self):
        """
        Reset the environment to its initial state.
        
        Returns:
            The initial observation of the environment.
        """
        # Refill the bowl with numbered balls from 1 to 50
        self.bowl = list(range(1, 51))

        # Reset bowl
        random.shuffle(self.bowl)
        # Reset current round
        self.current_round = 0
        # Draw two balls for player
        self.player_balls = [self._draw_ball(), self._draw_ball()]
        # Draw two balls for dealer
        self.dealer_balls = [self._draw_ball(), self._draw_ball()]
        # Set game as not finished
        self.done = False
        return self._get_state()

    def step(self, action):
        """
        Take a step in the environment.
        
        Args:
            action (int): The action to take.
            
        Returns:
            observation (np.ndarray): The observation of the environment after the action.
            reward (float): The reward for taking the action.
            done (bool): Whether the game is finished.
            info (dict): Additional information about the environment.
        """
        
        # Check if action is valid
        if not self.action_space.contains(action):
            raise ValueError("Invalid action")

        # Stand to end player's turn
        if action == 2:
            self.current_round = self.max_player_rounds
        # Discard min ball and draw a new one
        elif action == 0:
            self._replace_ball(min(self.player_balls))
        # Discard max ball and draw a new one
        elif action == 1:
            self._replace_ball(max(self.player_balls))

        # Check if game is finished
        if self.current_round == self.max_player_rounds:
            self.done = True
            self._play_dealer()

        return self._get_state(), self._get_reward(), self.done, {}


    def _replace_ball(self, ball):
        """
        Replace the given ball with a new one from the bowl.
        """
        # Check if there are enough balls in the bowl
        if not self.bowl:
            raise ValueError("Not enough balls in the bowl")

        # Add ball back to the bowl
        self.bowl.append(ball)
        # Remove ball from player's hand
        self.player_balls.remove(ball)
        # Draw a new ball
        new_ball = random.choice(self.bowl)
        # Add new ball to player's hand
        self.player_balls.append(new_ball)
        # Remove new ball from the bowl
        self.bowl.remove(new_ball)
        # Increment current round
        self.current_round += 1


    def _replace_dealer__ball(self, ball):
        """
        Replace the given ball with a new one from the bowl.
        """
        # Check if there are enough balls in the bowl
        if not self.bowl:
            raise ValueError("Not enough balls in the bowl")

        # Add ball back to the bowl
        self.bowl.append(ball)
        # Remove ball from player's hand
        self.dealer_balls.remove(ball)
        # Draw a new ball
        new_ball = random.choice(self.bowl)
        # Add new ball to player's hand
        self.dealer_balls.append(new_ball)
        # Remove new ball from the bowl
        self.bowl.remove(new_ball)
        # Increment current round
        self.current_round += 1

    def _play_dealer(self):
        """
        Dealer's Algorithm:
        If the difference between the balls isn't between 5 and 15, then replace the max ball.
        If it is greater than 25, then replace the max ball.
        Otherwise, replace the min ball.
        """
        self.current_round = 0

        while self.current_round < self.max_player_rounds:
            difference = self._score_hand(self.dealer_balls)
            if difference > 15 or difference < 5:
                ball = max(self.dealer_balls)
                if max(self.dealer_balls) > 25:
                    ball = max(self.dealer_balls)
                else:
                    ball = min(self.dealer_balls)

                self._replace_dealer__ball(ball)
            else:
                self.current_round = self.max_player_rounds
              
    def _get_state(self):
        """
        Return the current state of the environment as a tuple of:
        player's first ball, player's second ball, and the difference between the balls.
        """
        player_balls = sorted(self.player_balls)
        return player_balls[0], player_balls[1], abs(player_balls[0] - player_balls[1])


    def _display_data(self):
        return {
            'round': self.current_round,
            'player_balls': sorted(self.player_balls),
            'player_score': self._score_hand(self.player_balls),
            'dealer_balls': sorted(self.dealer_balls),
            'dealer_score': self._score_hand(self.dealer_balls),
            
        }


    def _draw_ball(self):
        """
        Draw a random ball from the bowl.
        """
        # Check if there are enough balls in the bowl
        if not self.bowl:
            raise ValueError("Not enough balls in the bowl")

        # Draw a random ball from the bowl
        ball = random.choice(self.bowl)
        # Remove ball from the bowl
        self.bowl.remove(ball)
        return ball




    def _score_hand(self, balls):
        """
        Calculate the difference between the given balls.
        """
        # Sort balls in ascending order
        sorted_balls = sorted(balls)
        # Calculate difference between balls
        return abs(sorted_balls[0] - sorted_balls[1])

    

    def _get_reward(self):
        """
        Calculate the reward for the player based on the difference between the player's balls and the dealer's balls.
        """
        # Calculate difference between player's balls
        player_difference = self._score_hand(self.player_balls)
        # Calculate difference between dealer's balls
        dealer_difference = self._score_hand(self.dealer_balls)

        # Player loses if their difference is less than 5 and or greated than 15
        if player_difference<5 or player_difference > 15:
            return -1
        # Player wins if the dealer's difference is less than 5 and or greated than 15
        elif dealer_difference<5 or dealer_difference > 15:
            return 1
        # Player wins if their difference is greater than dealer's difference
        elif player_difference > dealer_difference:
            return 1
        # Player loses if their difference is less than dealer's difference
        elif player_difference < dealer_difference:
            return -1
        # In case both has the same difference
        elif dealer_difference == player_difference:
            # The player with higher max wins
            if (max(self.player_balls) > max(self.dealer_balls)):
                return  1 
            else:
                return -1 
        # Draw if both differences are the same
        else:
            return 0