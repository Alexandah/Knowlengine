from theory import Idea
from theory import Theory
from ifthentheory import IfThenTheory

#handles cmd line parsing
def main():
	t = None

	arg = ""
	while True:
		arg = input("Knowlengine: What kind of theory? Brainstorm or IfThen: ")
		if arg == "Brainstorm":
			print("Using Brainstorm theory type.\n")
			t = Theory()
			break

		elif arg == "IfThen":
			print("Using IfThen theory type.\n")
			t = IfThenTheory()
			break

		else:
			print("Unrecognized theory type.\n")

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

		elif arg == "circ":
			if not isinstance(t, IfThenTheory):
				print("Unrecognized argument.\n")

			print("Circular logic: ")
			for circle in t.checkCircularity():
				names = list()
				for idea in circle:
					names.append(idea.name)
				print(str(names))
			print()

		elif arg == "nonseq":
			if not isinstance(t, IfThenTheory):
				print("Unrecognized argument.\n")

			print("Possible non-sequeters: ")
			for idea in t.checkNonSequeters():
				idea.print()	
			print()

		elif arg == "help":
			if not isinstance(t, IfThenTheory): 
				print("Commands: add, link, rmIdea, rmLink, rank, display, exit\n")
			else:
				print("Commands: add, link, rmIdea, rmLink, rank, circ, nonseq, display, exit\n")

		elif arg == "exit":
			break

		else:
			print("Unrecognized argument.\n")

if __name__ == "__main__":
	main()
