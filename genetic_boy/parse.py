# solution parser
solution_lines = []
start = 'output.txt'
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

