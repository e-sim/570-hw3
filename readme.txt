Erica Sim
HW3
Ling 570

Q3(b) I used a directed graph to store the input FST, with node and edge          objects.  However, were I to start it over, I think I would use a 2D array to build a transition table, as it would be more organized and potentially easier to debug.

The only change I made to the Viterbi algorithm to handle FSTs was to add a way of keeping track of the output string, which I would concatenate the output for the highest probability transition to the end of.
   