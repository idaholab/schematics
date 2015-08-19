from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Compounded graph test case.')
command_line_parser.parse()

from schematics import Graph
from schematics import Canvas


# ------------- pipe1

pipe1 = Graph(name = 'pipe1')

pipe1.add_node(x=0.0, y=0.0, name = 'inlet')
pipe1.add_node(1.0, 0.0, name = 'outlet')

# pipe1.connect('inlet', 'outlet', name = 'internal', directional = False)

pipe1.anchor = 'inlet'


# ------------- pipe2

pipe2 = pipe1.copy(x=1.5, y=0.0, name = 'pipe2')

pipe2.anchor = 'inlet'


# ------------- long_pipe1

long_pipe1 = Graph(name = 'long_pipe1', graphs = [pipe1, pipe2])

long_pipe1.connect('pipe1:outlet', 'pipe2:inlet', name = "junction", la = 0.0)
long_pipe1.connect('pipe1:inlet', 'pipe1:outlet', name = "internal-connection1", directional = False, la = 0.0)
long_pipe1.connect('pipe2:inlet', 'pipe2:outlet', name = "internal-connection2", directional = False, la = 0.0)


# ------------- long_pipe2

long_pipe2 = long_pipe1.copy(x=2.5, y=1.0, name = 'long_pipe2')
long_pipe2.reflect(axis = 'y')
long_pipe2.edges["junction"].label_location = 'top'
long_pipe2.edges["internal-connection1"].label_location = 'top'
long_pipe2.edges["internal-connection2"].label_location = 'top'


# ------------- circuit1

circuit1 = Graph(name = 'circuit1', graphs = [long_pipe1, long_pipe2])

circuit1.connect('long_pipe1:pipe2:outlet', 'long_pipe2:pipe1:inlet', name = "junction1")
circuit1.connect('long_pipe2:pipe2:outlet', 'long_pipe1:pipe1:inlet', name = "junction2")


# ------------- circuit2

circuit2 = circuit1.copy(name = 'circuit2')
circuit2.move(x=3.0, y=3.0)
circuit2.rotate(angle = 45.0)


# ------------- super graph

super_graph = Graph(name = 'super', graphs = [circuit1, circuit2])

# print super_graph, '\n' * 2
# print super_graph.general_info()


# ------------- PLOTTING

CAN = Canvas(border_thickness = 0.05, grid = True)
CAN.add_graph(super_graph)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
