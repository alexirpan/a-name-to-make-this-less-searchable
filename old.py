# Global variables are worst variables but I'm lazy
import time
import random

def satisfies(eqn, assign):
    a, b, c, d, e = eqn
    return (a * assign[b] + c * assign[d] + e) % p == 0
    
plateau = [0]
    
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
            plateau[0] = 0
            return index, best_val, best_score - score[original_val]
        # A magic, tweakable constant
        elif plateau[0] < 350 and best_val != original_val:
            plateau[0] += 1
            return index, best_val, 0
    return indices[:v//2]
    
def move(state, prev_energy):
    # moves the state, returns the index and old value in case it has to roll back
    # In a reset, returns -1, -1
    # (avoids copying entire list this way)
    val = local_max(state)
    if type(val) is tuple:
        # not a local max
        index, value, diff = val
        index, value, diff = val
        state[index] = value
        prev_energy[0] += diff
    else:
        # is a local max
        # to get away from this, you have to change pretty radically, so...
        # randomly change half the indices
        for index in val:
            state[index] = random.randint(0, p-1)
        prev_energy[0] = sum(satisfies(eqn, state) for eqn in equations)  
        
for file in range(1,2):
    t = time.time()
    count = 0
    #print "Input %d" % file
    fin = open("official_input_files/20.in", "r")
    v, e, p = map(int, fin.readline().split())
    # precompute modular inverses
    inverses = [None] + [pow(i, p-2, p) for i in xrange(1, p)]
    equations = [map(int, fin.readline().split()) for _ in xrange(e)]
    fin.close()
    # index i matches to equation indices that include it
    includes = [ [] for _ in xrange(v) ]
    for i, eqn in enumerate(equations):
        a,b,c,d,e = eqn
        includes[b].append(i)
        includes[d].append(i)
        
    # initial state
    state = [random.randint(0, p-1) for _ in xrange(v)]
    prev_energy = [sum(satisfies(eqn, state) for eqn in equations)]
    best_state = None
    best_ener = 0
    while time.time() - t < 360:
        count += 1
        move(state, prev_energy)
        if prev_energy[0] > best_ener:
            best_state = list(state)
            best_ener = prev_energy[0]
            print " ".join(map(str, best_state))
            print "Satisfies %d" % best_ener
            print "%d iterations" % count
            print "%f seconds" % (time.time() - t)
