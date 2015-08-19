from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('A long junction.')
command_line_parser.parse()

from schematics import Graph
from schematics import Canvas
import matplotlib.pyplot as plt
from math import sqrt

component1 = Graph(name = 'component1')
component1.add_node(x=0.0,   y=0.0,   name = 'outlet',   ll = 'bottom')

component2 = Graph(name = 'component2')
component2.add_node(x=2.0,   y=1.0,   name = 'inlet',   ll = 'top')

junction = Graph(name = 'junction')
junction.add_node(x=1.0,   y=0.0,   name = 'node1',   ll = 'bottom', draw = False)
junction.add_node(x=1.0,   y=1.0,   name = 'node2',   ll = 'top', draw = False)

system1 = Graph(name = 'system1', graphs = [component1, component2, junction])
system1.connect('component1:outlet', 'junction:node1',
                dir = False, ll = 'top',
                ew = 0.05
               )
system1.connect('junction:node1', 'junction:node2',
                dir = False, ll = 'top',
                ew = 0.05
               )
system1.connect('junction:node2', 'component2:inlet',
                dir = True,  ll = 'top',
                ew = 0.05, hw_to_ew = 2.5, hl_to_hw = 2.5
               )

# system2 = system1.copy(4.0, 0.0, name = 'system2')
# system2.rotate(45.0)

plot = Graph(name = 'plot', graphs = [system1])#, system2])

CAN = Canvas(border_thickness = 0.05, grid = True)
CAN.add_graph(plot)
CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
