import gymnasium as gym
import numpy as np

from tutorial import display_policy, run_one_experiment

living_cost = 0
discount_rate = 1.0
current_iteration_v_star_per_state = []
last_iteration_v_star_per_state = []
optimal_policy = []
num_iterations = 100

# Q*(s, a) = Σ T(s, a, s') · [ R(s, a, s') + γ · V*(s') ]
#      * p  = the probability of transitioning into the next state
#      * s' = the index of the next state,
#      * r  =  reward,
#      * T  = is terminal, True/False (done=True if the next state is a Hole or the Goal).
def compute_q_star(action):
    q = []
    for possible_transition in action:
        # the probability of transitioning into the next state
        prob = possible_transition[0]

        # r = reward
        reward = possible_transition[2]

        # s' = the index of the next state, used to compute v*
        next_state = possible_transition[1]
        v_star_of_next_state = last_iteration_v_star_per_state[next_state]

        # * T  = is terminal, True/False (done=True if the next state is a Hole or the Goal).
        is_terminal = possible_transition[3]

        # if it is terminal, no next reward
        if is_terminal:
            v_star_of_next_state = 0

        action_q = prob *(reward + discount_rate * v_star_of_next_state)
        q.append(action_q)


    q_star = sum(q)
    return q_star

def compute_v_star(P, index):
    # for each action you can take compute the q*
    q_stars_for_actions = []
    for action in P.values():
        q_star = compute_q_star(action)
        q_stars_for_actions.append(q_star)

    # store v* for state
    current_iteration_v_star_per_state[index] = max(q_stars_for_actions)

    # save action that lead to max
    optimal_policy[index] = q_stars_for_actions.index(max(q_stars_for_actions))

    return max(q_stars_for_actions)


def run_for_state(env, iteration_count):
    global last_iteration_v_star_per_state
    num_states = env.observation_space.n
    frozen_lake = env.env.env.env
    # compute v*
    for s in range(num_states):
        curr = frozen_lake.P[s]
        compute_v_star(curr, s)

    # update last runs v* values to the ones just computed
    last_iteration_v_star_per_state = current_iteration_v_star_per_state[:]

    # run x times
    if iteration_count > num_iterations:
        return optimal_policy


    return run_for_state(env, iteration_count + 1)

# run policy once
def run_found_policy(env, policy, nS):
    # display policy
    print("\n")
    print("optimal policy")
    print(display_policy(np.array(policy), nS))
    # Running one experiment ...
    print("\nRunning one experiment with this random policy (5 runs with display)")
    num_episodes = 5
    display = True
    goals, holes, total_rewards, total_goal_steps = run_one_experiment(env, policy, num_episodes, display)

    print("\nRunning one experiment with this random policy (1000 runs without display)")
    num_episodes = 1000
    display = False
    goals, holes, total_rewards, total_goal_steps = run_one_experiment(env, policy, num_episodes, display)

    percent_goal = goals / num_episodes
    percent_hole = holes / num_episodes
    mean_reward = total_rewards / num_episodes
    mean_goal_steps = 0.0 if (goals == 0) else (total_goal_steps / goals)

    print("\n*** FOUND POLICY RESULTS ***:")
    print(f"\tGoals: {goals:>5d}/{num_episodes} = {percent_goal:>7.3%}")
    print(f"\tHoles: {holes:>5d}/{num_episodes} = {percent_hole:>7.3%}")
    print(f"\tmean reward:          {mean_reward:.5f}")
    print(f"\tmean goal steps:     {mean_goal_steps:.2f}")


# run policy 1000 times and compute stats
def run_policy(policy, env):
    goals = []
    steps = []
    num_episodes = 10000
    for _ in range(100):
        goal, holes, total_rewards, total_goal_steps = run_one_experiment(env, policy, num_episodes)
        goals.append(goal)
        steps.append(total_goal_steps)

    mean_goals = np.mean(goals)
    mean_steps = np.mean(steps)
    std_dev_goals = np.std(goals)

    print("\n*** RESULTS FOR 100 RUNS***:")
    print(f"\tMean Goals: {mean_goals}")
    print(f"\tMean Steps: {mean_steps}")
    print(f"\tstd dev Goals: {std_dev_goals}")


def run_value_iteration(env):
    #assign global vars
    global current_iteration_v_star_per_state, last_iteration_v_star_per_state, optimal_policy
    # initalize with 0s everywhere
    num_s = env.observation_space.n
    current_iteration_v_star_per_state = [0] * num_s
    last_iteration_v_star_per_state = [0] * num_s
    optimal_policy = [0] * num_s

    # run alg
    run_for_state(env, 0)

    # after optimal policy found, run it and print stats
    # run_found_policy(env, optimal_policy, num_s)
    run_policy(optimal_policy, env)
    return optimal_policy