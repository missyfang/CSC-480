import gym

living_cost = 0
discount_rate = 1.0
current_iteration_v_star_per_state = []
last_iteration_v_star_per_state = []

# Q*(s, a) = Σ T(s, a, s') · [ R(s, a, s') + γ · V*(s') ]
#      * p  = the probability of transitioning into the next state
#      * s' = the index of the next state,
#      * r  =  reward,
#      * T  = is terminal, True/False (done=True if the next state is a Hole or the Goal).
def compute_q_star(action):
    q = []
    for possible_transition in action:
        prob = possible_transition[0]
        reward = possible_transition[2]
        v_star_of_next_state = last_iteration_v_star_per_state[possible_transition[1]]
        action_q = prob *(reward + discount_rate * v_star_of_next_state)
        q.append(action_q)

    q_star = sum(q)
    return q_star

def compute_v_star(P, index):
    # for each action you can take compute the q*
    q_stars_for_actions = []
    for action in P:
        q_star = compute_q_star(action)
        q_stars_for_actions.append(q_star)

    current_iteration_v_star_per_state[index] = q_stars_for_actions

    return max(q_stars_for_actions)

def compute_value_of_state():
    pass

def run(frozen_lake):
    for p in frozen_lake.P:
        compute_q_star(p)
    pass


def create_state():
    env = gym.make('FrozenLake-v1', desc=None, map_name="8x8", is_slippery=True, render_mode="ansi")
    frozen_lake = env.env.env.env

    # initalize with 0s everywhere, expcept reward and hole state they have value at start
    current_iteration_v_star_per_state = [0] * env.observation_space.n
    last_iteration_v_star_per_state = [0] * env.observation_space.n

    return  frozen_lake
