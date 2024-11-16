import gurobipy as gp
from gurobipy import GRB
import numpy as np

n = 10
UB = n
c = 10
w = [1, 2, 3, 4, 5, 1, 3, 3, 4, 2] 

model = gp.Model ()
x = model.addVars(n, UB, vtype=GRB.BINARY)
y = model.addVars (UB, vtype=GRB.BINARY)

# minimize the number of bins used
model.setObjective(gp.quicksum(y[j] for j in range(UB) ), GRB.MINIMIZE)

# pack each item in exactly one bin
model.addConstrs(gp.quicksum(x[i,j] for j in range(UB)) == 1 for i in range(n))

# bin capacity constraint
model.addConstrs(gp.quicksum(w[i] * x[i,j] for i in range(n)) <= c * y[j] for j in range (UB))

# solve
model.optimize()

bin_for_item = [-1 for i in range(n)]

for i in range(n):
    for j in range(UB):
        if x[i,j].X > 0.5:
            bin_for_item[i] = j

print(f"n bins = {model. ObjVal}")
print(f"Bin assignment for each item: {bin_for_item}")