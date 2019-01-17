import networkx as nx
import math
#import networkx.drawing as draw
#import matplotlib.pyplot as plot

class Idea:
	#constructor for "brainstorm" theory type
	def __init__(self, name, description):
		self.name = name
		self.description = description

	def print(self):
		print("	Name: "+self.name+" Description: "+self.description)

class Theory:

	def __init__(self):
		self.ideaNetwork = nx.Graph()

	#return the node with the given name
	#return None if its not there
	#for later, try to make this O(1) as opposed to O(N)
	def getNode(self, name):
		for node in self.ideaNetwork.nodes():
			if node.name == name:
				return node
		return None

	#returns the degree of a given node object
	#returns -1 if the node doesn't exist
	def getDeg(self, node):
		if node not in self.ideaNetwork.nodes():
			return -1
		return self.ideaNetwork.degree(node)

	#given an idea object and attribute string, return the attribute
	def getAttribute(self, node, attribute):
		return self.ideaNetwork.node[node][attribute]
	#given an idea object, attribute string, and new value, set the attribute
	def setAttribute(self, node, attribute, value):
		self.ideaNetwork.node[node][attribute] = value

	#adds given idea object to theory graph
	def addIdea(self, idea):
		self.ideaNetwork.add_node(idea)

	#away and towards are the string names of the nodes to be linked
	#doesn't support linking non-existent nodes
	def linkIdeas(self, away, towards):
		awayNode = self.getNode(away)
		towardsNode = self.getNode(towards)

		if awayNode!=None and towardsNode!=None:
			self.ideaNetwork.add_edge(awayNode, towardsNode)
		else:
			print("Couldn't link the nodes because at least one does not exist!")

	#remove idea by name string
	def removeIdea(self, idea):
		ideaNode = self.getNode(idea)

		if ideaNode!=None:
			self.ideaNetwork.remove_node(ideaNode)
		else:
			print("Can't remove non-existent ideas!")

	#remove link by name strings of connected nodes
	def removeLink(self, away, towards):
		#first check that both nodes exist
		awayNode = self.getNode(away)
		if awayNode==None:
			print("Start node doesn't exist!")
			return
		towardsNode = self.getNode(towards)
		if towardsNode==None:
			print("End node doesn't exist!")
			return

		#remove edge if it exists, print error otherwise
		try:
			self.ideaNetwork.remove_edge(awayNode, towardsNode)
		except:
			print("Link doesn't exist to be removed!")



	#calculates the std deviation of num edges per node
	#and ranks each node according to this sigma value
	#returns list of properly ranked ideas
	def connectivityStdDev(self):
		ideas = self.ideaNetwork.nodes()
		#loop through the nodes and calculate average degree
		avgDeg = 0
		for idea in ideas:
			avgDeg += self.getDeg(idea)
		avgDeg /= len(ideas)

		#calculate the std deviation = sqrt((1/n)sum([Xi-avg]^2))
		sigma = 0
		for idea in ideas:
			sigma += pow(self.getDeg(idea)-avgDeg,2)
		sigma /= len(ideas)
		sigma = math.sqrt(sigma)
		#rank each node according to its sigma adjusted value
		ranked = list()
		for idea in ideas:
			#mark the node with its value
			self.setAttribute(idea, 'connectivityRating', self.getDeg(idea)/sigma)
			ranked.append(idea)

		#sort ideas by connectivity
		ranked.sort(key = lambda idea: self.getAttribute(idea, 'connectivityRating'), reverse=True)
		return ranked


	#display work here
	#make it look pretty later
	def display(self):
		print("Nodes: ")
		for idea in self.ideaNetwork.nodes():
			idea.print()
		print("\n")

		print("Edges: ")
		for edge in self.ideaNetwork.edges():
			output = "	[ "
			for idea in edge:
				output+= idea.name + ", "
			output+="]"
			print(output)
		print("\n")



#handles cmd line parsing
def main():
	t = Theory()
	arg = ""
	while True:
		arg = input("Knowlengine: ")
		if arg == "add":
			name = input("Idea name: ")
			description = input("Idea description: ")
			t.addIdea(Idea(name, description))
			print()

		elif arg == "link":
			ideaA = input("From idea: ")
			ideaB = input("To idea: ")
			t.linkIdeas(ideaA, ideaB)
			print()

		elif arg == "rmIdea":
			name = input("Idea to remove: ")
			t.removeIdea(name)
			print()

		elif arg == "rmLink":
			ideaA = input("Start of link to remove: ")
			ideaB = input("End of link to remove: ")
			t.removeLink(ideaA, ideaB)
			print()

		elif arg == "display":
			t.display()

		elif arg == "rank":
			print("Ideas ranked by connectedness:")
			for idea in t.connectivityStdDev():
				print("Name: "+idea.name+" Connectivity: "+str(t.getAttribute(idea, 'connectivityRating')))
			print()

		elif arg == "help":
			print("Commands: add, link, rmIdea, rmLink, rank, display, exit\n")

		elif arg == "exit":
			break

		else:
			print("Unrecognized argument.\n")

if __name__ == "__main__":
	main()
