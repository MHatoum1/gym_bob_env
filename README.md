# Introduction
The BOBEnv is a custom gym environment for the Bowl of Balls (BOB) game.

## Game Rules:
In the [BOB game](https://medium.datadriveninvestor.com/bowl-of-balls-bob-new-openai-gym-environment-fa4af856f58c), the player has a bowl with numbered balls (from 1 till 50). The player selects two balls at random (initial state) then calculates the difference between the balls. The goal is to have this difference between 5 and 15. The player has the right to return one of the two balls (min or max) and get a new one. He can do this up to 3 times.

The player with the highest ball difference wins. In case of a draw, the player with the highest ball wins.

##  Winning Conditions
The player with the highest ball difference between 5 and 15 wins. In case of a draw, the player with the highest ball wins.

##  Prerequisites
* Python 3.6 or higher
* gym
* numpy

##  Installation as a gym environment

To install BOBEnv as a gym environment, follow these steps:

1. Clone this repository or download the BOBEnv.py file.
2. In your gym project, import the BOBEnv module: __from BOBEnv import BOBEnv__
3. To create an instance of the environment, use __env = BOBEnv()__

##  Usage

To use BOBEnv as a gym environment, follow these steps:

1. Create an instance of the environment: __env = BOBEnv()__
2. Reset the environment to its initial state: __observation = env.reset()__
3. Take an action in the environment: __observation, reward, done, info = env.step(action)__
4. Repeat steps 2 and 3 until the game is finished (__done__ is __True__).