import multiprocessing
import sys


from tutorial import generate_random_policy, run_one_experiment, display_policy

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

    # create 10 random policies
    policies = []
    for i in range(10):
        policy = generate_random_policy(number_actions, number_states, seed=i)
        policies.append((f"policy_{i}", policy))

    print("10 polices created")

    # run all policies in parallel
    with multiprocessing.Pool() as pool:
        policy_results= pool.map(run_policy_100, [(env, name, policy) for name, policy in policies])


    max_mean_goals = policy_results[0]
    for r in policy_results[1:]:
        if r[1] > max_mean_goals[1]:
            max_mean_goals = r

    policy_results.remove(max_mean_goals)

    second_max_mean_goals = policy_results[0]
    for r in policy_results[1:]:
        if r[1] > second_max_mean_goals[1]:
            second_max_mean_goals = r


    print(f"Lowest: {max_mean_goals[0]} — mean goals : {max_mean_goals[1]}, mean steps : {max_mean_goals[2]}, goal std dev : {max_mean_goals[3]}")
    print(f"2nd Lowest: {second_max_mean_goals[0]} — mean goals : {second_max_mean_goals[1]}, mean steps : {second_max_mean_goals[2]}, goal std dev : {second_max_mean_goals[3]}")


pass


# run a policy 100 times in parallel and get info
def run_policy_100(args):
    env, name, policy = args
    all_results = []
    for _ in range(100):
        r = run_policy(env, policy)
        all_results.append(r)

    goals = []
    steps = []

    for res in all_results:
        goals.append(res[0])
        steps.append(res[1])

    mean_goals = np.mean(goals)
    mean_steps = np.mean(steps)
    std_dev_goals = np.std(goals)

    print("\n*** RESULTS ***:")
    print(f"\tName: {name}")
    print(f"\tMean Goals: {mean_goals}")
    print(f"\tMean Steps: {mean_steps}")
    print(f"\tstd dev Goals: {std_dev_goals}")
    print(display_policy(policy, env.observation_space.n))
    return name, mean_goals, mean_steps, std_dev_goals



# run a single policy 10_000 times
def run_policy(env, policy):
    num_episodes = 10_000

    goals, holes, total_rewards, total_goal_steps = run_one_experiment(env, policy, num_episodes)


    return goals, total_goal_steps



def part_two():
    env = gym.make('FrozenLake-v1', desc=None, map_name="8x8", is_slippery=True, render_mode="ansi")
    from value_iteration import run_value_iteration
    run_value_iteration(env)
    pass


def main():
   # part_one()
    part_two()




if __name__ == "__main__":
    main()

