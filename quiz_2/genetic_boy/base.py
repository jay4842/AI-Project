# This will include our base code for setting up the project.
import random as r


# this will generate a state of n queens
def generate_state(n=8):
	# Start with 8 as the normal
	space = [0 for i in range(0,n)]

	# now populate the state randomly
	#  space at i can be from 0 to n
	for i in range(0,n):
		space[i] = r.randint(0,n)
	return space
# thats it nothing special

# setup the fitness function
def cal_fitness(space):
	n = len(space)
	print(n)
	# make a tempory array to hold the state, making evaluating easy
	temp_space = [[0 for i in range(0,n)] for i in range(0,n)]
	#print(temp_space)
	for x in range(n):
				

	line = ''
	for i in range(0,n):
		for j in range(0,n):
			line += str(temp_space[i][j]) + ' '
		print(line)
		line = ''


if __name__ == '__main__':
	space = generate_state()
	print(space)
	fit = cal_fitness(space)
