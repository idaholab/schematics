from unittest import TestCase

from schematics import Node, Edge, Graph
from copy import deepcopy


class TestGraph(TestCase):
  def _check_graph(self, graph, name, anchor, anchored, nodes, edges, numbers): # numbers -- (anchored_nodes, anchored_edges, unique_nodes, unique_anchored_edges, unique_unanchored_edges, subgraphs, anchored_subgraphs)
    self.assertEqual(len(graph.nodes), len(nodes))
    self.assertEqual(len(graph.edges), len(edges))
    self.assertEqual(graph.anchor, anchor)
    self.assertEqual(graph.anchored, anchored)

    for node in nodes:
      self.assertEqual(graph.nodes[node[0]], node[1])

    for edge in edges:
      self.assertEqual(graph.edges[edge[0]], edge[1])

    self.assertEqual(len(graph.anchored_nodes), numbers[0])
    self.assertEqual(len(graph.anchored_edges), numbers[1])

    self.assertEqual(len(graph.unique_nodes), numbers[2])
    self.assertEqual(len(graph.unique_anchored_edges), numbers[3])
    self.assertEqual(len(graph.unique_unanchored_edges), numbers[4])

    self.assertEqual(len(graph.subgraphs), numbers[5])
    self.assertEqual(len(graph.anchored_subgraphs), numbers[6])

    self.assertEqual(graph.name, name)


  def _get_original_numbers(self):
    return (len(Node._instances), len(Edge._instances), len(Graph.graphs))


  def _check_numbers(self, (node, edge, graph), node_inc, edge_inc, graph_inc):
    self.assertEqual(node + node_inc, len(Node._instances))
    self.assertEqual(edge + edge_inc, len(Edge._instances))
    self.assertEqual(graph + graph_inc, len(Graph.graphs))


  def test_instantiation(self):
    original_numbers = self._get_original_numbers()

    simple = Graph(name = 'simple')

    nodes = []
    edges = []
    numbers = (0, # anchored_nodes
               0, # anchored_edges
               0, # unique_nodes
               0, # unique_anchored_edges
               0, # unique_unanchored_edges
               0, # subgraphs
               0  # anchored_subgraphs
              )
    self._check_graph(simple, 'simple', None, False, nodes, edges, numbers)
    self._check_numbers(original_numbers, 0, 0, 1)


  def test_add_node(self):
    original_numbers = self._get_original_numbers()

    simple = Graph(name = 'simple')
    simple.add_node(x=0.0,   y=1.0,   name = 'A')

    nodes = [('A', Node(0.0, 1.0))]
    edges = []
    numbers = (1, # anchored_nodes
               0, # anchored_edges
               1, # unique_nodes
               0, # unique_anchored_edges
               0, # unique_unanchored_edges
               0, # subgraphs
               0  # anchored_subgraphs
              )
    self._check_graph(simple, 'simple', 'A', False, nodes, edges, numbers)
    self._check_numbers(original_numbers, 2, 0, 1)


  def test_connect(self):
    original_numbers = self._get_original_numbers()

    simple = Graph(name = 'simple')
    simple.add_node(x=0.0,   y=0.0,   name = 'A')
    simple.add_node(x=0.0,   y=1.0,   name = 'B', anchor = True)
    simple.connect('A', 'B', name = "I", directional = False)

    nodes = [('A', Node(0.0, 0.0)), ('B', Node(0.0, 1.0))]
    edges = [('I', Edge('A', 'B', directional = False))]
    numbers = (2, # anchored_nodes
               1, # anchored_edges
               2, # unique_nodes
               1, # unique_anchored_edges
               0, # unique_unanchored_edges
               0, # subgraphs
               0  # anchored_subgraphs
              )
    self._check_graph(simple, 'simple', 'B', True, nodes, edges, numbers)
    self._check_numbers(original_numbers, 4, 2, 1)


  def test_copy(self):
    original_numbers = self._get_original_numbers()

    simple = Graph(name = 'simple')
    simple.add_node(x=0.0,   y=0.0,   name = 'A')
    simple.add_node(x=0.0,   y=1.0,   name = 'B')
    simple.connect('A', 'B', name = "I", directional = False)
    simple_copy = simple.copy(0.0, 0.0)

    nodes = [('A', Node(0.0, 0.0)), ('B', Node(0.0, 1.0))]
    edges = [('I', Edge('A', 'B', directional = False))]
    numbers = (2, # anchored_nodes
               1, # anchored_edges
               2, # unique_nodes
               1, # unique_anchored_edges
               0, # unique_unanchored_edges
               0, # subgraphs
               0  # anchored_subgraphs
              )
    self._check_graph(simple_copy, 'simple(copy)', 'A', True, nodes, edges, numbers)
    self._check_numbers(original_numbers, 6, 3, 2)

    for node, node_copy in zip(simple.nodes.values(), simple_copy.nodes.values()):
      self.assertEqual(node, node_copy)
      self.assertIsNot(node, node_copy)
    for edge, edge_copy in zip(simple.edges.values(), simple_copy.edges.values()):
      self.assertEqual(edge, edge_copy)
      self.assertIsNot(edge, edge_copy)


  def test_subgraphing(self):
    original_numbers = self._get_original_numbers()

    simple = Graph(name = 'simple')
    simple.add_node(x=0.0,   y=0.0,   name = 'A')
    simple.add_node(x=0.0,   y=1.0,   name = 'B')
    simple.connect('A', 'B', name = "I", directional = False)
    simple_copy = simple.copy(1.0, 0.0)
    super_graph = Graph(name = 'super_graph', graphs = [simple, simple_copy])
    super_graph.connect('simple:A', 'simple(copy):B', name = 'II', directional = True)

    nodes = [('simple:A', Node(0.0, 0.0)), ('simple:B', Node(0.0, 1.0)),
             ('simple(copy):A', Node(1.0, 0.0)), ('simple(copy):B', Node(1.0, 1.0))]
    edges = [('simple:I', Edge('simple:A', 'simple:B', directional = False)),
             ('simple(copy):I', Edge('simple(copy):A', 'simple(copy):B', directional = False)),
             ('II', Edge('simple:A', 'simple(copy):B', directional = True))]
    numbers = (4, # anchored_nodes
               3, # anchored_edges
               0, # unique_nodes
               1, # unique_anchored_edges
               0, # unique_unanchored_edges
               2, # subgraphs
               2  # anchored_subgraphs
              )
    self._check_graph(super_graph, 'super_graph', 'simple:A', True, nodes, edges, numbers)
    self._check_numbers(original_numbers, 8, 6, 3)


  def test_copying_with_subgraphing(self):
    original_numbers = self._get_original_numbers()

    pipe1 = Graph(name = 'pipe1')
    pipe1.add_node(x=0.0, y=0.0, name = 'inlet')
    pipe1.add_node(1.0, 0.0, name = 'outlet')
    pipe2 = pipe1.copy(x=1.5, y=0.0, name = 'pipe2')
    long_pipe1 = Graph(name = 'long_pipe1', graphs = [pipe1, pipe2])
    long_pipe1.connect('pipe1:outlet', 'pipe2:inlet', name = "junction")
    long_pipe1.connect('pipe1:inlet', 'pipe1:outlet', name = "internal-connection1", directional = False)
    long_pipe1.connect('pipe2:inlet', 'pipe2:outlet', name = "internal-connection2", directional = False)
    long_pipe2 = long_pipe1.copy(x=2.5, y=1.0, name = 'long_pipe2')
    long_pipe2.reflect(axis = 'y')
    circuit = Graph(name = 'circuit', graphs = [long_pipe1, long_pipe2])
    circuit.connect('long_pipe1:pipe2:outlet', 'long_pipe2:pipe1:inlet', name = "junction1")
    circuit.connect('long_pipe2:pipe2:outlet', 'long_pipe1:pipe1:inlet', name = "junction2")

    nodes = [('long_pipe1:pipe1:inlet',  Node(0.0, 0.0)),
             ('long_pipe1:pipe1:outlet', Node(1.0, 0.0)),
             ('long_pipe1:pipe2:inlet',  Node(1.5, 0.0)),
             ('long_pipe1:pipe2:outlet', Node(2.5, 0.0)),
             ('long_pipe2:pipe1:inlet',  Node(2.5, 1.0)),
             ('long_pipe2:pipe1:outlet', Node(1.5, 1.0)),
             ('long_pipe2:pipe2:inlet',  Node(1.0, 1.0)),
             ('long_pipe2:pipe2:outlet', Node(0.0, 1.0))]
    edges = [('long_pipe1:junction', Edge('long_pipe1:pipe1:outlet', 'long_pipe1:pipe2:inlet', directional = True)),
             ('long_pipe1:internal-connection1', Edge('long_pipe1:pipe1:inlet', 'long_pipe1:pipe1:outlet', directional = False)),
             ('long_pipe1:internal-connection2', Edge('long_pipe1:pipe2:inlet', 'long_pipe1:pipe2:outlet', directional = False)),
             ('long_pipe2:junction', Edge('long_pipe2:pipe1:outlet', 'long_pipe2:pipe2:inlet', directional = True)),
             ('long_pipe2:internal-connection1', Edge('long_pipe2:pipe1:inlet', 'long_pipe2:pipe1:outlet', directional = False)),
             ('long_pipe2:internal-connection2', Edge('long_pipe2:pipe2:inlet', 'long_pipe2:pipe2:outlet', directional = False)),
             ('junction1', Edge('long_pipe1:pipe2:outlet', 'long_pipe2:pipe1:inlet', directional = True)),
             ('junction2', Edge('long_pipe2:pipe2:outlet', 'long_pipe1:pipe1:inlet', directional = True))]
    numbers = (8, # anchored_nodes
               8, # anchored_edges
               0, # unique_nodes
               2, # unique_anchored_edges
               0, # unique_unanchored_edges
               2, # subgraphs
               2  # anchored_subgraphs
              )
    self._check_graph(circuit, 'circuit', 'long_pipe1:pipe1:inlet', True, nodes, edges, numbers)
    self._check_numbers(original_numbers, 16, 16, 7)
