from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Labeled node test case.')
command_line_parser.parse()

from schematics import Graph
from schematics import Canvas
import matplotlib.pyplot as plt

main = Graph(name = 'main')

main.add_node(x=0.0,   y=0.0,   ll = 'bottom')
main.add_node(x=1.0,   y=0.0,   ll = 'right')
main.add_node(x=1.0,   y=1.0,   ll = 'top')
main.add_node(x=0.0,   y=1.0,   ll = 'left')

main.connect('Node 0', 'Node 1', label_location = 'bottom', label_angle = 30.0)
main.connect('Node 1', 'Node 2', label_location = 'top',    label_angle = 30.0)
main.connect('Node 2', 'Node 3', label_location = 'top',    label_angle = 30.0)
main.connect('Node 3', 'Node 0', label_location = 'top',    label_angle = 30.0)

print main.edges

GRAPH = Graph(name = 'graph', graphs = [main], node_line_width = 2.0, node_radius = 0.05)
GRAPH.anchor_graph()
print 'Nodes are anchored:', GRAPH.anchored
print GRAPH.general_info(), '\n'
print GRAPH

CAN = Canvas(border_thickness = 0.05, grid = True)
CAN.add_graph(GRAPH)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
