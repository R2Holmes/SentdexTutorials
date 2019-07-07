import gym
import numpy as np

env = gym.make("MountainCar-v0")
env.reset()


#print(env.observation_space.high)#[0.6, 0.07]
#print(env.observation_space.low) #[-1.2, -0.07]
#print(env.action_space.n)#3


#create Q table with discrete values
#DISCRETE_OS_SIZE = [20,20]#make them dynamic
DISCRETE_OS_SIZE = [20] * len(env.observation_space.high)
discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE


#print(discrete_os_win_size)#[0.09, 0.007]

q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))
#print(q_table.shape)#(20,20,3)
#print(q_table[0])#20,3
#print(q_table)#every possible combination


done = False

while not done:
	action = 2 #3 actions: 0 push car left, 1 do nothing, 2 push car right
	new_state, reward, done, _ = env.step(action)
	#new_state: [position, velocity]
	#print(reward, new_state)#would run out of memory
	#reward = -1 until you reach the top then it's 0
	
	#convert continuous values into discrete values
	
	env.render()
	
env.close()
	