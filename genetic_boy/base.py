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
import os

# http://oeis.org/A000170
# The number of solutions is OEIS sequence A000170:
# 1, 2, 3, 4, ...
# 1 ,0,0,2,10,4,40,92,352,724,2680,14200,73712,365596,2279184,14772512,
# 95815104,666090624,4968057848,39029188884,314666222712,2691008701644,
# 24233937684440,227514171973736,2207893435808352,22317699616364044,234907967154122528

def make_dir(directory):
	directory = "".join(str(x) for x in directory)
	try:
		os.stat(directory)
	except FileNotFoundError:
		try:
			os.mkdir(directory)
		except FileNotFoundError:
			subDir = directory.split('/')
			while(subDir[-2] == ''):
				subDir = subDir[:-2]
			newDir = ""
			for x in range(len(subDir)-2):
				newDir += (subDir[x])
				newDir += ('/')
			make_dir(newDir)
			os.mkdir(directory)

# just to hold our states
class State():
	
	# can have a state passed as a parameter
	#  or randomly create it
	def __init__(self,n=8,val=None):
		self.children = 0
		self.mutation = None
		if(val == None):
			self.state = generate_state(n)
			if(r.randint(0,100) > 80):
				self.state = slight_mutate(self.state)
				self.mutation = 'Slight'
		else:
			self.state = val
		

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
			if(j == state[i]):
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
				line += '~ ' # <- This is a debug feature for count attack pairs
		board += line + '\n'
		line = ''
	print(board)
# working on this

# Attack count

