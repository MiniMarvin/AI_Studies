import os

for i in range(1, 4):
	for j in range(1, 11):
		if j == 2 or j == 4 or j == 6:
			continue
		os.system("pypy run_search.py -p " + str(i) + " -s " +str(j))