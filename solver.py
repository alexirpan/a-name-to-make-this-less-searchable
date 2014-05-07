# Global variables are worst variables but I'm lazy
from math import floor
import random

def satisfies(eqn, assign):
    a, b, c, d, e = eqn
    return (a * assign[b] + c * assign[d] + e) % p == 0
    
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
        best_score = max(score)
        best_val, best_score = random.choice(filter(lambda x: x[1] == best_score, enumerate(score)))
        # compare best score to initial value. if 0, then this is a local max for this variable
        if best_score - score[original_val] > 0:
            return index, best_val
    return indices[:v//2]
    
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
        best_val, best_score = max(enumerate(scores[i]), key=lambda x: x[1])
        state[i] = best_val
    
def move(state):
    # to get proper annealing, need to incorporate a way to get past local maxima...
    # let's try a semi-hill climbing strategy...
    # while you are not a local max, move upwards
    # when you are a local max, randomly change one variable
    # (the change is uniform across all values)
    # problem: most likely, it will just change that index back...
    # will not change back if other variables are now no longer local max?
    val = local_max(state)
    if type(val) is tuple:
        # not a local max
        index, value = val
        changed_index[0] = index
        state[index] = value
    else:
        # is a local max
        # to get away from this, you have to change pretty radically, so...
        # randomly change half the indices
        for index in val:
            state[index] = random.randint(0, p-1)
        # we now have to reset this array
        for i in xrange(e):
            prev_equations[i] = satisfies(equations[i], state)

from anneal import Annealer
annealer = Annealer(energy, move)

for file in range(1,21):
    fin = open("../%d.in" % file, "r")
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
    # initial satisfied array
    prev_equations = [satisfies(eqn, state) for eqn in equations]
    changed_index = [0]
    state, e = annealer.anneal(state, 100, 100, 
                                350000, updates=6)
    print sum(satisfies(eqn, state) for eqn in equations)  # the "final" score