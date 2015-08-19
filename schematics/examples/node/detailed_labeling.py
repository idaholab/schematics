from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Detailed node label.')
command_line_parser.parse()

from schematics import Graph
from schematics import Canvas
import matplotlib.pyplot as plt

main = Graph(name = 'main')

main.add_node(x=0.0, y=0.0, name = 'test0', ll = 'bottom', lp = 0.0)
main.add_node(x=0.0, y=0.0, name = 'test1', ll = 'top',    lp = 0.0)
main.add_node(x=0.0, y=0.0, name = 'test2', ll = 'left',   lp = 0.0)
main.add_node(x=0.0, y=0.0, name = 'test3', ll = 'right',  lp = 0.0)

bounding = Graph(name = 'bounding')

disp = 0.1
bounding.add_node(x=disp,  y=0.0, name = 'top',    dl = False)
bounding.add_node(x=-disp, y=0.0, name = 'bottom', dl = False)
bounding.add_node(x=0.0, y=-disp, name = 'left',   dl = False)
bounding.add_node(x=0.0, y=disp,  name = 'right',  dl = False)

GRAPH = Graph(name = 'graph', graphs = [main, bounding])

CAN = Canvas(border_thickness = 0.0, grid = True)
CAN.add_graph(GRAPH)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
