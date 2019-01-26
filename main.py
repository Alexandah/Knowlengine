from theory import Idea
from theory import Theory
from ifthentheory import IfThenTheory

#handles cmd line parsing
def main():
	t = None

	arg = ""
	while True:
		arg = input("Knowlengine: What kind of theory? Brainstorm(1) or IfThen(2): ")
		if arg == "1":
			print("Using Brainstorm theory type.\n")
			t = Theory()
			break

		elif arg == "2":
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

		elif arg == "disp":
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
			circles = t.checkCircularity()
			if circles is None:
				print("No circular logic found!")
			else:
				for circle in circles:
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
				print("Commands: add, link, rmIdea, rmLink, rank, disp, exit\n")
			else:
				print("Commands: add, link, rmIdea, rmLink, rank, circ, nonseq, disp, exit\n")

		elif arg == "exit":
			break

		else:
			print("Unrecognized argument.\n")

if __name__ == "__main__":
	main()
