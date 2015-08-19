from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('A basic junction.')
command_line_parser.parse()

from schematics import Graph
from schematics import Canvas
import matplotlib.pyplot as plt
from math import sqrt

component1 = Graph(name = 'component1')
component1.add_node(x=0.0,   y=0.0,   name = 'outlet',   ll = 'bottom')

component2 = Graph(name = 'component2')
component2.add_node(x=1.0,   y=1.0,   name = 'inlet',   ll = 'right')

junction = Graph(name = 'junction')
junction.add_node(x=1.0,   y=0.0,   name = 'node',   ll = 'bottom', draw = False)

system1 = Graph(name = 'system1', graphs = [component1, component2, junction])
system1.connect('component1:outlet', 'junction:node', dir = False, ll = 'top')
system1.connect('junction:node', 'component2:inlet',  dir = True,  ll = 'top')

system2 = system1.copy(2.0, 0.0, name = 'system2')
system2.rotate(45.0)

# -----

component1 = Graph(name = 'component1')
component1.add_node(x=0.0,   y=2.0,   name = 'outlet',   ll = 'bottom')

component2 = Graph(name = 'component2')
component2.add_node(x=1.5,   y=3.0,   name = 'inlet',   ll = 'right')

junction = Graph(name = 'junction')
junction.add_node(x=1.0,   y=2.0,   name = 'node',   ll = 'bottom', draw = False)

system3 = Graph(name = 'system3', graphs = [component1, component2, junction])
system3.connect('component1:outlet', 'junction:node', dir = False, ll = 'top')
system3.connect('junction:node', 'component2:inlet',  dir = True,  ll = 'top')

system4 = system3.copy(2.0, 2.0, name = 'system4')
system4.rotate(45.0)


# -----

plot = Graph(name = 'plot', graphs = [system1, system2, system3, system4])

CAN = Canvas(border_thickness = 0.05, grid = True)
CAN.add_graph(plot)
CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
