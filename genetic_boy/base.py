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
	

New UPDATE:
Producing a generation will override the previous generation, only producing fit children.
'''
import random as r
import numpy as np
from progress.spinner import Spinner
import datetime
import time
# http://oeis.org/A000170
# The number of solutions is OEIS sequence A000170:
# 1, 2, 3, 4, ...
# 1 ,0,0,2,10,4,40,92,352,724,2680,14200,73712,365596,2279184,14772512,
# 95815104,666090624,4968057848,39029188884,314666222712,2691008701644,
# 24233937684440,227514171973736,2207893435808352,22317699616364044,234907967154122528

# just to hold our states
class State():
	
	def __init__(self,n=8,val=None):
		if(val == None):
			self.state = generate_state(n)
		else:
			self.state = val
		self.children = 0

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
	states = [State(n) for x in range(pop)]

	return states

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

# change this to only return parents with a fitness of 4 or less
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
def three_way_tournament(a,b):
	if(len(a) != len(b)):
		print('error: states are not the same size!')
		return
	
	n = len(a)
	child = [-1 for x in range(n)]
	nums  = []

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
#

# reproduce
def reproduce(a,b):
	if(len(a) != len(b)):
		print('error: states are not the same size!')
		return
	# three way tournament
	child = three_way_tournament(a,b)
	return child


# These also might change if we dont find children
# the mutate functions
def slight_mutate(child):
	return single_mutate(child)

def med_mutate(child):
	# only do one side of the guy
	state_1 = single_mutate(child)
	sub_1_1 = single_mutate(state_1)
	sub_1_2 = single_mutate(state_1)
	return tournament_select(sub_1_1,sub_1_2)

# for getting a really different child
def heavy_mutate(child):
	state_1 = single_mutate(child)
	state_2 = single_mutate(child)

	sub_1_1 = single_mutate(state_1)
	sub_1_2 = single_mutate(state_1)

	sub_2_1 = single_mutate(state_2)
	sub_2_2 = single_mutate(state_2)

	sub_1_w = three_way_tournament(sub_1_1,sub_1_2)
	sub_2_w = three_way_tournament(sub_2_1,sub_2_2)
	return tournament_select(sub_1_w,sub_2_w)	
#
def eval_mutate(x,y,child):
	fit   = cal_fitness(child)
	fit_a = cal_fitness(x)
	fit_b = cal_fitness(y)
	if((fit_a < fit) or (fit_b < fit)):
		# if our child is not stronger than the others generate a new guy
		if(fit > 0 and fit < 2):
			# slight or maybe med
			if(r.randint(0,100) > chance):
				child = med_mutate(child)
			else:
				child = slight_mutate(child)
		# now check the medium chance condition		
		elif(fit > 2 and fit < (n-(n/2) * 2)):
			if(r.randint(0,100) > chance):
				child = heavy_mutate(child)
			else:
				child = med_mutate(child)
				
		# If we are that unfit heavy mutation
		else:
			child = heavy_mutate(child)
			
			# else there is still a chance of a slight mutation
	else:
		if(r.randint(0,100) > chance):
			child = slight_mutate(child)

	return child
# # # # # # MAIN SECTION HERE
if __name__ == '__main__':
	start_time = time.time()
	n = 8
	chance = 65
	i = 0
	solutions = []
	population = generate_pop(pop=200000,n=8)
	# 92
	
	print(len(solutions))
	debug = True
	
	# first eval population
	spinner = Spinner('')
	for q  in range(len(population)):
		state = population[q].state
		unique = True
		if(cal_fitness(state) == 0):
			# add the guy
			for boy in solutions:
				if(compare_state(state,boy)):
					unique = False
			if(unique):
				solutions.append(state)
				print('{}/92 FOUND SOLUTION: {}'.format(len(solutions),state))
		spinner.next()
	# now check for duplicates
	spinner = Spinner('working ')
	total_states = len(population)
	while(len(solutions) != 92):
		if(i % 10 == 0):
			print(' GENERATION: {} TOTAL STATES CREATED: {}'.format(i, total_states))
			elapsed_time = time.time() - start_time
			print(' Time Elapsed: {}'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
			print('-----------------------------------------------------------------')

		max_child = 200000
		new_pop = []
		best_child = [0 for k in range(n)]
		#print('----- NEXT GENERATION -----')
		for u in range(max_child): # now to generate the guys
			#print('pop {}'.format(len(population)))
			x, y = get_two(population)
			x.children += 1
			y.children += 1
			child = State(val=reproduce(x.state,y.state))
			# now evaluate the child
			child.state = eval_mutate(x.state,y.state,child.state)
			# then add the guy
			population.append(child)
			# check if this guy is a solution
			unique = True
			if(cal_fitness(child.state) == 0):
				# add the guy
				for q in range(len(solutions)):
					state = solutions[q]
					if(compare_state(child.state,state)):
						unique = False
				if(unique):
					solutions.append(child.state)
					print(' {}/92 FOUND SOLUTION: {}'.format(len(solutions),child.state))
			#else:
				#if(cal_fitness(child.state) < cal_fitness(best_child)):
					#best_child = child
					#if(debug): print('best child: {} {}'.format(cal_fitness(best_child),best_child))
			new_pop.append(child)
			# some last checks
			# WE DONT WANT THE PARENTS TO HAVE MORE THAN 4 CHILDREN
			if(x.children > 5):
				#print('State {} died: {} {}'.format(population.index(x),cal_fitness(x.state),x.state))
				population.remove(x)

			if(y.children > 5):
				#print('State {} died: {} {}'.format(population.index(y),cal_fitness(y.state),y.state))
				population.remove(y)
			spinner.next() # moved this guy here
		# now see if the child is a solution

		total_states += len(new_pop)
		population = new_pop
		i += 1
		
		#'''

	# after finding solutions write them to a file
	with open('solutions.txt', 'w') as file:
		for sol in solutions:
			file.write('{}\n'.format(sol))
		file.close()

	print('DONE!')
	elapsed_time = time.time() - start_time
	print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))






