import gym
import numpy as np
import matplotlib.pyplot as plt

env = gym.make("MountainCar-v0")
#env.reset()
#env = env.unwrapped

#print(env.observation_space.high)#[0.6, 0.07]
#print(env.observation_space.low) #[-1.2, -0.07]
#print(env.action_space.n)#3

LEARNING_RATE = 0.1
DISCOUNT = 0.95#future reward vs current reward
EPISODES = 2000
SHOW_EVERY = 500



#create Q table with discrete values
#DISCRETE_OS_SIZE = [20,20]#make them dynamic
DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

# Exploration settings
epsilon = 1  # not a constant, qoing to be decayed
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES//2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

#print(discrete_os_win_size)#[0.09, 0.007]

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))
#print(q_table.shape)#(20,20,3)
#print(q_table[0])#20,3
#print(q_table)#every possible combination

ep_rewards = []
aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}


def get_discrete_state(state):
	discrete_state = (state - env.observation_space.low)/discrete_os_win_size
	return tuple(discrete_state.astype(np.int))  # we use this tuple to look up the 3 Q values for the available actions in the q-table


discrete_state = get_discrete_state(env.reset())

#print(discrete_state)


#print(np.argmax(q_table[discrete_state]))#pick action with the highest absolute value --> 0

for episode in range(EPISODES):
	episode_reward = 0
	discrete_state = get_discrete_state(env.reset())
	done = False
	
	if episode % SHOW_EVERY == 0:
		render = True
		print(episode)
	else:
		render = False

	while not done:

		if np.random.random() > epsilon:
			# Get action from Q table
			action = np.argmax(q_table[discrete_state])
		else:
			# Get random action
			action = np.random.randint(0, env.action_space.n)


		new_state, reward, done, _ = env.step(action)
		episode_reward += reward
		
		
		new_discrete_state = get_discrete_state(new_state)

		if episode  % SHOW_EVERY == 0:
			env.render()
		#new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

		# If simulation did not end yet after last step - update Q table
		if not done:

			# Maximum possible Q value in next step (for new state)
			max_future_q = np.max(q_table[new_discrete_state])

			# Current Q value (for current state and performed action)
			current_q = q_table[discrete_state + (action,)]

			# And here's our equation for a new Q value for current state and action
			new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

			# Update Q table with new Q value
			q_table[discrete_state + (action,)] = new_q


		# Simulation ended (for any reson) - if goal position is achived - update Q value with reward directly
		#elif new_state[0] >= env.goal_position:
		elif new_state[0] >= env.unwrapped.goal_position:
			#q_table[discrete_state + (action,)] = reward
			q_table[discrete_state + (action,)] = 0
			print("We made it on episode: ", episode)

		discrete_state = new_discrete_state

	# Decaying is being done every episode if episode number is within decaying range
	if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
		epsilon -= epsilon_decay_value
		
	ep_rewards.append(episode_reward)
	
	if not episode % SHOW_EVERY:
		average_reward = sum(ep_rewards[-SHOW_EVERY:])/len(ep_rewards[-SHOW_EVERY:])
		aggr_ep_rewards['ep'].append(episode)
		aggr_ep_rewards['avg'].append(average_reward)
		aggr_ep_rewards['min'].append(min(ep_rewards[-SHOW_EVERY:]))
		aggr_ep_rewards['max'].append(max(ep_rewards[-SHOW_EVERY:]))
	
	print("Episode: ",episode," avg: ",average_reward, " min: ", min(ep_rewards[-SHOW_EVERY:]), " max: ", max(ep_rewards[-SHOW_EVERY:]))
	
env.unwrapped.close()

plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label="avg")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label="min")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label="max")
plt.legend(loc=4)
plt.show()