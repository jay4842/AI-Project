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

# print a board based on a temp_space
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
	# START OF CORNER CASES #############################
	# left top
	if(i == 0 and j == 0):
		# sides
		for x in range(1,n):
			# check right
			if(space[i][j+x] == 1):
				attacks.append([i,j,i,j+x])
				break # stop looking
		# check down
		for x in range(1,n):
			# check down
			if(space[i+x][j] == 1):
				attacks.append([i,j,i+x,j])
				break # stop looking
		# diag
		for x in range(1,n):
			# check diag down right
			if(space[i+x][j+x] == 1):
				attacks.append([i,j,i+x,j+x])
				break # stop looking
	#top right #############################
	elif(i == 0 and j == n-1):
		# sides
		for x in range(1,n):
			# check left
			if(space[i][j-x] == 1):
				attacks.append([i,j,i,j-x])
				break # stop looking
		# check down
		for x in range(1,n):
			# check down
			if(space[i+x][j] == 1):
				attacks.append([i,j,i+x,j])
				break # stop looking
		# diag
		for x in range(1,n):
			# check diag down right
			if(space[i+x][j-x] == 1):
				attacks.append([i,j,i+x,j-x])
				break # stop looking
	# left bottom #############################
	elif(i == n-1 and j == 0):
		# sides
		for x in range(1,n):
			# check right
			if(space[i][j+x] == 1):
				attacks.append([i,j,i,j+x])
				break # stop looking
		# check up
		for x in range(1,n):
			# check right
			if(space[i-x][j] == 1):
				attacks.append([i,j,i-x,j])
				break # stop looking
		# diag
		for x in range(1,n):
			# check diag up right
			if(space[i-x][j+x] == 1):
				attacks.append([i,j,i-x,j+x])
				break # stop looking
	
	# right bottom #############################
	elif(i == n-1 and j == n-1):
		# sides
		for x in range(1,n):
			# check left
			if(space[i][j-x] == 1):
				attacks.append([i,j,i,j-x])
				break # stop looking
		# check up
		for x in range(1,n):
			# check up
			if(space[i-x][j] == 1):
				attacks.append([i,j,i-x,j])
				break # stop looking
		# diag
		for x in range(1,n):
			# check diag up left
			if(space[i-x][j-x] == 1):
				attacks.append([i,j,i-x,j-x])
				break # stop looking
	# END OF CORNERS #############################
	
	# SIDES

	#  LEFT SIDE
	elif((i > 0 and i < n-1) and j == 0):
		print('check right')
		for x in range(1,n):
			print(x)
			# check right
			if(space[i][x] == 1):
				attacks.append([i,j,i,x])
				break # stop looking
		# check down
		print('check down')
		for x in range(i+1,n):
			# check down
			print(x)
			if(space[x][j] == 1):
				attacks.append([i,j,x,j])
				break # stop looking
		# check up
		print('check up')
		for x in range(1,n-(n-i)): 
			# check up
			print(x)
			if(space[i-x][j] == 1):
				attacks.append([i,j,i-x,j])
				break # stop looking
		# diag
		print('check diag down right')
		for x in range(i+1,n):
			print(x)
			# check diag down right
			if(space[x][j+x] == 1):
				attacks.append([i,j,x,j+x])
				break # stop looking
		#
		print('check diag up right')
		for x in range(1,n-(n-i)):
			print(x)
			# check diag up right
			if(space[i-x][j+x] == 1):
				attacks.append([i,j,i-x,j+x])
				break # stop looking

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
