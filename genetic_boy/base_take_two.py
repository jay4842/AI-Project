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

# fact boy
def factorial(n):
	if n == 0:
		return 1
	else:
		return n * factorial(n-1)

# calculate the max boys
def max_clash(n):
	return ( factorial(n) / (factorial(2) * factorial(n-2)) )

# make a folder, sometimes acts weird?
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

		self.fit = cal_fitness(self.state)
		

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
	
	max_boys = max_clash(n)

	return max_boys - check_clashes(space)

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
def get_two(population,fit_thresh):
	size = len(population)-1
	x = r.randint(0,size)
	y = r.randint(0,size)
	if(y == x):
		while(y == x):
			y = r.randint(0,len(population))
	# we still want to get fit populations
	'''while(population[x-1].fit > fit_thresh or population[y-1].fit > fit_thresh):
		x = r.randint(0,size)
		y = r.randint(0,size)
		if(y == x):
			while(y == x):
				y = r.randint(0,size)#'''

	return x-1, y-1

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

# double mutate, switch two values (total of four) in state
def double_mutate(state):
	w = r.randint(0, len(state))
	x = r.randint(0, len(state))
	y = r.randint(0, len(state))
	z = r.randint(0, len(state))

	if(w == x and w == y and w == z):
		while(w == x and w == y and w == z):
			w = r.randint(0, len(state))
	if(x == y and x == z):
		while(x == y and x == z):
			x = r.randint(0, len(state))
	if(y == z):
		while(y == z):
			y = r.randint(0, len(state))

	w -= 1
	x -= 1
	y -= 1
	z -= 1

	temp = state[w]
	state[x] = state[w]
	state[x] = temp

	temp = state[y]
	state[y] = state[z]
	state[z] = temp

	return state
#end double_mutate

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
			del nums[idx] # remove for the nums list for uniqueness


	return child

# one point crossover
def one_point_crossover(a,b):
	if(len(a) != len(b)):
		print('error: states are not the same size!')
		return
	
	#print(a)
	#print(b)

	n = len(a)
	child_1 = a[0:int(n/2)] + b[int(n/2):]
	child_2 = b[0:int(n/2)] + a[int(n/2):]
	# # # # #
	return child_1,child_2

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


# These also might change if we don't find children
# the mutate functions
def slight_mutate(child):
	if(r.randint(0,100) > 50):
		return single_mutate(child)
	else:
		return double_mutate(child)

def med_mutate(child):
	# only do one side of the guy
	state_1 = single_mutate(child)
	sub_1_1 = single_mutate(state_1)
	sub_1_2 = double_mutate(state_1)
	return tournament_select(sub_1_1,sub_1_2)

# for getting a really different child
def heavy_mutate(child):
	state_1 = single_mutate(child)
	state_2 = double_mutate(child)

	sub_1_1 = single_mutate(state_1)
	sub_1_2 = single_mutate(state_1)

	sub_2_1 = double_mutate(state_2)
	sub_2_2 = double_mutate(state_2)

	sub_1_w = tournament_select(sub_1_1,sub_1_2)
	sub_2_w = tournament_select(sub_2_1,sub_2_2)
	return tournament_select(sub_1_w,sub_2_w)	
#

# This will be a bridge for testing out different ways to get fit children!
def eval_mutate(x,y,child,target,chance=95):
	fit   = child.fit
	fit_a = x.fit
	fit_b = y.fit

	if(fit != target):
		if(r.randint(0,100) > chance):
			if(r.randint(0,100) > 50):
				child.state = slight_mutate(child.state)
				child.fit = cal_fitness(child.state)
				child.mutation = 'Slight'
			elif(r.randint(0,100) > 45):
				child.state = med_mutate(child.state)
				child.fit = cal_fitness(child.state)
				child.mutation = 'Medium'
			else:
				child.state = heavy_mutate(child.state)
				child.fit = cal_fitness(child.state)
				child.mutation = 'Heavy'

	return child

def is_solution(state,solutions,max_boys):
	# add the guy
	for q in range(len(solutions)):
		if(compare_state(state,solutions[q])):
			return False

	return True # if we get here its a solution

