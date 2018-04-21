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
from progress.spinner import Spinner

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

	#print('    FITNESS')
	#print('---------------')
	#print_board(mat)
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
	#print('row count = {}'.format(row_count))
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
			#else:
				#temp_space[x][abs_val] = -1
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
		#else: temp_space[x][x] = -1
	if(count > 1): 
		#print('found {} pairs\n'.format(count-1))
		diag_right_count += (count - 1)

	# now for the other side 
	i = n-2
	j = n-1
	#temp_space[j][i] = 2
	#print('top_boy')
	while(i >= 1): # this is the first half
		count = 0
		#print('------')
		x = i
		while(x >= 0):
			val = abs(i - x)
			#print('{} {}'.format(x, j-val))
			if(temp_space[x][j-val] == 1):
				count += 1
			#else: 
				#temp_space[x][j-val] = -1
			x-=1 
		i -= 1

	# diag left
	# now for the middle
	i = n-1
	j = 0
	count = 0
	while(i >= 0 and j <= n-1):
		if(temp_space[i][j] == 1):
			count += 1
		#else:
			#temp_space[i][j] = -1
		j += 1 
		i -= 1 
	if(count > 1): 
		#print('found {} pairs\n'.format(count-1))
		diag_left_count += (count - 1)

	i = n-2
	j = 0
	while(i >= 0):
		#print('-----')
		count = 0
		for x in range(j,i+1):
			val = abs(i - x)
			#print('{} {}'.format(val, x))
			if(temp_space[x][val] == 1):
				count += 1
			#else:
				#temp_space[x][val] = -1
		if(count > 1): 
			#print('found {} pairs\n'.format(count-1))
			diag_left_count += (count - 1)

		i-=1

	# and the bottom half
	i = n
	j = 1
	#print('bot boy')
	while(j <= n-2):
		#print('-------')
		#print(j)
		y = i-1
		x = j
		count = 0
		while(x <= n-1):
			#print('{} {}'.format(y,x))
			if(temp_space[x][y] == 1):
				count += 1
			#else:
				#temp_space[x][y] = -1
			y -= 1
			x += 1

		if(count > 1): 
			#print('found {} pairs\n'.format(count-1))
			diag_left_count += (count - 1)
		j += 1


	#print('diag left  = {}'.format(diag_left_count))
	#print('diag right = {}'.format(diag_right_count))
	#print('---------------')
	#print_board(temp_space)


	# we don't need to check up or down because that case will never occur

	return (row_count + diag_left_count + diag_right_count)

# END OF ATTACK HELPERS # # # # # # # # # 

# setup the fitness function
def cal_fitness(space):
	n = len(space)
	#print(n)
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

# more stuff
def generate_pop(pop=1000,n=8):
	# returns a list size of pop states
	states = [generate_state(n=8) for x in range(pop)]

	return states

# return a state that has a fit of 0
def eval_pop(population):
	for x in range(len(population)):
		if(cal_fitness(population[x]) == 0):
			return population[x]
	
	return None

# # # # # # # # # # # # # #
# Genetic helpers
def get_rand_pair(n=8):
	x = r.randint(0,n)
	y = r.randint(0,n)
	if(y == x):
		while(y == x):
			y = r.randint(0,n)

	return x,y
# just compare two states
def compare_state(a,b):
	for x in range(len(a)):
		if(a[x] != b[x]):
			return False

	return True

def get_two(population):
	x = r.randint(0,len(population))
	y = r.randint(0,len(population))
	if(y == x):
		while(y == x):
			y = r.randint(0,len(population))

	return population[x-1], population[y-1]

# mutate helpers
def single_mutate(state):
	# swap two values in a state
	x = r.randint(0,len(state))
	y = r.randint(0,len(state))
	if(y == x):
		while(y == x):
			y = r.randint(0,len(state))
	x -= 1# our index was off by one
	y -= 1 

	temp = state[x]
	state[x] = state[y]
	state[y] = temp

	return state

# tournament select
def tournament_select(a,b):
	if(len(a) != len(b)):
		print('error: states are not the same size!')
		return

	a_fit = cal_fitness(a)
	b_fit = cal_fitness(b)
	return a if a_fit < b_fit else b
# 

# reproduce
def reproduce(a,b):
	if(len(a) != len(b)):
		print('error: states are not the same size!')
		return

	# two point crossover
	n = len(a)
	
	x = int(n/3)
	y = n-3
	#print(x)
	#print(y)
	child = [-1 for x in range(n)]
	nums  = []
	#crossover points
	# First use three way tournament using the parents
	for i in range(n):
		if(a[i] == b[i]):
			child[i] = a[i]
		else:
			nums.append(a[i])
			nums.append(b[i])


	# now fill in the rest
	for i in range(n):
		if(child[i] == -1):
			idx = (r.randint(0,len(nums))) - 1
			child[i] = nums[idx]

	return child


# the mutate function
def mutate(child):
	state_1 = single_mutate(child)
	state_2 = single_mutate(child)

	sub_1_1 = single_mutate(state_1)
	sub_1_2 = single_mutate(state_1)

	sub_2_1 = single_mutate(state_2)
	sub_2_2 = single_mutate(state_2)

	sub_1_w = tournament_select(sub_1_1,sub_1_2)
	sub_2_w = tournament_select(sub_2_1,sub_2_2)
	return tournament_select(sub_1_w,sub_2_w)	

def gen_child(a,b,chane=70):
	if(len(a) != len(b)):
		print('error: states are not the same size!')
		return
	child = reproduce(x,y)
	if(r.randint(0,100) > chance):
		child = mutate(child)

	return child

# # # # # # MAIN SECTION HERE
if __name__ == '__main__':
	#state_1 = [0, 3, 4, 5, 1, 6, 7, 2]
	#state_2 = [6, 0, 7, 1, 4, 2, 5, 3] # this is a solved state!
	#a = [2, 5, 1, 3, 8, 4, 7, 6]
	#b = [2, 4, 7, 3, 6, 1, 8, 5]
	#print(cal_fitness(state))
	#print(compare_state(state_1,state_2))
	
	#print(reproduce(a,b))
	n = 8
	chance = 65
	i = 0
	population = generate_pop(n=8)
	# 92
	solutions = []
	
	spinner = Spinner('working ')
	while(len(solutions) != 92):
		if(i % 100 == 0):
			print('Iteration: {} pop size: {}'.format(i, len(population)))
		
		max_child = r.randint(10,500)
		for x in range(max_child):
			x, y = get_two(population) 
			population.append(gen_child(x,y,chance=chance))

		check = eval_pop(population)

		if(check != None):
			unique = True
			if(len(solutions) > 0):
				for x in range(len(solutions)):
					if(compare_state(check,x)):
						unique = False
						break
				if(unique):
					solutions.append(check)
					print('Found solution! {}'.format(check))
		
		i += 1
		spinner.next()#'''

	# after finding solutions write them to a file
	with open('solutions.txt', 'w') as file:
		for sol in solutions:
			file.write('{}\n'.format(sol))
		file.close()
