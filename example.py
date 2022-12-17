from BOBEnv import BOBEnv

def play_BOB():
    env = BOBEnv()
    
    # Reset the environment and get the initial state
    state = env.reset()
    print("Initial state: ", state)
    print("Game: ", env._display_data())
    
    while True:
        # Take an action and get the next state, reward, and done status
        action = input("Enter action (discard_max (0), discard_min (1), or stand(2)): ")
        state, reward, done, _ = env.step(int(action))
        print("Current state: ", state)
        print("Game: ", env._display_data())
        
        
        if done:
            break
    
    # Print the final reward
    print("Final reward: ", reward)

# Play the game
play_BOB()
