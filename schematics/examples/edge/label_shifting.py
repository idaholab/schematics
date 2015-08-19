from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Shifting edge label.')
command_line_parser.parse()

from schematics import Graph
from schematics import Canvas
import matplotlib.pyplot as plt
from math import sqrt

main = Graph(name = 'main')

main.add_node(x=0.0,   y=0.0,   name = 'A',   ll = 'bottom')
main.add_node(x=1.0,   y=0.0,   name = 'B',   ll = 'right')

main.connect('A', 'B', name = '1', ll = 'top', la = 0.0, label_shift = 0.75)

graphs = []
displacement = 3.0

for i in range(2):
  graphs.append( main.copy(i * displacement, 0.0) )
  graphs[-1].rotate(i * 45.0)

main.connect('A', 'B', name = '1', ll = 'bottom', la = 0.0, label_shift = -0.75)
for i in range(2):
  graphs.append( main.copy(i * displacement, 2.0) )
  graphs[-1].rotate(i * 45.0)

CAN = Canvas(border_thickness = 0.05, grid = True)
for graph in graphs:
  CAN.add_graph(graph)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
