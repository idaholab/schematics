from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Reflected graph test case.')
command_line_parser.parse()

from schematics import Graph
from schematics import Canvas
import matplotlib.pyplot as plt
from math import sqrt

main = Graph(name = 'main')

main.add_node(x=0.0,   y=0.0,   name = 'A',   ll = 'bottom')
main.add_node(x=1.0,   y=0.0,   name = 'B',   ll = 'right')
main.add_node(x=1.0,   y=1.0,   name = 'C',   ll = 'top')
main.add_node(x=0.0,   y=1.0,   name = 'D',   ll = 'left')

main.connect('A', 'B', name = '1', ll = 'top', la = 45.0, lp = 1.0)
main.connect('B', 'C', name = '2', ll = 'top', la = 45.0, lp = 1.0)
main.connect('C', 'D', name = '3', ll = 'top', la = 45.0, lp = 1.0)
main.connect('D', 'A', name = '4', ll = 'top', la = 45.0, lp = 1.0)

main.anchor_graph()
print 'Nodes are anchored:', main.anchored
print main.general_info(), '\n'
print main

graphs = []
graphs.append(main)

graphs.append( main.copy(-1.0, 0.0) )
graphs[-1].reflect('y')

graphs.append( main.copy(0.0, -1.0) )
graphs[-1].reflect('x')


CAN = Canvas(border_thickness = 0.05, grid = True)
for graph in graphs:
  CAN.add_graph(graph)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
