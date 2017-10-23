# Erica Sim
# Ling 570 Autumn 2017
# hw3
'''This program reads/builds (w)FSTs and provides the most likely path & 
output for a given input
'''

import sys
import re
import collections


class Edge:

    def __init__(self, in_word, dest, weight, output):
        self.in_word = in_word
        self.dest = dest
        self.weight = weight
        self.output = output

class Node:

    def __init__(self, name):
        self.name = name
        self.adjacents = []
        self.accept = False

    #for testing
    def __repr__(self):
        return "name=" + self.name + " accept=" + str(self.accept)
               # + " (" + str(self.adjacents) + ")"

    def set_accept(self):
        self.accept = True

class TrelSquare:

    def __init__(self, prob, prev_state, out_str, state_node, step):
        debug_print(str(prob) + " " + str(state_node.name) if state_node else "Nothing")
        self.prob = prob
        self.prev_state = prev_state
        self.out_str = out_str
        self.state = state_node
        self.step = step

    def __repr__(self):
        state_name = "None" 
        prev_state = "None"       
        if self.state:
            state_name = self.state.name

        if self.prev_state:
            prev_state = self.prev_state.name
        
        return "|  SQUARE prob= " + str(self.prob) + " on step " + str(self.step) + " for state " + str(self.state.name) if self.state else "NONE" + " |"

    def find_prob(self, dest_node, curr_word):
        '''the probability of going to the destination node/state from this one'''
        prob = 0.0
        new_out = ""
        if self.prob == 0.0 or not self.state:
            return (0, "")
        
        for edge in self.state.adjacents:
            debug_print("\t\t\tedge word: " + edge.in_word + " current word: " + curr_word)
            debug_print("\t\t\tedge dest: " + edge.dest + " dest node: " + curr_word)
            if edge.dest == dest_node.name and edge.in_word == curr_word:
                new_prob = self.prob * float(edge.weight)
                debug_print("\t\t\tprob: " + str(self.prob) + " edge weight: " + str(edge.weight))
                if new_prob > prob:
                    new_out = edge.output
                    prob = new_prob
                    continue
        return (prob, new_out)

'''finds the maximum of all of the find_prob for the previous column (to current)'''
def find_max_prob(column, dest_node, curr_word):
    max_prob = 0.0
    max_owner = None
    output = ""
    for origin_sq in column:
        debug_print("\torigin sq is {0}".format(str(origin_sq)))
        prob_tup = origin_sq.find_prob(dest_node, curr_word)
        curr_prob = prob_tup[0]
        new_out = prob_tup[1]

        debug_print("\t\t" + str(prob_tup))
        if curr_prob > max_prob:
            max_prob = curr_prob
            max_owner = origin_sq.state
            if origin_sq.out_str: 
                output = origin_sq.out_str + " \"" + new_out + '"'
            else:
                output = '"' + new_out + '"'

    return (max_prob, max_owner, output)

'''for the very last one there aren't edges, so it needs a different find_prob method'''
def find_final_prob(final_column):
    final_prob = 0.0
    output = ""
    for square in final_column:
        if square.prob > final_prob and square.state.accept:
            final_prob = square.prob
            output = square.out_str
            max_owner = square.state

    return (final_prob, output)


#### debug print
DEBUGGING = False
def debug_print(text):
    if DEBUGGING:
        print(text)
        sys.stdout.flush()

#### main program starts

debug_print("START PROGRAM")


FST_FILE = open(sys.argv[1], "r")
node_dict = collections.OrderedDict()

for line in FST_FILE:
    line = line.rstrip()

    #regex for each line of fst file
    FST_ACCEPT_REGEX_PATTERN = re.compile(r"(\w+)$")
    FST_EDGE_REGEX_PATTERN = re.compile(r"\((\w+) \((\w+) \"(\w*)\" +\"(\w*)\" (\d(\.\d+))?\)\)")
    accept_match = FST_ACCEPT_REGEX_PATTERN.match(line)

    if accept_match:
        acc_state = accept_match.group(1)

    else:
        edge_match = FST_EDGE_REGEX_PATTERN.match(line)

        curr = edge_match.group(1)
        next_node_code = edge_match.group(2)
        in_word = edge_match.group(3)
        out_word = edge_match.group(4)

        if edge_match.group(5):
            weight = edge_match.group(5)
        else:
            weight = 1

        if curr not in node_dict:

            new_node = Node(curr)
            node_dict[curr] = new_node
            
            if acc_state == curr:
                new_node.set_accept()

            debug_print("made " + str(new_node))

        #turns out you gotta make sure all destination nodes are made too
        if next_node_code not in node_dict:

            new_node = Node(next_node_code)
            node_dict[next_node_code] = new_node
            
            if acc_state == next_node_code:
                new_node.set_accept()

            debug_print("made " + str(new_node))


        new_edge = Edge(in_word, next_node_code, weight, out_word)
        node_dict[curr].adjacents.append(new_edge)


FST_FILE.close()


# START NEW STUFF

INFILE = open(sys.argv[2], "r")

for line in INFILE:

    orig_line = line.strip("\n")
    line = line.translate(None, '"')
    inputs = line.split()
    dummy = Node("start")
    debug_print("length of dictionary: " + str(len(node_dict)))
    trellis = [[TrelSquare(0, dummy, "", None, -1) for x in range(len(inputs) + 1)] for i in range(len(node_dict))]

    curr_node = node_dict.values()[0]
    curr_word = inputs[0]
    out_str = ""
    step = 0

    # first one:
    trellis[0][step] = TrelSquare(1.0, dummy, "", curr_node, step)
    step += 1

    debug_print("inputs are: " + str(inputs).translate(None, ))
    debug_print("length of input: " + str(len(inputs)))

    #loop through steps/chars of line/columns in trellis (all ~equiv)
    for curr_word in inputs:

        j = 0
        while j < len(trellis):
            curr_node = node_dict.values()[j]
            debug_print("dictionary: " + str(node_dict))

            prev_col = []
            for x in trellis:
                prev_col.append(x[step-1])

            max_tup = find_max_prob(prev_col, curr_node, curr_word)
            debug_print(max_tup)
            max_prob = max_tup[0]
            max_owner = max_tup[1]
            out_so_far = max_tup[2]

            trellis[j][step] = TrelSquare(max_prob, max_owner, out_so_far,
                                          curr_node, step)
            #debug_print("TRELLIS: " + str(trellis))
            j += 1

        step += 1

    last_col = [array[len(inputs)] for array in trellis]
    (final_prob, output) = find_final_prob(last_col)
    if final_prob == 0.0:
        output = "*none*"

    prob_str = "%g" % final_prob
    print(orig_line + " => " + output + " " + prob_str)

    # note for later: %g makes human readable number format string = "%g" % prob

INFILE.close()
