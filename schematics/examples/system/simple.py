from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('A simple system.')
command_line_parser.parse()

from schematics import Canvas
from schematics import System
from schematics import Pipe
from schematics import Point

simple = System('simple')

simple.add_component(
  Pipe(
    1.0, 0.5, Point(), name = 'Pipe 1', angle = 0.0,
    label_location = 'center', label_pad = 0.0, label_angle = 0.0
  )
)

simple.add_component(
  Pipe(
    1.0, 0.5, Point(1.5, 0.0), name = 'Pipe 2', angle = 0.0,
    label_location = 'center', label_pad = 0.0, label_angle = 0.0
  )
)

simple.connect(
  'Pipe 1:outlet', 'Pipe 2:inlet',
  name = 'Junction 1', label_edge_number = 0, label_location = 'top',
  label_pad = 1.0, label_angle = 0.0, label_shift = 0.0
)

CAN = Canvas(border_thickness = 0.05, grid = True)
CAN.add_system(simple)
CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
