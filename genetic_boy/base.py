# This will include our base code for setting up the project.

'''
	SETTING UP OUR PROBLEM
	- make our start state
	- a way to check fitness

	The genetic algorithm will be in its own file.

'''
import random as r
import numpy as np


# this will generate a state of n queens
def generate_state(n=8):
	# Start with 8 as the normal
	space = [0 for i in range(n)]

	# now populate the state randomly
	#  space at i can be from 0 to n
	for i in range(0,n):
		space[i] = r.randint(0,n-1)
	return space
# thats it nothing special

# generate a board based on a state
def make_space(state):
	n = len(state)
	# make a temporary array to hold the state, making evaluating easy
	temp_space = [[0 for i in range(n)] for j in range(n)]
	#print(temp_space)

	for j in range(0,n): # show the board for now
		for i in range(0,n):
			if(j == space[i]):
				temp_space[i][j] = 1

	return temp_space

# print a board cleanly
def print_board(space):
	n = len(space)
	line = ''
	board = ''
	for j in range(0,n): # show the board for now
		for i in range(0,n):
			line += str(space[i][j]) + ' '
		board += line + '\n'
		line = ''
	print(board)
# working on this

def check_attack(space,i,j):
	print('--------------')
	print('queen[{},{}]'.format(i,j))
	
	print(space[i][j])
	#print_board(space)
	attacks = []
	n = len(space)
	
	# if center
	# check for unique values
	unique_attks = []

	print(attacks)
	return attacks



# setup the fitness function
def cal_fitness(space):
	n = len(space)
	print(n)
	# make a temporary array to hold the state, making evaluating easy
	temp_space = [[0 for i in range(n)] for j in range(n)]
	#print(temp_space)
				
	fit = 0
	attk_pairs = [] # will store pair info, ex attk_pairs = [[2,2,1,3],...] # will store a pair of queens in each sub array

	line = ''
	board = ''
	for j in range(0,n): # show the board for now
		for i in range(0,n):
			if(j == space[i]):
				temp_space[i][j] = 1
	print_board(temp_space)

	print(np.shape(temp_space))
	for i in range(0,n):
		#print('queen[{},{}]'.format(space[i],i)) # fix the indexing of the temp space
		attk_pairs.append(check_attack(temp_space,space[i],i))
	#print(np.unique(attk_pairs))
	return fit

if __name__ == '__main__':
	space = generate_state(n=8)
	print(space)

	fit = cal_fitness(space)
	print(fit)



