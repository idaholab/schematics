from __future__ import print_function
from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Display color palettes.')
command_line_parser.parse()

from schematics import Point
from schematics import Canvas
from schematics import Pipe
from schematics import Component

CAN = Canvas(border_thickness = 0.05, grid = False)

print(Component.stats)
# RAINBOW
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, 4.5), label_location = 'left', label_string = 'Rainbow', face_color = (0.6875, .1953, 0.1875)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, 4.5), face_color = (0.8825, 0.4170, 0.1445)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, 4.5), face_color = (0.9961, 0.8320, 0.0)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, 4.5), face_color = (0.125, 0.4101, 0.1445)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, 4.5), face_color = (0.1758, 0.203, 0.7461)))
CAN.add_component( Pipe(1.0, 1.0, Point(4.5, 4.5), face_color = (0.5, 0.2266, 0.5703)))

# Fantastic Mr. Fox
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, 3.0), label_location = 'left', label_string = 'Fantastic\n Mr. Fox', face_color = (0.8633, 0.5508, 0.1602)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, 3.0), face_color = (0.8828, 0.8203, 0.0)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, 3.0), face_color = (0.27343, 0.67187, 0.78125)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, 3.0), face_color = (0.894531, 0.5234, 0.00391)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, 3.0), face_color = (0.7031, 0.05859, 0.125)))
CAN.add_component( Pipe(1.0, 1.0, Point(4.5, 3.0), face_color = (0.9531, 0.9179, 0.8008)))

# Beachy Time
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, 0.0), label_location = 'left', label_string = 'Beachy\nTime', face_color = (0.59, 0.81, 0.71)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, 0.0), face_color = (1.00, 0.93, 0.68)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, 0.0), face_color = (1.00, 0.44, 0.41)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, 0.0), face_color = (1.00, 0.80, 0.36)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, 0.0), face_color = (0.53, 0.85, 0.69)))
# CAN.add_component( Pipe(1.0, 1.0, Point(4.5, 0.0), face_color = (, 1.0)))

# Griffindor
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, -1.5), label_location = 'left', label_string = 'Griffindor', face_color = (0.45, 0.00, 0.00)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, -1.5), face_color = (0.68, 0.00, 0.00)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, -1.5), face_color = (0.93, 0.73, 0.19)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, -1.5), face_color = (0.83, 0.65, 0.15)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, -1.5), face_color = (0.0, 0.0, 0.0)))
# CAN.add_component( Pipe(1.0, 1.0, Point(4.5, -1.5), face_color = (1.0, 1.0, 1.0, 1.0)))

# Summertime Loving, Loving in the Summer (Time)
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, -3.0), label_location = 'left', label_string = 'Summertime Loving,\nLoving in the Summer\n(Time)', label_pad = 0.25, face_color = (1.00, 0.75, 0.31)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, -3.0), face_color = (0.42, 0.82, 0.86)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, -3.0), face_color = (0.05, 0.65, 0.71)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, -3.0), face_color = (0.05, 0.27, 0.49)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, -3.0), face_color = (0.91, 0.44, 0.16)))
# CAN.add_component( Pipe(1.0, 1.0, Point(4.5, -3.0), face_color = ()))

# Winters
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, -4.5), label_location = 'left', label_string = 'Winters', face_color = (0.24, 0.39, 0.36)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, -4.5), face_color = (0.27, 0.08, 0.28)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, -4.5), face_color = (0.82, 0.83, 0.75)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, -4.5), face_color = (0.02, 0.00, 0.22)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, -4.5), face_color = (0.48, 0.48, 0.48)))
# CAN.add_component( Pipe(1.0, 1.0, Point(4.5, -4.5), face_color = ()))

# The Monarch's Lair
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, -6.0), label_location = 'left', label_string = "The Monarch's Lair", face_color = (0.64, 0.05, 0.71)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, -6.0), face_color = (0.95, 0.63, 0.15)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, -6.0), face_color = (0.98, 0.79, 0.00)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, -6.0), face_color = (0.64, 0.04, 0.49)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, -6.0), face_color = (0.91, 0.71, 0.86)))

print(Component.stats)

CAN.draw(save_file = None, display = True, print_information = False)
