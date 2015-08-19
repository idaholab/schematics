from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Display color palettes.')
command_line_parser.parse()

from schematics import Point
from schematics import Canvas
from schematics import Pipe
from schematics import Component

CAN = Canvas(border_thickness = 0.05, grid = False)

print Component.stats
# Reds
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, 3.0), face_color = (0.597659, 0.0, 0.0)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, 3.0), face_color = (0.67578, 0.19531, 0.19531)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, 3.0), face_color = (0.71484, 0.2968, 0.2968)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, 3.0), face_color = (0.7539, 0.3984, 0.3984)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, 3.0), face_color = (0.796875, 0.49609, 0.49609)))
CAN.add_component( Pipe(1.0, 1.0, Point(4.5, 3.0), face_color = (0.8359, 0.5976, 0.5976)))

# Oranges
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, 1.5), face_color = (0.82, 0.36, 0.01)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, 1.5), face_color = (0.83, 0.43, 0.11)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, 1.5), face_color = (0.85, 0.49, 0.20)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, 1.5), face_color = (0.87, 0.55, 0.30)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, 1.5), face_color = (0.89, 0.62, 0.40)))
CAN.add_component( Pipe(1.0, 1.0, Point(4.5, 1.5), face_color = (0.91, 0.68, 0.50)))

# Yellows
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, 0.0), face_color = (0.98, 0.79, 0.00)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, 0.0), face_color = (0.98, 0.81, 0.10)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, 0.0), face_color = (0.98, 0.83, 0.20)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, 0.0), face_color = (0.98, 0.85, 0.30)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, 0.0), face_color = (0.98, 0.87, 0.40)))
CAN.add_component( Pipe(1.0, 1.0, Point(4.5, 0.0), face_color = (0.99, 0.89, 0.50)))

# Greens
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, -1.5), face_color = (0.0351, 0.34375, 0.0703)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, -1.5), face_color = (0.1289, 0.40625, 0.1601)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, -1.5), face_color = (0.22656, 0.4726, 0.2539)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, -1.5), face_color = (0.3203, 0.5391, 0.3476)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, -1.5), face_color = (0.41797, 0.6015, 0.4375)))
CAN.add_component( Pipe(1.0, 1.0, Point(4.5, -1.5), face_color = (0.5156, 0.66796, 0.53125)))

# Blues
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, -3.0), face_color = (0.0, 0.0, 0.597659)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, -3.0), face_color = (0.19531, 0.19531, 0.67578)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, -3.0), face_color = (0.2968, 0.2968, 0.71484)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, -3.0), face_color = (0.3984, 0.3984, 0.7539)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, -3.0), face_color = (0.49609, 0.49609, 0.796875)))
CAN.add_component( Pipe(1.0, 1.0, Point(4.5, -3.0), face_color = (0.5976, 0.5976, 0.8359)))

# Purples
CAN.add_component( Pipe(1.0, 1.0, Point(-3.0, -4.5), face_color = (0.30, 0.12, 0.40)))
CAN.add_component( Pipe(1.0, 1.0, Point(-1.5, -4.5), face_color = (0.37, 0.20, 0.46)))
CAN.add_component( Pipe(1.0, 1.0, Point(0.0, -4.5), face_color = (0.44, 0.29, 0.52)))
CAN.add_component( Pipe(1.0, 1.0, Point(1.5, -4.5), face_color = (0.51, 0.38, 0.58)))
CAN.add_component( Pipe(1.0, 1.0, Point(3.0, -4.5), face_color = (0.58, 0.47, 0.64)))
CAN.add_component( Pipe(1.0, 1.0, Point(4.5, -4.5), face_color = (0.65, 0.56, 0.70)))

print Component.stats

CAN.draw(save_file = None, display = True, print_information = False)
