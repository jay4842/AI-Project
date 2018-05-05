from glob import glob
import datetime
import time
# solution parser
def parse_solutions(file='output.txt'):
	solution_lines = []
	start = file
	with open(start,'r') as file:
		for line in file:
			line = line.replace('\n','')
			if('FOUND' in line):
				line = line.split(':')[-1][1:]
				print(line)
				solution_lines.append(line)

	with open('solutions.txt','w') as file:
		for line in solution_lines:
			file.write(line + '\n')


def parse_log(log_file):
	lines = []
	with open(log_file,'r') as file:
		for line in file:
			lines.append(line.replace('\n',''))

		file.close()

	# now go though and get total iterations
	# time spent
	# iteration of the last solution too
	total_its  = lines[-1].split(' ')[-1]
	total_time = lines[len(lines)-2].split(' ')[-1]
	#print(lines[len(lines)-4].split(' '))
	#input('->')
	last_it    = lines[len(lines)-4].split(' ')[5].replace(':','')

	return total_its, total_time, last_it

if __name__ == '__main__':

	three_logs = glob('logs/three_*/')
	norm_logs  = glob('logs/n_*/')

	print(three_logs)
	print(norm_logs)

	with open('parse_out.txt','w') as boy:
		for folder in three_logs:
			files = glob(folder+'*.txt')
			print(folder[13] + ' pop = ' + folder[15:len(folder)-1])
			print(folder)
			try:
				over_all_its = 0
				last_its = 0
				for file in files:
					total_its, total_time, last_it = parse_log(file)
					over_all_its += int(total_its)
					last_its += int(last_it)

				# cal averages
				over_all_its = over_all_its / len(files)
				last_its = last_its / len(files)
				print(over_all_its)
				print(last_its)
				boy.write('Three way crossover\n')
				boy.write('N = {}  POP = {}\n'.format(folder[13],folder[15:len(folder)-1]))
				boy.write('Over_all = {}\n'.format(over_all_its))
				boy.write('last_its = {}\n'.format(last_its))
				boy.write('-----------------------\n')
			except Exception as e:
				print(e)

		boy.write('/ / / / / / / / / / / / / / / / / / / / / / / / /\n')
		for folder in norm_logs:
			files = glob(folder+'*.txt')
			print(folder[7] + ' pop = ' + folder[9:len(folder)-1])
			print(folder)
			try:
				over_all_its = 0
				last_its = 0
				for file in files:
					total_its, total_time, last_it = parse_log(file)
					over_all_its += int(total_its)
					last_its += int(last_it)

				# cal averages
				over_all_its = over_all_its / len(files)
				last_its = last_its / len(files)
				print(over_all_its)
				print(last_its)
				boy.write('One point crossover\n')
				boy.write('N = {}  POP = {}\n'.format(folder[7],folder[9:len(folder)-1]))
				boy.write('Over_all = {}\n'.format(over_all_its))
				boy.write('last_its = {}\n'.format(last_its))
				boy.write('-----------------------\n')
			except Exception as e:
				print(e)



