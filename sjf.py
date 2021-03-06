import sys
import numpy as np
from configManager import *

def disp(x, s):
	f.write("	"+s+ "\n")
	for i in range(count):
		f.write('		P' + str(i+1) + '\t' + str(x[i]) + "\n")

def fileRead(arriv, burst, number_processes):
	sigma_burst = ConfigManager.getStandardDeviationBurstTime()
	mu_arrival = ConfigManager.getAverageArribalTime()
	sigma_arrival = ConfigManager.getStandardDeviationArribalTime()
	number_processes = ConfigManager.getNumberOfProcessess()
	mu_burst = ConfigManager.getAverageBurstTime()
    
	i = 0
	for arrival_time in np.random.normal(mu_arrival, sigma_arrival, number_processes):
		arriv.append(int(arrival_time))
		i += 1
	
	i = 0
	for burst_time in np.random.normal(mu_burst, sigma_burst, number_processes):
		burst.append(int(burst_time))
		i += 1
	return number_processes		

def minIndex(l):
	if l >= arriv[count-1]: 
		return count-1 
	m = count - 1
	while True:
		if (l < arriv[m]):
			m -= 1
		else:
			break
	return m	

def minValue(cop, n):
	new = []
	for i in range(n+1):
		new.insert(i, cop[i])
	return min(new)
		
def cal():
	n = 0
	last = 1
	copy = []
	line = arriv[0]
	start.insert(0, arriv[0])

	for i in range(count):
		copy.insert(i, burst[i])
	line += copy[0]
	end.insert(0, line)
	copy[0] = 999999
	
	while True:
		n = minIndex(line)
		n = minValue(copy, n)
		index = copy.index(n)
		
		start.insert(index, line)
		line += burst[index]
		end.insert(index, line)
		copy[index] = 999999
		
		last += 1
		if last == count: 
			break	

def waiting(sum):
	sum = 0
	for i in range(count):
#		wait.insert(i, (turn[i] - burst[i]))
		wait.insert(i, (start[i] - arriv[i]))
		sum += wait[i]
	disp(wait, 'Waiting Time')
	return sum

def turnaround(sum):
	sum = 0
	for i in range(count):
		turn.insert(i, (end[i] - arriv[i]))
		sum += turn[i]
	disp(turn, 'Turnaround Time')
	return sum


f = open("results_SJF.txt", "w")
f.write("SJF Results\n")	
sum_tr_simulation = 0
sum_ts_simulation = 0

number_simulations = ConfigManager.getNumberSimulations()
for i in range(number_simulations):
	f.write("")
	f.write("Simulation " + str(i+1) +"\n")
	sum = 0
	line = 0
	count = 0
	end = []
	wait = []
	turn = []
	start = []
	arriv = []
	burst = []

	count = fileRead(arriv, burst, count)
	disp(arriv, 'Arrival Time')
	disp(burst, 'Burst Time')

	cal()

	disp(end, 'Completion Time')

	sum = turnaround(sum)
	avg = float(sum)/count
	avg_tr = avg
	f.write('	Average Turnaround Time : ' + str(avg_tr) + "\n")
	sum_tr_simulation += avg_tr

	sum = waiting(sum)
	avg = float(sum)/count
	avg_ts = avg
	f.write('	Average Waiting Time : ' + str(avg_ts) + "\n")
	sum_ts_simulation += avg_ts

	tpr = avg_tr/avg_ts
	f.write('	Average Retorn Time TR/TS : ' + str(tpr) + "\n")

f.write("SJF TS Total Average  " + str(sum_ts_simulation/number_simulations) + "\n")
f.write("SJF TR Total Average  " + str(sum_tr_simulation/number_simulations) + "\n")
f.close()