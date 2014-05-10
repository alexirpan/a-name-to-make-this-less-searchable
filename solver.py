# Global variables are worst variables but I'm lazy
import time
import random

# according to PyPy docs, this object makes the class new-style
# and new-style are faster classes
class HillClimber(object):
    def __init__(self, fin_name, fout_name, seed=None, time_limit=1080):
        fin = open(fin_name, "r")
        v, e, p = map(int, fin.readline().split())
        self.v = v
        self.e = e
        self.p = p
        self.time_limit = time_limit
         # precompute modular inverses
        self.inverses = [None] + [pow(i, p-2, p) for i in xrange(1, p)]
        self.equations = [map(int, fin.readline().split()) for _ in xrange(e)]
        self.prev_energy = 0
        self.plateau = 0
        # index i matches to equation indices that include it
        self.includes = [ [] for _ in xrange(v) ]
        for i, eqn in enumerate(self.equations):
            a,b,c,d,e = eqn
            self.includes[b].append(i)
            self.includes[d].append(i)
        fin.close()
        self.fout_name = fout_name
        self.seed = seed
            
    def satisfies(self, eqn, assign):
        a, b, c, d, e = eqn
        return (a * assign[b] + c * assign[d] + e) % self.p == 0
    
    def local_max(self, state):
        # if local_max, return False
        # else, return an (index, value) pair. index is a random index to improve, value is what to set it to.
        v = self.v
        p = self.p
        indices = range(v)
        random.shuffle(indices)
        for index in indices:
            score = [0] * p # number equations satisfied with assignment to index
            original_val = state[index]
            for eqn_ind in self.includes[index]:
                a, b, c, d, e = self.equations[eqn_ind]
                if index == b:
                    satisfies = (-self.inverses[a] * (c * state[d] + e)) % p
                else:
                    # index == d
                    satisfies = (-self.inverses[c] * (a * state[b] + e)) % p
                score[satisfies] += 1
            best_score = max(score)
            best_val, best_score = random.choice(filter(lambda x: x[1] == best_score, enumerate(score)))
            # compare best score to initial value. if 0, then this is a local max for this variable
            d_score = best_score - score[original_val]
            if d_score > 0:
                self.plateau = 0
                self.prev_energy += d_score
                return index, best_val
            # A magic, tweakable constant
            # larger = more time wasted travelling around, but more likely to find a better solution
            # on 2.in, in a 2 minute run there is almost always one time where improvement took > 300 iterations
            # and usually there is only one
            # too lazy to actually statistically analyze it
            elif self.plateau < 10000 and best_val != original_val:
                self.plateau += 1
                return index, best_val
        return indices[:v//2]
    
    def move(self, state):
        # moves the state, returns the index and old value in case it has to roll back
        # In a reset, returns -1, -1
        # (avoids copying entire list this way)
        val = self.local_max(state)
        if type(val) is tuple:
            # not a local max
            index, value = val
            state[index] = value
        else:
            return False
            # is a local max
            # to get away from this, you have to change pretty radically, so...
            # randomly change half the indices
            for index in val:
                state[index] = random.randint(0, self.p-1)
            self.plateau = 0
            self.prev_energy = sum(self.satisfies(eqn, state) for eqn in self.equations)

    # not used yet
    def run(self):
        fout = open(self.fout_name, "w")
        t = time.time()
        count = 0
        # initial state
        if self.seed:
            state = self.seed
        else:
            state = [random.randint(0, self.p-1) for _ in xrange(self.v)]
        best_state = None
        best_ener = 0
        self.prev_energy = sum(self.satisfies(eqn, state) for eqn in self.equations)
        while time.time() - t < self.time_limit:
            count += 1
            success = self.move(state)
            if self.prev_energy > best_ener:
                best_state = list(state)
                best_ener = self.prev_energy
                print >> fout, " ".join(map(str, best_state))
                print >> fout, "Satisfies %d" % best_ener
                print >> fout, "%d iterations" % count
                print >> fout, "%f seconds" % (time.time() - t)
            if not success:
                break
        fout.close()
        
from multiprocessing import Process
# Windows requires a standalone function, can't use bound or unbound version
def spawn(climber):
    climber.run()
# Stupid Windows, makes the name == main needed as well

if __name__ == '__main__':
    NUM_CORES = 4
    # 11.0 files
    important = range(1,31)
    with open("official_input_files/solutions.txt") as f:
        seeds = [map(int, line.strip().split()) for line in f]
    for file in important:
        print "Input %d" % file
        climbers = [HillClimber("official_input_files/%d.in" % file, "%d-%d.out"% (file, i), seed=seeds[file], time_limit=300) for i in range(NUM_CORES)]
        processes = [Process(target=spawn, args=(climber,)) for climber in climbers]

        for proc in processes:
            proc.start()
            
        for proc in processes:
            proc.join()