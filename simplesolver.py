# Global variables are worst variables but I'm lazy
from math import floor
import random
fin = open("../1.in", "r")
v, e, p = map(int, fin.readline().split())
# precompute modular inverses
inverses = [None] + [pow(i, p-2, p) for i in xrange(1, p)]
equations = [map(int, fin.readline().split()) for _ in xrange(e)]

# index i matches to equation indices that include it
includes = [ [] for _ in xrange(v) ]
for i, eqn in enumerate(equations):
    a,b,c,d,e = eqn
    includes[b].append(i)
    includes[d].append(i)
    
# initial state
state = [random.randint(0, p-1) for _ in xrange(v)]
    
def satisfies(eqn, assign):
    a, b, c, d, e = eqn
    return (a * assign[b] + c * assign[d] + e) % p == 0
    
# initial satisfied array
prev_equations = [satisfies(eqn, state) for eqn in equations]
changed_index = [0]
    
def energy(assign):
    # note that we want to minimize this!
    # rough test for now
    #
    # to make this run faster, this function has memory
    # only needs to update on the updated indices
    # uses global variables for this...I KNOW IT'S AWFUL
    for eqn_index in includes[changed_index[0]]:
        prev_equations[eqn_index] = satisfies(equations[eqn_index], assign)
    return -sum(prev_equations)
    
def local_max(state):
    # if local_max, return False
    # else, return an (index, value) pair. index is a random index to improve, value is what to set it to.
    indices = range(v)
    random.shuffle(indices)
    for index in indices:
        score = [0] * p # number equations satisfied with assignment to index
        original_val = state[index]
        for eqn_ind in includes[index]:
            a, b, c, d, e = equations[eqn_ind]
            if index == b:
                satisfies = (-inverses[a] * (c * state[d] + e)) % p
            else:
                # index == d
                satisfies = (-inverses[c] * (a * state[b] + e)) % p
            score[satisfies] += 1
        best_val, best_score = max(enumerate(score), key=lambda x: x[1])
        # compare best score to initial value. if 0, then this is a local max for this variable
        if best_score - score[original_val] > 0:
            return index, best_val
    return False
    
def assign_with_given(state, index):
    # assign every other variable to satisfy most with this value for index
    # ignore any equation that does not include index
    scores = [ [0]*p for _ in xrange(v)]
    for eqn_ind in includes[index]:
        a, b, c, d, e = equations[eqn_ind]
        if index == b:
            satisfies = (-inverses[a] * (c * state[d] + e)) % p
            scores[d][satisfies] += 1
        else:
            # index == d
            satisfies = (-inverses[c] * (a * state[b] + e)) % p
            scores[b][satisfies] += 1
    for i in xrange(v):
        if i == index:
            continue
        # there will be ties. Choose randomly
        best_score = max(scores[i])
        choices = [(value,score) for value,score in enumerate(scores[i]) if score == best_score]
        state[i] = random.choice(choices)[0]
 
def move(state):
    # change one variable to something else
    ind = random.randint(0, v-1)
    changed_index[0] = ind
    state[ind] = random.randint(0, p-1)    

from anneal import Annealer
annealer = Annealer(energy, move)
state, e = annealer.anneal(state, 100, 0.001, 
                            500000, updates=6)
print sum(satisfies(eqn, state) for eqn in equations)  # the "final" score