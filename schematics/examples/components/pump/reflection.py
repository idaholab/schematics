from __future__ import print_function
from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Simple pump reflected.')
command_line_parser.parse()

from schematics import Point
from schematics import Canvas
from schematics import Pump
from schematics import Component

CAN = Canvas(border_thickness = 0.05, grid = True)

print(Component.stats)

CAN.add_component( Pump(0.3, Point(0.0, 0.0), label_location = 'center', name = 'not reflected', label_pad = 0.5, angle = 0))
CAN.add_component( Pump(0.3, Point(1.0, 0.0), label_location = 'right', name = 'relfect_y \nright label', label_pad = 0.5, angle = 0.0, reflect = 'y'))
CAN.add_component( Pump(0.3, Point(2.0, 0.0), label_location = 'left', name = 'relfect_y \nleft label', label_pad = 0.5, angle = 0.0, reflect = 'y'))
CAN.add_component( Pump(0.3, Point(0.0, -1.0), label_location = 'center', name = 'not reflected', label_pad = 0.5, angle = 0.0))

print(Component.stats)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
