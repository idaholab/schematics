from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Reflected node labels.')
command_line_parser.parse()

from schematics import Graph
from schematics import Canvas
import matplotlib.pyplot as plt

main = Graph(name = 'main')

main.add_node(x=0.0,   y=0.0,   name = 'A',   ll = 'bottom')
main.add_node(x=1.0,   y=0.0,   name = 'B',   ll = 'right')
main.add_node(x=1.0,   y=1.0,   name = 'C',   ll = 'top')
main.add_node(x=0.0,   y=1.0,   name = 'D',   ll = 'left')

# BOTTOM
bottom = Graph(name = 'bottom')

bottom.add_node(x=0.5,   y=-1.0,
                name = 'angled name [x]',
                ll = 'bottom', la = 45.0)

bottom.add_node(x=0.5,   y=-1.0,
                name = 'angled (ref) [x]',
                ll = 'bottom', la = 45.0, ref = 'x')

bottom.add_node(x=0.5,   y=-2.0,
                name = 'angled name [y]',
                ll = 'bottom', la = 45.0)

bottom.add_node(x=0.5,   y=-2.0,
                name = 'angled (ref) [y]',
                ll = 'bottom', la = 45.0, ref = 'y')


# TOP
top = Graph(name = 'top')

top.add_node(x=0.5,   y=2.0,
             name = 'angled name [x]',
             ll = 'top', la = 45.0)

top.add_node(x=0.5,   y=2.0,
             name = 'angled (ref) [x]',
             ll = 'top', la = 45.0, ref = 'x')

top.add_node(x=0.5,   y=3.0,
             name = 'angled name [y]',
             ll = 'top', la = 45.0)

top.add_node(x=0.5,   y=3.0,
             name = 'angled (ref) [y]',
             ll = 'top', la = 45.0, ref = 'y')


# RIGHT
right = Graph(name = 'right')

right.add_node(x=2.0,   y=0.5,
               name = 'angled name [y]',
               ll = 'right', la = 45.0)

right.add_node(x=2.0,   y=0.5,
               name = 'angled (ref) [y]',
               ll = 'right', la = 45.0, ref = 'y')

right.add_node(x=3.0,   y=0.5,
               name = 'angled name [x]',
               ll = 'right', la = 45.0)

right.add_node(x=3.0,   y=0.5,
               name = 'angled (ref) [x]',
               ll = 'right', la = 45.0, ref = 'x')

# LEFT
left = Graph(name = 'left')

left.add_node(x=-1.0,   y=0.5,
              name = 'angled name [y]',
              ll = 'left', la = 45.0)

left.add_node(x=-1.0,   y=0.5,
              name = 'angled (ref) [y]',
              ll = 'left', la = 45.0, ref = 'y')

left.add_node(x=-2.0,   y=0.5,
              name = 'angled name [x]',
              ll = 'left', la = 45.0)

left.add_node(x=-2.0,   y=0.5,
              name = 'angled (ref) [x]',
              ll = 'left', la = 45.0, ref = 'x')

GRAPH = Graph(name = 'graph', graphs = [main, left, right, top, bottom])
GRAPH.anchor_graph()
print 'Nodes are anchored:', GRAPH.anchored
print GRAPH.general_info(), '\n'
print GRAPH

CAN = Canvas(border_thickness = 0.05, grid = True)
CAN.add_graph(GRAPH)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
