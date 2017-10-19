# Erica Sim
# Ling 570 Autumn 2017
# hw3
# This program reads/builds (w)FSTs and provides the most likely 
# path & output for a given input

import sys
import re
import collections

# stuff from last time

class Edge:

    def __init__(self, char, dest, weight, output):
        self.char = char
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
		return "name=" + self.name + " accept=" + str(self.accept)\
				+ " (" + str(self.adjacents) + ")"

	def set_accept(self):
		self.accept = True

class TrelSquare:

    def __init__(self, prob, prev_state, out_str, state_node, step):
        self.prob = prob
        self.prev_state = prev_state
        self.out_str = out_str
        self.state = state_node
        self.step = step

    def find_prob(self, dest_node, curr_char):
        #the probability of going to the destination node/state from this one
        prob = 0
        new_out = ""
        for edge in self.state.adjacents:
            if edge.dest = dest_node.name and edge.char = curr_char:
                prob = self.prob * edge.weight
                new_out = edge.output
                break
        return (prob, new_out)




#### debug print
DEBUGGING = False
def debugPrint(text):
	if (DEBUGGING):
		print(text)
		sys.stdout.flush()

#### main program starts

debugPrint("START PROGRAM")


fst_file = open(sys.argv[1], "r")
node_dict = collections.OrderedDict()

for line in fst_file:

#regex for each line of fsa file
	FSA_ACCEPT_REGEX_PATTERN = re.compile(r"(\w+)$")
	FSA_EDGE_REGEX_PATTERN = re.compile(r"\((\w+) \((\w+) \
        \"(\w*)\" \"(\w*)\" (\d(\.\d+)?)\)\)")
	accept_match = FSA_ACCEPT_REGEX_PATTERN.match(line.strip())


    if accept_match:
		acc_state = accept_match.group(1)

    else:
        edge_match = FSA_EDGE_REGEX_PATTERN.match(line)
        curr = edge_match.group(1)
        next_node_code = edge_match.group(2)
        in_char = edge_match.group(3)
        out_char = edge_match.group(4)
 
        if edge_match.group(5):
            weight = edge_match.group(5)
        else:
            weight = 1

		if curr not in node_dict:

			new_node = Node(curr)
			node_dict[curr] = new_node
			debugPrint("made " + str(new_node))

			if acc_state is curr:
				new_node.set_accept()


		new_edge = Edge(in_char, next_node_code, weight, out_char)
		node_dict[curr].adjacents.append(new_edge)

		debugPrint("adjacents are  " + str(node_dict[curr].adjacents))


fst_file.close()


# START NEW STUFF

infile = open(sys.argv[2], "r")

for line in infile:

	orig_line = line.strip("\n")
	line = line.translate(None, '" ')
    length_line = len(line)
    #num_states = len(node_dict.keys())
    dummy = Node("start")
    #trellis = [(node_dict[i]) = [] for i in node_dict.keys()]
    # makes an array of arrays named after the different states/nodes
    trellis = [i = [] for i in node_dict.keys()]

    #first fill in the trellis 
    # while weight != 0?? <-- goes somewhere

    curr_node = node_dict.keys().next()
    curr_char = line[0]
    out_str = ""
    step = 0

    # first one:
    trellis [0][0]: TrelSquare(1, dummy, "", curr_node, step)
    step += 1

    #trelsquare has prob, prevnode, outstr, destnode, step
 
    # the edges all have inchar, next node, weight, outchar, + a name 
    # so, for each adjacent edge that has the right character (each edge in legal moves)
    # prob = max (prev prob * edge prob)
    # ^^prev prob = look in array named for curr node, #step -1 (?), get [0] in tuple
    
    # go to the array named next node, #step cell
    # prev node = curr node
    # out_str = out_str + output
    # prob = prob

    # prob = self.find_prob[0]
    # newout = self.find_prob[1]

    #loop through steps/chars of line/columns in trellis (all ~equiv)
    while step < len(line):

        list = [array[step] for array in trellis]
        max_prob = 0
        max_owner = None

        #loop through squares in curr column & fill out
        for square in list:


            prev_col = [array[step-1] for array in trellis]
            for origin in prev_col:
                curr_prob = square.find_prob(curr_node, curr_char)
                if curr_prob > max_prob:
                    max_prob = curr_prob
                    max_owner = curr_node



        step += 1
        


    # note for later: %g makes human readable number format string = "%g" % prob

infile.close()