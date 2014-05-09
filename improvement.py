"""Solves the problem with iterative improvement.

Uses a modular inverse function from
https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python.
"""

import random
from modmath import Mod

in_file = 'question.in'
solution_file = 'solution.out'

def normalize(equation):
    """Changes an equation from the form a*xb + c*xd + e = 0
    to xa + b*xc = d, with a < c.
    """
    a, b, c, d, e = equation
    if b > d:
        a, b, c, d = c, d, a, b
    a, c, e = 1, Mod.mod_div(c, a), Mod.mod_div(e, a)
    e = Mod.mod(-e)
    return (b, c, d, e)

def solve_for_other(equation, v, assignment):
    """Solve for vertex V in EQUATION given ASSIGNMENT.

    Return value, the desired value for V.
    """
    v1, a, v2, c = equation
    if v == v1:
        return solve_for(equation, v2, assignment[v2])[1]
    else:
        return solve_for(equation, v1, assignment[v1])[1]

def solve_for(equation, v, value):
    """Given that vertex V is assigned VALUE, solve for
    the other vertex in EQUATION.

    Return (other, other_value) where OTHER is the index
    of the other vertex, and OTHER_VALUE is its value.
    """
    v1, a, v2, c = equation
    if v == v1:
        return v2, Mod.mod_div(c - value, a)
    else:
        return v1, Mod.mod(c - a*value)

def current_satisfied(v, equations, assignment):
    """Return the number of satisfied equations that involve
    variable V.
    """
    satisfied = 0
    for equation in equations[v]:
        v1, a, v2, c = equation
        if (assignment[v1] + a * assignment[v2]) % Mod.P == c:
            satisfied += 1
    return satisfied

def judge(assignment, equations):
    satisfied = 0
    for equation in equations:
        v1, a, v2, c = equation
        if (assignment[v1] + a * assignment[v2]) % Mod.P == c:
            satisfied += 1
    return satisfied

def improve(assignment):
    """Iteratively change the values of variables until no more
    improvement can be made.
    """
    while True:
        changed = False
        for v in range(V):
            if len(equations[v]) == 0:
                continue

            #Dict from value => satisfied equations
            candidate_values = {}
            for equation in equations[v]:
                val = solve_for_other(equation, v, assignment)
                if val not in candidate_values:
                    candidate_values[val] = 0
                candidate_values[val] += 1

            #Find best value
            if assignment[v] not in candidate_values:
                old_sat = 0
            else:
                old_sat = candidate_values[assignment[v]]
            values = candidate_values.items()
            values.sort(key = lambda kv: -kv[1])
            best_value, best_sat = values[0]

            if best_sat > old_sat:
                assignment[v] = best_value
                changed = True

        if not changed:
            break
    return assignment

def make_disjoint(n):
    return [-1] * n
    
def find(s, i):
    if s[i] < 0:
        return i
    s[i] = find(s, s[i])
    return s[i]
    
def union(s, i, j):
    r1, r2 = find(s, i), find(s, j)
    if r1 == r2:
        return
    if s[r1] < s[r2]:
        s[r2] += s[r1]
        s[r1] = r2
    else:
        s[r1] += s[r2]
        s[r2] = r1
    
def only_one(s):
    return -len(s) in s
    
#Read input
with open(in_file) as f:
    #Number of vertices, equations, and prime
    V, E, P = [int(x) for x in f.readline().split()]
    Mod.P = P
    Mod.calculate_inverses()
    #List of relevant equations for every variable
    equations = [list() for _ in range(V)]
    all_equations = []
    #Process each equation
    tree = make_disjoint(V)
    tree_done = False
    for line in f:
        equation = [int(x) for x in line.split()]
        equation = normalize(equation)
        v1, b, v2, d = equation
        all_equations.append(equation)
        if not tree_done and find(tree, v1) != find(tree, v2):
            equations[v1].append(equation)
            equations[v2].append(equation)
            union(tree, v1, v2)
            if only_one(tree):
                tree_done = True

def solve_tree():
    best_assignment, best_value = None, -1
    for start_val in xrange(P):
        assign = [-1] * V
        assign[0] = start_val
        visited = set()
        to_check = set()
        to_check.add(0)
        while to_check:
            i = to_check.pop()
            if i in visited:
                continue
            visited.add(i)
            for eqn in equations[i]:
                if assign[i] == -1:
                    assert False, "What the fuck"
                v, value = solve_for(eqn, i, assign[i])
                if v not in visited:
                    assign[v] = value
                    to_check.add(v)
        value = judge(assign, all_equations)
        if value > best_value:
            best_assignment, best_value = assign[:], value
    with open(solution_file, 'w') as f:
        f.write(' '.join([str(x) for x in best_assignment]))
        
solve_tree()
exit()
                
#Pick random vertex to start
start = 0#random.randrange(V) #Fixme: Pick vertex with largest degree
best_assignment, best_value = None, -1
#Try all start values
for start_value in xrange(P):
    assignment = [0] * V
    assignment[start] = start_value
    #Expand
    for equation in equations[start]:
        v, value = solve_for(equation, start, start_value)
        assignment[v] = value #Fixme: Handle contradictory edges
    #Iterative improvement
    assignment = improve(assignment)
    value = judge(assignment, all_equations)
    #Check quality
    if value > best_value:
        best_value = value
        best_assignment = assignment
        print "Value %s with %s = %s" % (value, start, start_value)

#Load assignment
#with open(solution_file) as f:
#    assignment = [int(x) for x in f.readline().split()]
#best_assignment = improve(assignment)
#print judge(best_assignment, all_equations)

with open(solution_file, 'w') as f:
    f.write(' '.join([str(x) for x in best_assignment]))
