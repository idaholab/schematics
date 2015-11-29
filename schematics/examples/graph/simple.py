from __future__ import print_function
from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Pentagon graph test case.')
command_line_parser.parse()

from schematics import Graph
from schematics import Canvas

GRAPH = Graph(name = 'pentagon')

# Add Nodes
GRAPH.add_node(x=0.0,   y=0.0,   name = 'A', anchor = True, ll = 'top')
GRAPH.add_node(x=0.75,  y=-1.5,  name = 'B', ll = 'bottom')
GRAPH.add_node(x=-1.5,  y=-0.75, name = 'C', ll = 'left')
GRAPH.add_node(x=1.5,   y=-0.75, name = 'D', ll = 'right')
GRAPH.add_node(x=-0.75, y=-1.5,  name = 'E', ll = 'bottom')

# Add Connections
GRAPH.connect('A', 'B', name = "I", directional = False, ll = 'top')
GRAPH.connect('C', 'A', name = "II", ll = 'top')
GRAPH.connect('A', 'D', name = "III", ll = 'top')
GRAPH.connect('A', 'E', name = "IV", directional = False, ll = 'top')

GRAPH.connect('B', 'C', name = "V", directional = False, ll = 'top')
GRAPH.connect('D', 'B', name = "VI", ll = 'bottom')
GRAPH.connect('B', 'E', name = "VII", ll = 'bottom')

GRAPH.connect('C', 'D', name = "VIII", directional = False, ll = 'top')
GRAPH.connect('E', 'C', name = "IX", ll = 'bottom')

GRAPH.connect('D', 'E', name = "X", directional = False, ll = 'top')

GRAPH.anchor_graph()
print('Nodes are anchored:', GRAPH.anchored)
print(GRAPH.general_info(), '\n')
print(GRAPH)

# plot
CAN = Canvas(border_thickness = 0.05, grid = True)
CAN.add_graph(GRAPH)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
