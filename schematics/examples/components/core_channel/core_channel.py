from __future__ import print_function
from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Simple core channel.')
command_line_parser.parse()

from schematics import Point
from schematics import Canvas
from schematics import CoreChannel
from schematics import Component

CAN = Canvas(border_thickness = 0.05, grid = False)

print(Component.stats)

CAN.add_component( CoreChannel(1.0, 3.0, Point(-3.0, 0.0), label_location='left', name='left \nreflect_y', label_pad = 0.25, angle=0.0, reflect = 'y', face_color = (0.6875, .1953, 0.1875, 1.0)))
CAN.add_component( CoreChannel(1.0, 3.0, Point(0.0, 0.0), label_location='center', name='center', label_pad = 0.25, angle=0.0, face_color = (0.5, 0.2266, 0.5703, 1.0)))
CAN.add_component( CoreChannel(1.0, 3.0, Point(3.0, 0.0), label_location='right', name='right \nreflect_y', label_pad = 0.25, angle=0.0, reflect = 'y', face_color = (0.9961, 0.8320, 0.0, 1.0)))

print(Component.stats)

CAN.draw(save_file = None, display = True, print_information = False)
