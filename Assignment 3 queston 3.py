# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 15:44:24 2020

@author: kevin
"""
import pulp
model = pulp.LpProblem("Preschool Problem", pulp.LpMinimize)

#Initialize variables
x=pulp.LpVariable(name = "# of Full Time Employees Hired", lowBound = 0, cat = "Integer")
y={}
z={}
b={}
c={}
d={}
e={}
S = 10
A = 2
for s in range (S):
    y[s]=pulp.LpVariable("# of WeCare Agency Part-time Employees hired in Scenario %s" %s, lowBound = 0, cat = "Integer")
    z[s]=pulp.LpVariable("# of EduServices Part-time Employees hired in Scenario %s" %s, lowBound = 0, cat = "Integer")
    b[s]=pulp.LpVariable("# of WeCare Agency Part-time Employees hired in Scenario %s when group savings" %s, lowBound = 0, cat = "Integer")
    c[s]=pulp.LpVariable("# of EduServices Part-time Employees hired in Scenario %s when group savings" %s, lowBound = 0, cat = "Integer")
    for a in range (A):
        d[s,a]=pulp.LpVariable("Part time hired in Scenario %s from agency %s" %(s,a), cat = "Binary")
        e[s,a]=pulp.LpVariable("Part Time hired in Scenario %s from agency %s group discount" %(s,a), cat = "Binary")

scenario = [
    [0.1, 4],
    [0.15, 4],
    [0.1, 5],
    [0.05, 6],
    [0.2, 6],
    [0.15, 7],
    [0.05, 7],
    [0.1, 8],
    [0.05, 9],
    [0.05, 9]
    ]


    

#Objective function
model+=25000*x+pulp.lpSum(scenario[s][0]*((32000*y[s]-3000*b[s])+(30000*z[s]-4000*c[s])) for s in range (S)), "Profit"                      


#constraints
for s in range (S):
    model += x + y[s]+z[s]>=scenario[s][1], "Demand constraint %s" %s
    model += d[s,0]+d[s,1]<=1, "Either or agency %s" %s
#Big m constraint
    model += y[s]<=9*d[s,0], "Big M Constraint x %s" %s
    model += z[s]<=9*d[s,1], "Big M Constraint z %s"%s
    model += z[s]>=2*d[s,1]
#Discount constraints
    model += b[s]<=9*e[s,0]
    model += c[s]<=9*e[s,1]
    model += 4*e[s,0]<=y[s]
    model += 6*e[s,1]<=z[s]
    model += b[s]<=y[s]
    model += c[s]<=z[s]
    
#Solve our model
model.solve()

#Display variable values
for variable in model.variables():
    print ("{} = {}".format(variable.name, variable.varValue))

print()
print(pulp.LpStatus[model.status])
print(pulp.value(model.objective))
