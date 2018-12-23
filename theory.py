import networkx as nx 

class Idea:
	#constructor for brainstorm theory type
	def __init__(self, name, description):
		self.name = name
		self.description = description

	#constructor for If/Then and FOL theory types
	#argument is the logical operation internal to this idea
	def __init__(self, name, description, argument):
		self.name = name
		self.description = description
		self.argument = argument

class Theory:

	def __init__(self):
		self.ideaNetwork = nx.Graph()

	def addIdea(self, idea):
		self.ideaNetwork.add_node(idea)

	def linkIdeas(self, away, towards):
		self.ideaNetwork.add_edge(away, towards)

	def removeIdea(self, idea):
		self.ideaNetwork.remove_node(idea)

	def removeLink(self, away, towards):
		self.ideaNetwork.remove_edge(away, towards)

	#display work here
	def display(self):
		print("eat ass")

		
	#loop through graph for a path back to oneself
	def checkCircularity(self, idea):
		print("eat ass")
		
	#see if any set of ideas are disconnected from the rest
	#returns this set of disconnected nodes if found, null otherwise
	def findIslands(self):
		print("eat ass")


		