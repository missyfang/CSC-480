import multiprocessing
import sys
import math

from tutorial import generate_random_policy, run_one_experiment

# NOTE THAT THESE TRY EXCEPTS ARE ONLY ADDED SO THAT YOU KNOW
# THAT YOU MUST INSTALL THESE LIBRARIES IF YOU DON'T ALREADY HAVE THEM

try:
    import gymnasium as gym
except:
    print("The gymnasium library is not installed!")
    print("Please install gymnasium in your python environment using:")
    print("\tpip install gymnasium")
    sys.exit(1)

try:
    import numpy as np
except:
    print("The numpy library is not installed!")
    print("Please install numpy in your python environment using:")
    print("\tpip install numpy")
    sys.exit(1)




def part_one():
# TODO check creating env right
    # Create a FrozenLake 8x8 environment using Gymnasium
    env = gym.make('FrozenLake-v1', desc=None, map_name="8x8", is_slippery=True, render_mode="ansi")

    number_states = env.observation_space.n
    number_actions =  env.action_space.n

    #create 10 random policies
    policies = []
    for i in range(10):
        policy = generate_random_policy(number_actions, number_states, seed=i)
        policies.append((f"policy_{i}", policy))

    print("10 polices created")

    # run policies in parallel
    with multiprocessing.Pool() as pool:
        results = pool.map(run_policy, [(env, name, policy) for name, policy in policies])

    print(results)

    pass

def run_policy(arg):
    env, name, policy = arg
    num_episodes = 10000

    goals, holes, total_rewards, total_goal_steps = run_one_experiment(env, policy, num_episodes)

    percent_goal = goals / num_episodes
    percent_hole = holes / num_episodes
    mean_reward = total_rewards / num_episodes
    mean_goal_steps = 0.0 if (goals == 0) else (total_goal_steps / goals)

    print("\n*** RESULTS ***:")
    print(f"\tGoals: {goals:>5d}/{num_episodes} = {percent_goal:>7.3%}")
    print(f"\tHoles: {holes:>5d}/{num_episodes} = {percent_hole:>7.3%}")
    print(f"\tmean reward:          {mean_reward:.5f}")
    print(f"\tmean goal steps:     {mean_goal_steps:.2f}")
    return name, goals, holes, total_rewards, total_goal_steps


def part_two():
    # TODO: your code here ...
    pass


def main():
    # TODO: feel free to change this as required
    # TODO: also, check tutorial.py for some hints on how to implement your experiments
    part_one()
    part_two()


if __name__ == "__main__":
    main()

