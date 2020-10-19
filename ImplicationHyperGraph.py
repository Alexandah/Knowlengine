from z3 import *


class ImplicationHyperGraph:
    class ImplicationEdge:
        class EdgeConnector:
            def __init__(self, node, negated=False):
                self.node = node
                self.negated = negated

        def __init__(self, in_nodes, out_nodes):
            self.in_nodes = set(
                [
                    self.EdgeConnector(x[1:], True)
                    if "~" in x
                    else self.EdgeConnector(x)
                    for x in in_nodes
                ]
            )
            self.out_nodes = set(
                [
                    self.EdgeConnector(x[1:], True)
                    if "~" in x
                    else self.EdgeConnector(x)
                    for x in out_nodes
                ]
            )

    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.props = {}
        self.comp_props = {}

    def add_node(self, nodes=[]):
        self.nodes.update(nodes)
        for n in nodes:
            self.props[n] = Bool(n)

    def add_edge(self, edge):
        in_nodes = edge[0]
        out_nodes = edge[1]
        new_nodes = [x[1:] if "~" in x else x for x in in_nodes] + [
            x[1:] if "~" in x else x for x in out_nodes
        ]
        for n in new_nodes:
            if not n in self.nodes:
                assert False
        e = self.ImplicationEdge(in_nodes, out_nodes)
        self.edges.add(e)
        return e

    def implies_edge(self, implier, implied):
        self.add_edge((implier, implied))
        p = self.props[implier[0]]
        q = self.props[implied[0]]
        string = implier[0] + "-->" + implied[0]
        self.comp_props[string] = Implies(p, q)

    def and_implies_edge(self, anded, implied):
        self.add_edge((anded, implied))
        P = [self.props[x] for x in anded]
        q = self.props[implied[0]]
        string = ""
        for i, x in enumerate(anded):
            string += x
            if i < len(anded) - 1:
                string += "&"
        string += "-->" + implied[0]
        self.comp_props[string] = Implies(And(P), q)

    def or_implies_edge(self, ored, implied):
        for node in ored:
            self.add_edge((node, implied))
        P = [self.props[x] for x in ored]
        q = self.props[implied[0]]
        string = ""
        for i, x in enumerate(ored):
            string += x
            if i < len(ored) - 1:
                string += "\/"
        string += "-->" + implied[0]
        self.comp_props[string] = Implies(Or(P), q)

    def implies_and_edge(self, implier, anded):
        for node in anded:
            self.add_edge((implier, node))
        Q = [self.props[x] for x in anded]
        p = self.props[implier[0]]
        string = implier[0] + "-->"
        for i, x in enumerate(anded):
            string += x
            if i < len(anded) - 1:
                string += "&"
        self.comp_props[string] = Implies(p, And(Q))

    def implies_or_edge(self, implier, ored):
        self.add_edge((implier, ored))
        Q = [self.props[x] for x in ored]
        p = self.props[implier[0]]
        string = implier[0] + "-->"
        for i, x in enumerate(ored):
            string += x
            if i < len(ored) - 1:
                string += "\/"
        self.comp_props[string] = Implies(p, Or(Q))

    def check_sat(self, conditions=[]):
        s = Solver()
        s.add([self.comp_props[x] for x in self.comp_props] + conditions)
        print(s.check())
        print("Example: " + str(s.model()))

    def check_possible_worlds(self, conditions=[]):
        def search(prop, props_left, assignment, truth_assignments):
            if len(props_left) == 0:
                for val in [prop, Not(prop)]:
                    truth_assignments.append(assignment + [val])
                return
            for val in [prop, Not(prop)]:
                search(
                    props_left[0], props_left[1:], assignment + [val], truth_assignments
                )
            return truth_assignments

        props_left = [self.props[x] for x in self.props]
        first_prop = props_left[0]
        props_left = props_left[1:]
        truth_assignments = search(first_prop, props_left, [], [])
        print(truth_assignments)

        possible_worlds = []
        clauses = [self.comp_props[x] for x in self.comp_props] + conditions
        for world in truth_assignments:
            s = Solver()
            s.add(clauses + world)
            if s.check() == "sat":
                possible_worlds.append(world)

        print("possible worlds")
        print(possible_worlds)

        return possible_worlds

    def print_graph(self):
        print("Nodes: " + str(self.nodes))
        print("Edges: ")
        for e in self.edges:
            print(" In: ")
            for s in e.in_nodes:
                print("     ~" + s.node) if s.negated else print("      " + s.node)
            print(" Out: ")
            for d in e.out_nodes:
                print("     ~" + d.node) if d.negated else print("      " + d.node)


if __name__ == "__main__":
    G = ImplicationHyperGraph()
    # The Indispensibility Argument
    """
    p1 = "exists_x Fx means x exists"
    p2 = "nat sci existentially quantifies over abstract objects"
    p3 = "we should believe what nat sci tells us"
    c = "we should believe that abstract objects exist"
    """
    p1 = "p1"
    p2 = "p2"
    p3 = "p3"
    c = "c"
    G.add_node([p1, p2, p3, c])
    G.and_implies_edge([p1, p2, p3], [c])
    G.print_graph()
    G.check_sat([G.props[p1], G.props[p2], G.props[p3]])
    print(G.check_possible_worlds())
