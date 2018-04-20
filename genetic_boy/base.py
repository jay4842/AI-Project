# This will include our base code for setting up the project.

'''
	SETTING UP OUR PROBLEM
	- make our start state
	- a way to check fitness

	The genetic algorithm will be in its own file.

	state example
	[3, 4, 0, 6, 4, 5, 5, 6]
	each spot is the row of the board, then the number at the spot is what tile
	 the queen is on the row.

	at row 0 there is a queen on tile 3.
	
'''
import random as r
import numpy as np

# http://oeis.org/A000170
# The number of solutions is OEIS sequence A000170:
# 1, 2, 3, 4, ...
# 1 ,0,0,2,10,4,40,92,352,724,2680,14200,73712,365596,2279184,14772512,
# 95815104,666090624,4968057848,39029188884,314666222712,2691008701644,
# 24233937684440,227514171973736,2207893435808352,22317699616364044,234907967154122528

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
			if(space[i][j] == 1):
				line += 'Q '
			elif(space[i][j] == 0):
				line += '. '
			else:
				line += '~ '
		board += line + '\n'
		line = ''
	print(board)
# working on this

# Attack count

'''
Currently working out how to get this working, once I get it I will check to see how to make
 it more simple
'''
def count_attack_pairs(mat):

	print('    FITNESS')
	print('---------------')
	print_board(mat)
	n = len(mat)
	row_count        = 0
	diag_left_count  = 0
	diag_right_count = 0
	# count the queens in each row
	#  attacking pairs found = count - 1
	
	#line = ''
	for j in range(0,n):
		count = 0
		for i in range(0,n):
			#line += '{} '.format(mat[i][j])
			if(mat[i][j] == 1):
				count += 1
				
		#print(line)

		if(count > 1): 
			#print('found {} pairs\n'.format(count-1))
			row_count += (count - 1)
		#line = ''
	# end of row check
	#print('     diag\n---------------')
	# count the queens in the diagonals
	print('row count = {}'.format(row_count))
	temp_space = mat
	
	# left
	# right
	i = n-2
	j = 0
	#temp_space[j][i] = 2
	while(i >= 1): # this is the first half
		count = 0
		#print('------')
		for x in range(i,n):
			abs_val = abs(i - x)
			
			#print('{} {}'.format(x,abs(i - x)))
			if(temp_space[abs_val][x] == 1):
				count += 1
			else:
				temp_space[abs_val][x] = -1
		if(count > 1): 
			#print('found {} pairs\n'.format(count-1))
			diag_right_count += (count - 1)
		i -= 1
	# now for the middle
	i = 0
	j = 0
	count = 0
	for x in range(i,n):

		if(temp_space[x][x] == 1):
			count += 1
		else: temp_space[x][x] = -1
	if(count > 1): 
		#print('found {} pairs\n'.format(count-1))
		diag_right_count += (count - 1)

	# now for the other side 
	i = 0
	j = 1

	print('diag right = {}'.format(diag_right_count))
	print('---------------')
	print_board(temp_space)


	# we don't need to check up or down because that case will never occur

	return (row_count + diag_left_count + diag_right_count)

# END OF ATTACK HELPERS # # # # # # # # # 

# setup the fitness function
def cal_fitness(space):
	n = len(space)
	print(n)
	# make a temporary array to hold the state, making evaluating easy
	temp_space = [[0 for i in range(n)] for j in range(n)]
	#print(temp_space)
				
	fit = 0
	attk_pairs = [] # will store pair info, ex attk_pairs = [[2,2,1,3],...] # will store a pair of queens in each sub array

	for j in range(0,n): # show the board for now
		for i in range(0,n):
			if(j == space[i]):
				temp_space[i][j] = 1
	
	return count_attack_pairs(temp_space)

if __name__ == '__main__':
	space = generate_state(n=8)
	print(space)

	fit = cal_fitness(space)
	print(fit)