'''
Currently working out how to get this working, once I get it I will check to see how to make
 it more simple

 Okay so this guy works by going horizontally and diagonally to count the number of queens in
 an attacking state.

 It might look like a lot but it really just traverses the board and returns the number of attacks.
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

def check_clashes(space):
	clashes = 0;
	# calculate row and column clashes
	# just subtract the unique length of array from total length of array
	# [1,1,1,2,2,2] - [1,2] => 4 clashes
	row_col_clashes = abs(len(space) - len(np.unique(space)))
	clashes += row_col_clashes

	# calculate diagonal clashes
	for i in range(len(space)):
		for j in range(len(space)):
			if ( i != j):
				dx = abs(i-j)
				dy = abs(space[i] - space[j])
				if(dx == dy):
					clashes += 1


	return clashes

# setup the fitness function
def cal_fitness(space): # RETURN THE NUMBER OF ATTACKS FOUND
	n = len(space)
	#print(n)
	# make a temporary array to hold the state, making evaluating easy
	temp_space = [[0 for i in range(n)] for j in range(n)]
	#print(temp_space)
	
	return check_clashes(space)

# more stuff
# GENERATE A RANDOM POPULATION OF STATES
def generate_pop(pop=1000,n=8):
	# returns a list size of pop states
	states = [State(n) for x in range(pop)]

	return states

# # # # # # # # # # # # # #
# Genetic helpers
def get_rand_pair(n=8): # return two random numbers, helpers that is most likely not used....
	x = r.randint(0,n)
	y = r.randint(0,n)
	if(y == x):
		while(y == x):
			y = r.randint(0,n)

	return x,y
# just compare two states
def compare_state(a,b): # check if two states are equal
	for x in range(len(a)):
		if(a[x] != b[x]):
			return False

	return True

# Return two parents and make sure they are not the same
def get_two(population):
	x = r.randint(0,len(population))
	y = r.randint(0,len(population))
	if(y == x):
		while(y == x):
			y = r.randint(0,len(population))

	return population[x-1], population[y-1]

# mutate helpers
#  swaps two values in a state
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
#  returns the fittest parent
def tournament_select(a,b):
	if(len(a) != len(b)):
		print('error: states are not the same size!')
		return

	a_fit = cal_fitness(a)
	b_fit = cal_fitness(b)
	return a if a_fit < b_fit else b
# 
# Three way tournament.
# - Transfer where the two parents are equal to the parent,
# - then use the numbers not transfered as the domain of the other spots,
# - Use these domains to randomly fill in the empty areas
def three_way_tournament(a,b):
	if(len(a) != len(b)):
		print('error: states are not the same size!')
		return
	
	n = len(a)
	child = [-1 for x in range(n)] # make the child
	nums  = []

	# See where the parents are equal, else add to the domain
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

# simple three way tournament crossover
#  Try it with another way?
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

	sub_1_w = tournament_select(sub_1_1,sub_1_2)
	sub_2_w = tournament_select(sub_2_1,sub_2_2)
	return tournament_select(sub_1_w,sub_2_w)	
#

# This will be a bridge for testing out different ways to get fit children!
def eval_mutate(x,y,child,chance=75):
	fit   = cal_fitness(child.state)
	fit_a = cal_fitness(x.state)
	fit_b = cal_fitness(y.state)

	if(r.randint(0,100) > chance):
		if(r.randint(0,100) > 50):
			child.state = slight_mutate(child.state)
			child.mutation = 'Slight'
		elif(r.randint(0,100) > 45):
			child.state = med_mutate(child.state)
			child.mutation = 'Medium'
		else:
			child.state = heavy_mutate(child.state)
			child.mutation = 'Heavy'

	return child
# # # # # # MAIN SECTION HERE
if __name__ == '__main__':
	total_sols = [1 ,0,0,2,10,4,40,92,352,724,2680,14200,73712,365596,2279184,14772512]
	start_time = time.time()
	make_dir('state_logs/')
	child_limit = 7
	n = 7
	chance = 65
	i = 0
	solutions = []
	state_log = open('state_logs/initial_state_log.txt','w')
	population = generate_pop(pop=10000,n=n)
	# 92
	
	# print_board(make_space(population[0].state))
	# print(check_clashes(population[0].state))
	
	print(len(solutions))
	debug = True
	
	best_child  = cal_fitness(population[0].state)
	worst_child = cal_fitness(population[0].state)
	# open our log
	# COMMENT OUT THE PRINT STUFF IF YOU DONT WANT TO SEE IT
	log_ = open('log_.txt','w')
	# first eval population
	spinner = Spinner('') # EVALUATE INITIAL POPULATION
	log_.write('Evaluating initial population...\n')
	for q in range(len(population)):
		curr_time = time.time()
		state = population[q].state
		state_log.write('Event [{}]\n'.format(time.strftime("%H:%M:%S", time.gmtime(curr_time))))
		state_log.write('fit[{}] {} created with a mutation: {}!\n'.format(cal_fitness(state),state,population[q].mutation))
		state_log.write('---------------------------------------------------\n')
		unique = True
		fit = cal_fitness(state)

		if(fit == 0):
			# add the guy
			for boy in solutions:
				if(compare_state(state,boy)):
					unique = False
			if(unique):
				solutions.append(state)
				print('{}/{} FOUND SOLUTION: {}'.format(len(solutions),total_sols[n-1],state))
				log_.write('{}/{} FOUND SOLUTION: {}\n'.format(len(solutions),total_sols[n-1],state))
		else:
			if(fit < worst_child):
				worst_child = fit
			elif(fit > best_child):
				best_child = fit
		spinner.next()
	# now check for duplicates
	spinner = Spinner('working ')
	total_states = len(population)
	gen_size = len(population)
	state_log.close()
	# START MAKING NEW GENERATIONS
	while(len(solutions) != total_sols[n-1]):
		state_log = open('state_logs/state_log_{}.txt'.format(i),'w')
		elapsed_time = time.time() - start_time
		if(i % 10 == 0):
			print(' GENERATION: {} TOTAL STATES CREATED: {}'.format(i, total_states))
			print(' SIZE OF GENERATION: {}'.format(gen_size))
			print(' Time Elapsed: {}'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
			print('-----------------------------------------------------------------')
		log_.write('GENERATION: {} TOTAL STATES CREATED: {}\n'.format(i, total_states))
		log_.write('Time Elapsed: {}\n'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
		log_.write('-----------------------------------------------------------------\n')
		max_child = 10000
		new_pop = []
		
		#print('----- NEXT GENERATION -----')
		# SHUFFLE OUR POPULATION
		r.shuffle(population)
		for u in range(max_child): # now to generate the guys
			#print('pop {}'.format(len(population)))
			x, y = get_two(population)
			#
			x.children += 1
			y.children += 1
			child = State(val=reproduce(x.state,y.state))
			# now evaluate the child
			child = eval_mutate(x,y,child)
			# More log stuff here
			curr_time = time.time()
			state_log.write('Event [{}]\n'.format(time.strftime("%H:%M:%S", time.gmtime(curr_time))))
			state_log.write('Parents: {} [{}] and {} [{}] created:\n'.format(x.state,x.mutation,y.state,y.mutation))
			state_log.write('fit[{}] {} created with a mutation: {}!\n'.format(cal_fitness(child.state),child.state,child.mutation))
			state_log.write('---------------------------------------------------\n')
			# then add the guy
			population.append(child)
			total_states += 1 # add one to the running total

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
					print('{}/{} FOUND SOLUTION: {}'.format(len(solutions),total_sols[n-1],state))
					log_.write('{}/{} FOUND SOLUTION: {}\n'.format(len(solutions),total_sols[n-1],state))
			else:
				child_fit = cal_fitness(child.state)
				if(child_fit < worst_child):
					worst_child = child_fit
				elif(child_fit > best_child):
					best_child = child_fit

					#if(debug): print('best child: {} {}'.format(cal_fitness(best_child),best_child))
			new_pop.append(child)
			# some last checks
			# WE DONT WANT THE PARENTS TO HAVE MORE THAN 4 CHILDREN
			if(x.children > child_limit):
				curr_time = time.time()
				state_log.write('Event [{}]\n'.format(time.strftime("%H:%M:%S", time.gmtime(curr_time))))
				state_log.write('State {} died: {} {}\n'.format(population.index(x),cal_fitness(x.state),x.state))
				state_log.write('---------------------------------------------------\n')
				population.remove(x)

			if(y.children > child_limit):
				curr_time = time.time()
				state_log.write('Event [{}]\n'.format(time.strftime("%H:%M:%S", time.gmtime(curr_time))))
				state_log.write('State {} died: {} {}\n'.format(population.index(y),cal_fitness(y.state),y.state))
				population.remove(y)
				state_log.write('---------------------------------------------------\n')
			spinner.next() # moved this guy here
		# now see if the child is a solution
		gen_size = len(population)
		i += 1

		# States that are unfit will be killed to preserve a survival of the fittest style.
		# Here parents that have a fitness that is too low will be killed

		medium_fit = [f for f in range(best_child,worst_child)]
		medium_fit = len(medium_fit) / 2

		for q in range(len(population)-1):
			try:
				fit = cal_fitness(population[q].state)
				# If the fitness is less than or equal to the worst child it dies
				if(fit >= worst_child):
					curr_time = time.time()
					state_log.write('Event [{}]\n'.format(time.strftime("%H:%M:%S", time.gmtime(curr_time))))
					state_log.write('State {} died: {} {}\n'.format(population[q].state,fit))
					state_log.write('---------------------------------------------------\n')
					population.remove(population[q])
					q -= 1
				# If the fitness is less than the medium there is a chance that it can be killed
				elif(fit > medium_fit):
					if(r.randint(0,100) > 60):
						curr_time = time.time()
						state_log.write('Event [{}]\n'.format(time.strftime("%H:%M:%S", time.gmtime(curr_time))))
						state_log.write('State {} died: {} {}\n'.format(population[q].state,fit))
						state_log.write('---------------------------------------------------\n')
						population.remove(population[q])
						q -= 1
			except Exception as e:
				break # break out of our loop here
		
		best_child  = cal_fitness(population[0].state)
		worst_child = cal_fitness(population[0].state)

		# kill parents
		elapsed_time = time.time() - start_time
		state_log.write('Iteration Complete!\nTime passed {}\n\n'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
		state_log.close()	
		

	# after finding solutions write them to a file
	with open('solutions.txt', 'w') as file:
		for sol in solutions:
			file.write('{}\n'.format(sol))
		file.close()

	log_.write('DONE\n')
	#state_log.write('DONE\n')
	print('DONE!')
	elapsed_time = time.time() - start_time
	print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
	log_.write('Time Elapsed: {}\n'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
	log_.close()
	#state_log.close()#'''

