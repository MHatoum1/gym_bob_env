# Introduction
Bowl of Balls environment for OpenAI Gym

## Game Rules:
Bowl of balls (BOB) is a game where we have a bowl with numbered balls (from 1 till 50).
* The player selects two balls at random (initial state) then calculates the difference between the balls.
* The goal is to have this difference between 5 and 15.
* The player has the right to return one of the two balls (min or max) and get a new one. He can do this up to 3 times.

##  Winning Conditions
The player with highest ball difference __wins__.
In case of __draw__ then the player with highest ball wins.

##  Prerequisites
OpenAI Gym is required. Please download [OpenAI Gym guide](https://github.com/openai/gym) by performing the below scripts
```
git clone https://github.com/openai/gym.git
cd gym
```

##  Installation

Copy the folder gym_bob to [gym/envs](<https://github.com/openai/gym/blob/master/gym/envs>) 

Edit [gym/envs/__ init __.py](<https://github.com/openai/gym/blob/master/gym/envs/__init__.py>) by adding the following:
```
register(
    id='BOB-v0',
    entry_point='gym.envs.gym_bob.gym_bob:BOBEnv'
)
```
Install gym using the following command
```
pip install -e .
```

##  Usage

To test the environment you can just do:

```
import gym
env = gym.make("BOB-v0")
env.reset()
```