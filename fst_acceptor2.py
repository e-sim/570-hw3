# Erica Sim
# Ling 570 Autumn 2017
# hw3
# This program reads/builds (w)FSTs and provides the most likely 
# path & output for a given input

import sys
import re

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


#### debug print
DEBUGGING = False
def debugPrint(text):
	if (DEBUGGING):
		print(text)
		sys.stdout.flush()

#### main program starts

debugPrint("START PROGRAM")


fst_file = open(sys.argv[1], "r")
node_dict = {}

for line in fst_file:

#regex for each line of fsa file
	FSA_ACCEPT_REGEX_PATTERN = re.compile(r"([0-9]+)$")
	FSA_EDGE_REGEX_PATTERN = re.compile(r"\(([0-9]+) \(([0-9]+) (\"|\*)([a-z])(\"|\*)\)\)")
	accept_match = FSA_ACCEPT_REGEX_PATTERN.match(line.strip())


	if accept_match:
		acc_state = accept_match.group(1)

	else:
		edge_match = FSA_EDGE_REGEX_PATTERN.match(line)
		curr = edge_match.group(1)
		next_node_code = edge_match.group(2)
		eps_code = edge_match.group(3)
		edge_char = edge_match.group(4)
		

		if curr not in node_dict:

			new_node = Node(curr)
			node_dict[curr] = new_node
			#print("made " + str(new_node))

			if acc_state is curr:
				new_node.set_accept()


		new_edge = Edge(edge_char, next_node_code, ("*" is eps_code))
		node_dict[curr].adjacents.append(new_edge)
		debugPrint("adjacents are  " + str(node_dict[curr].adjacents))


fsa_file.close()


# START NEW STUFF