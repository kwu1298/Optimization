# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 18:17:55 2020

@author: kevin
"""

import pulp 

#Inititate Optimization Problem
mlip=pulp.LpProblem("Recylcing Problem", pulp.LpMaximize)

# of acres
total_acres=145

# of material 
M = 4

# of Scenarios
S = 7

#Declaring Decision Variables
x={} 
y={}
#Declaring lists of data and probability 
z=[[1,20,20,50],
   [3,18,25,60],
   [5,16,30,70],
   [7,14,35,80],
   [9,12,40,90],
   [6,10,45,100],
   [4,8,50,110]
   ]

prob=[0.05,0.15,0.1,0.25,0.3,0.1,0.05]

#Initiatng decision variables 
for m in range(M):
    x[m]= pulp.LpVariable("Capacity dedicated to processing material %s" %m, lowBound = 0, cat = "Integer")
    for s in range (S):
        y[s,m]= pulp.LpVariable("# of material sold of processing material %s in scenario %s" %(m,s), lowBound = 0, cat = "Integer")

#Demand constraints
for m in range (M):
    for s in range (S):
        mlip+=y[s,m]<=x[m]
        mlip+=y[s,m]<=z[s][m]


#Objective Function

mlip += pulp.lpSum(prob[i]*(750000*y[i,0]+400000*y[i,1]+150000*y[i,2]+50000*y[i,3]) for i in range (S))

#constraints

        
mlip += x[2]>=0.15*(x[0]+x[1]+x[3]+x[2])
mlip += x[3]>=0.2*(x[0]+x[1]+x[2]+x[3])
mlip += (x[2]+x[1])>=(2*x[0])
mlip += x[0]*5+x[1]*3+x[2]*2+x[3]*1<=total_acres

mlip.solve()

#Display variable values
for variable in mlip.variables():
    print ("{} = {}".format(variable.name, variable.varValue))

print(pulp.LpStatus[mlip.status])
print(pulp.value(mlip.objective))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        