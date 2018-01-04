#!/usr/bin

"""
The functions
"""
#format and print the array
def beauty_print(total_eval):
	for i in range(0, 7):
		to_print = ""
		for j in range(0, 8):
			to_print += str(total_eval[i][j]) + "\t"
		print(to_print)

"""
Main script
"""
total_eval = [[0 for a in range(0, 8)] for b in range (0, 7)]

names = []

## Generate the file list
for i in range(1, 87):
	names += ["out_{}.txt".format(i)]

## Extract the data from file
for f_name in names:
	# print(f_name)
	fp = open(f_name)

	
	for i, line in enumerate(fp):
		if i >= 13 and i <= 19:
			# print(line)
			nums = [int(s) for s in line.split() if s.isdigit()]
			# print(nums)
			for x in range(1, 9):
				total_eval[i - 13][x - 1] += nums[x]
			pass
		elif i > 19:
			break

	# print()
	fp.close()

beauty_print(total_eval)

