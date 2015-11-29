from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Simple pipe reflected.')
command_line_parser.parse()

from schematics import Point
from schematics import Canvas
from schematics import Pipe
from schematics import Component

CAN = Canvas(border_thickness = 0.05, grid = True)

print(Component.stats)

CAN.add_component( Pipe(5, 1.0, Point(0.0, 0.0) , label_location = 'center', label_pad = 1.0, name = 'Not reflected', angle = 0.0, label_angle = 0.0) )

CAN.add_component( Pipe(5, 1.0, Point(0.0, 0.0) , label_location = 'bottom', label_pad = 1.0, name = 'Bottom label \n relfect_x', angle = 0.0, label_angle = 0.0, reflect = 'x') )

CAN.add_component( Pipe(5, 1.0, Point(0.0, -2.0) , label_location = 'center', label_pad = 1.0, name = 'Not reflected', angle = 0.0, label_angle = 0.0) )

CAN.add_component( Pipe(5, 1.0, Point(0.0, -2.0) , label_location = 'top', label_pad = 1.0, name = 'Top label \n relfect_x', angle = 0.0, label_angle = 0.0, reflect = 'x') )

print(Component.stats)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