# # # # # # MAIN SECTION HERE
if __name__ == '__main__':
	total_sols = [1 ,0,0,2,10,4,40,92,352,724,2680,14200,73712,365596,2279184,14772512]
	max_seconds = 5
	n = input('input n -> ');
	n = int(n)
	pop = input('input pop -> ')
	pop = int(pop)
	
	try:
		os.mkdir('logs/state_logs')
	except Exception as e:
		print(e)
	# 92
	
	# print_board(make_space(population[0].state))
	# print(check_clashes(population[0].state))
	debug = True

	# open our log
	# COMMENT OUT THE PRINT STUFF IF YOU DONT WANT TO SEE IT
	# first eval population
	spinner = Spinner('') # EVALUATE INITIAL POPULATION
	# make our log save folder
	folder = ('logs/n_{}_{}'.format(n,pop))
	try:
		os.mkdir(folder)
	except Exception as e:
		print(e)
	for e in range(0,5):
		try:
			start_time = time.time()
			end_time = start_time + 60 * max_seconds
			print('TEST {}'.format(e+1))
			child_limit = 7
			#n = 7
			max_boys = max_clash(n)
			chance = 65
			fit_thresh = max_boys - (max_boys/2)
			i = 0
			gen = 0
			solutions = []
			pop_size = pop
			#state_log = open('state_logs/initial_state_log.txt','w')
			population = generate_pop(pop=pop_size,n=n)
			max_child = pop_size
			print('size of solutions = {}'.format(len(solutions)))
			with open('{}/log_{}_{}_{}.txt'.format(folder,n,pop_size,e),'w') as log_:
				log_.write('Evaluating initial population...\n')
				for q in range(len(population)):
					state = population[q].state
					unique = True
					fit = population[q].fit

					if(fit == max_boys):
						if(is_solution(state,solutions,max_boys)):
							solutions.append(state)
							elapsed_time = time.time() - start_time
							print_board(make_space(state))
							out = '{}/{} FOUND SOLUTION AT ITERATION {}: {}'.format(len(solutions),total_sols[n-1],i,state)
							print(out)
							print(' Time Elapsed: {}\n'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
							log_.write(out + '\n')
							#log_.flush()

					spinner.next()
					i += 1
				# now check for duplicates
				spinner = Spinner('working ')
				total_states = len(population)
				gen_size = len(population)
				#state_log.close()
				# START MAKING NEW GENERATIONS
				while(len(solutions) != total_sols[n-1]):
					elapsed_time = time.time() - start_time
					if(gen % 10 == 0):
						#print(' GENERATION: {} TOTAL STATES CREATED: {}'.format(gen, total_states))
						#print(' SIZE OF GENERATION: {}'.format(gen_size))
						#print(' Time Elapsed: {}'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
						#print('-----------------------------------------------------------------')

						# life will get harder
						if(gen > 0 and fit_thresh > max_boys-3):
							fit_thresh -= 1
					new_pop = []
					
					#print('----- NEXT GENERATION -----')
					# SHUFFLE OUR POPULATION
					r.shuffle(population) # better random selection
					for u in range(max_child): # now to generate the guys
						#print('pop {}'.format(len(population)))
						x, y = get_two(population,fit_thresh) # can also delete unfit parents
						#
						parent_1 = population[x]
						parent_2 = population[y]

						s1,s2 = one_point_crossover(parent_1.state,parent_2.state)
						c1 = State(n=n,val=s1)
						c2 = State(n=n,val=s2)
						# now evaluate the child
						c1 = eval_mutate(parent_1,parent_2,c1,max_boys)
						c2 = eval_mutate(parent_1,parent_2,c2,max_boys)
						# More log stuff here
						population[x] = c1
						population[y] = c2
						# then replace our parents
						

						# check if this guy is a solution
						#
						if(c1.fit == max_boys):
							if(is_solution(c1.state,solutions,max_boys)):
								solutions.append(c1.state)
								print(' ')# formatting
								elapsed_time = time.time() - start_time
								print_board(make_space(c1.state))
								out = '{}/{} FOUND SOLUTION AT ITERATION {}: {}'.format(len(solutions),total_sols[n-1],i,c1.state)
								print(out)
								print(' Time Elapsed: {}\n'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
								log_.write(out + '\n')
								#log_.flush()

						if(c2.fit == max_boys):
							if(is_solution(c2.state,solutions,max_boys)):
								solutions.append(c2.state)
								print(' ') # formatting 
								elapsed_time = time.time() - start_time
								print_board(make_space(c2.state))
								out = '{}/{} FOUND SOLUTION AT ITERATION {}: {}'.format(len(solutions),total_sols[n-1],i,c2.state)
								print(out)
								print(' Time Elapsed: {}\n'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
								log_.write(out + '\n')
								#log_.flush()


						# add our variables
						total_states += 2
						i += 1
						spinner.next() # moved this guy here
					# now see if the child is a solution
					gen_size = len(population)
					gen += 1
					

				# after finding solutions write them to a file
				with open('logs/solutions.txt', 'w') as file:
					for sol in solutions:
						file.write('{}\n'.format(sol))
					file.close()

				log_.write('DONE\n')
				#state_log.write('DONE\n')
				print('DONE!')
				elapsed_time = time.time() - start_time
				print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
				log_.write('Time Elapsed: {}\n'.format(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
				log_.write('Total Iterations {}\n'.format(i))
				log_.close()

			# garbage collection help
			del solutions
			del population
		except KeyboardInterrupt as e:
			log_.write('KeyboardInterrupt\n')
			log_.close()

