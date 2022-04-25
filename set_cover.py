import sys
import numpy as np
import scipy.optimize as spo
import random

def randomized_rounding(A, x_opt, n_clms, n_rows):
    s = set([])
    
    x_round = np.zeros(n_rows, dtype='int')
    
    x = list(zip(x_opt, np.arange(n_rows)))
    x.sort(reverse=True)
    
    while (len(s) < n_clms):
        for row in x:
            if x_round[row[1]] == 0:
                if np.random.uniform() <= row[1]:
                    x_round[row[1]] = 1
                    for j in range(0, n_clms):
                        if (A[row[1]][j] == 1):
                            s.add(j)
                            if (len(s) == n_clms):
                                return x_round
                    
    return x_round

row_id = -1
weights = np.array([], dtype='int')
A = np.array([], dtype='int')
n_clms = 1
n_rows = 1

for line in sys.stdin:
    l = line.rstrip('\n').split()
    if row_id == -1:
        n_clms = int(l[0])
        n_rows = int(l[1])
        A = np.zeros((n_rows, n_clms), dtype='int')
    else:
        weights = np.append(weights, int(l[0]))
        for i in range(1, len(l)):
            clm_id = int(l[i])
            A[row_id][clm_id] = 1
    row_id += 1

b = np.ones(n_clms, dtype='int').T

res = spo.linprog(weights.T, A_ub=-A.T, b_ub=-b, bounds=(0,1))
x_opt = res.x

number_of_rounding = 10000
min_cost = np.sum(weights)
answer = np.ones(n_clms, dtype='int')
for i in range(number_of_rounding):
    x_rounding = randomized_rounding(A, x_opt, n_clms, n_rows)
    cost = np.sum(weights * x_rounding)
    if(min_cost > cost):
        min_cost = cost
        answer = x_rounding
        

        
for r in range(len(answer)):
    if answer[r] == 1:
        print(r+1, end=" ")
