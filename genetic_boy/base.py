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
	space = [0 for i in range(0,n)]

	# now populate the state randomly
	#  space at i can be from 0 to n
	for i in range(0,n):
		space[i] = r.randint(0,n-1)
	return space
# thats it nothing special

# working on this
def check_attack(space,i,j):
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
			# check right
			if(space[i+x][j] == 1):
				attacks.append([i,j,i+x,j])
				break # stop looking
		# diag
		for x in range(1,n):
			# check right
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
			# check right
			if(space[i+x][j] == 1):
				attacks.append([i,j,i+x,j])
				break # stop looking
		# diag
		for x in range(1,n):
			# check right
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
			# check right
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
			# check right
			if(space[i-x][j] == 1):
				attacks.append([i,j,i-x,j])
				break # stop looking
		# diag
		for x in range(1,n):
			# check right
			if(space[i-x][j-x] == 1):
				attacks.append([i,j,i-x,j-x])
				break # stop looking
	# END OF CORNERS #############################
	
	# STAT OF SIDES
	# left side
	elif(i == 0 and (j > 0 and j < n-1)):
		
		# check up
		for x in range(i,n-i-n): # move for only the squares in the board
			if(space[i-x][j] == 1):
				attacks.append([i,j,i-x,j])
				break # stop looking
		# check down
		for x in range(i,n): # move for only the squares in the board
			if(space[i+x][j] == 1):
				attacks.append([i,j,i+x,j])
				break # stop looking

		# check down diag
		for x in range(i,n): # move for only the squares in the board
			if(space[i+x][j] == 1):
				attacks.append([i,j,i+x,j+x])
				break # stop looking

		# check up diag
		for x in range(i,n-i-n): # move for only the squares in the board
			if(space[i-x][j-x] == 1):
				attacks.append([i,j,i-x,j-x])
				break # stop looking
	# top side
	# right side
	# bottom side

	# if center

# setup the fitness function
def cal_fitness(space):
	n = len(space)
	print(n)
	# make a temporary array to hold the state, making evaluating easy
	temp_space = [[0 for i in range(0,n)] for i in range(0,n)]
	#print(temp_space)
				
	fit = 0
	attk_pairs = [] # will store pair info, ex attk_pairs = [[2,2,1,3],...] # will store a pair of queens in each sub array

	line = ''
	board = ''
	for j in range(0,n): # show the board for now
		for i in range(0,n):
			if(j == space[i]):
				temp_space[i][j] = 1
			line += str(temp_space[i][j]) + ' '
			# cal here
			if(temp_space[i][j] == 1):
				attk_pairs.append(check_attack(space,i,j))
				pass
		#print(line)
		board += line + '\n'
		line = ''

	print(board)
	print(np.unique(attk_pairs))
	return fit

if __name__ == '__main__':
	space = generate_state()
	print(space)

	fit = cal_fitness(space)
	print(fit)
