# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 12:20:54 2020

@author: kevin
"""

import pulp as pulp

#the # of models
M = 3

#the # of quarters
Q = 4

#defining demand and capacity list
demand = [
    [2000, 6500, 5500, 6000],   #basic
    [1500,3000,8000,5000], #fishing
    [50,150,150,200] #Burges
    ]

capacity = [
    [3000,8000,8000,3000],
    [10000,8000,6000,4000],
    [150,160,170,180] 
    ]


#Initiate distribution problem
milp =pulp.LpProblem("Question1", pulp.LpMinimize)

#Defining Decision Variables 
x={}
y={}
devPlus = {}
devMinus = {}

#Define x as product m produced in quarter q and y as product m stored in quarter q
for m in range (M):
    for q in range (Q):  
        x[m,q]=pulp.LpVariable(name = "x(%s, %s)" %(m,q), lowBound = 0, cat = "Integer")
        y[m,q]=pulp.LpVariable(name = "y(%s, %s)" %(m,q), lowBound = 0, cat = "Integer")
        devMinus[m,q] = pulp.LpVariable("Product %s in Scenario %s Under" %(m,q), lowBound = 0, cat = "Continuous")
        devPlus[m,q] = pulp.LpVariable("Product %s in Scenario %s Over" %(m,q), lowBound = 0, cat = "Continuous")

#Initiate storage with zero starting off
for m in range (M):
    y[m,0]=0
# Add the objective function to the optimization problem 
#milp += pulp.lpSum([np.abs(x[m,q]-x[m,q+1]) for m in range (M) for q in range (Q-1)]), "Differences_in_production"
milp+=pulp.lpSum(devPlus[i,j] + devMinus[i,j] for i in range (M) for j in range (Q-1))

# Add production constraint
for q in range (Q):
    milp += x[0, q]+ 2*x[1, q]+ 3*[2, q]<=16000

# Add capacity constraints
for m in range (M):
    for q in range (Q):
        milp += x[m,q]<=capacity[m][q]

# Add demand constraints
for m in range (M):
    for q in range (Q):
        milp += x[m,q] + y[m,q]>=demand[m][q]

# Add empty capacity constraints
for m in range (M):
    milp += x[m,3] + y[m,3] - demand[m][3]==0

for m in range (M):
    for q in range (Q-1):
        milp += x[m,q]+devPlus[m,q]-devMinus[m,q]==x[m,q+1]
# Add demand constraints
for m in range (M):
    for q in range (Q-1):
        milp += x[m,q] + y[m,q] - demand[m][q]==y[m,q+1]    

# The problem is solved using PuLP's linear solver
milp.solve()

# The status of the solution is printed to the screen
print("PuLP Solver Status:", pulp.LpStatus[milp.status])

# The optimized objective function value is printed to the screen    
print("Total Difference between quarters = ", pulp.value(milp.objective))
#Display variable values
for variable in milp.variables():
    print ("{} = {}".format(variable.name, variable.varValue))



