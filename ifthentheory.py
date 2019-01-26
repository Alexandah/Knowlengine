import networkx as nx
from theory import Theory
from theory import Idea

class IfThenTheory(Theory):
	
	def __init__(self):
		self.ideaNetwork = nx.DiGraph()
		#ignored words is a dict to ensure checking if it contains an item O(1)
		self.ignoredWords = dict()
		for line in open("ignoredWords.txt", 'r'):
			self.ignoredWords[line] = line

	#checks for circular logic
	#returns None if no circular arguments are found
	#returns a list of circular arguments if at least one is found
	def checkCircularity(self):
		circularArguments = list(nx.simple_cycles(self.ideaNetwork))
		if len(circularArguments) is 0:
			return None
		return circularArguments


	#-naive version of a non-sequeter detector
	#-is naive b/c can only understand explicit meaning, aka can't account for synonyms,
	#and doesn't check that the relations between nouns, adjectives, and verbs are not altered arbitrarily.
	#These would require AI and such is beyond the current scope of this project.
	#-works by checking all non-articles and non-prepositions within a given idea and 
	#seeing if their occurences occur at least once in the ideas from which this idea derives
	#-if at least one item of the conclusion cannot be found within the argument's premises, 
	#then return true. Otherwise return false. 
	def isNonSequeterNaive(self, idea):
		premises = self.ideaNetwork.predecessors(idea)
		
		#check each word in the idea's description
		words = idea.description.split()
		for word in words:
			#pass over irrelivant word types
			if word in self.ignoredWords:
				continue
			#check if this word can be found within the premises
			#if not, then a nonsequeter has occurred
			found = False
			numPremises = 0
			for premise in premises:
				numPremises+=1
				for premiseWord in premise.description.split():
					if word == premiseWord:
						found = True
						break
				if found:
					break;

			#if this idea has no premises, then treat it as an axiom true in itself.
			#this cannot be a nonsequeter in this case.
			if numPremises == 0:
				return False
					
			if not found: 
				print("Found nonsequeter for idea: "+idea.name+" on word: "+word)
				return True 

		#we've checked all the relevant words and failed to find a non-sequeter
		return False

	#return a list of all suspected nonsequeters
	#I'm guessing this is around O(n^2) to O(n^3) but I don't feel like 
	#calculating this precisely rn
	def checkNonSequeters(self):
		nonSeq = list()
		for idea in self.ideaNetwork.nodes():
			if self.isNonSequeterNaive(idea):
				nonSeq.append(idea)

		return nonSeq