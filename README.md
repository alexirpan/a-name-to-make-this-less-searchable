The main strategy behind this is hill climbing.

The hill climber works by starting from a random assignment. It randomly iterates through all variables.
At the first variable found such that changing that variables increases the score, it changes that variable to maximize score gain.
If the variable can be changed to a different value while keeping the same score, it does so. This allows the high climber to travel on plateaus
To avoid infinite plateau loops, the climber is allowed to not increase score up to 350 times. Then, it must either improve score or restart.
At a restart, half the indices are chosen, and reset to random values.

This repeats on many threads, for many iterations.

There are also some meta-strategies. One file processes equations until the equations have connected all variables into a tree
(if you think of variables = vertices, equations = edges)
A tree can be satisfied P ways, check all these ways and return the best.
If a team did not randomize the order of their equations, and placed the optimal solution at the top of their file,
this will find that optimal very quickly. This works surprisingly well.
We also ran this on the last equations, in case a team generated the optimal equations at the end.

Finally, there was some hand-done tweaking that involves seeding hill climbers/iterative improvers with good solutions
(usually ones found by the meta-strategy breaker above.) This allows for more optimization.