import networkx as nx
#import networkx.drawing as draw
#import matplotlib.pyplot as plot

class Idea:
	#constructor for brainstorm theory type
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
	#and ranks each node according to its std deviation
	#def connectivityStdDev(self):
		#loop through the nodes and get their degrees to calculate
		#the std deviation
	#	stdDev = 0;

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

		elif arg == "help":
			print("Commands: add, link, rmIdea, rmLink, display, exit\n")

		elif arg == "exit":
			break

		else:
			print("Unrecognized argument.\n")

if __name__ == "__main__":
	main()
