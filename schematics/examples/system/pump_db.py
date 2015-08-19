from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('A simple system.')
command_line_parser.parse()

from schematics import Canvas
from schematics import System
from schematics import Pipe
from schematics import Pump
from schematics import CoreChannel
from schematics import Point

tmi = System('tmi')

radius = 1.0
px = 0.0
py = 0.0
y = (0.5 * radius) + py
x = (3.0 * radius) + px
tmi.add_node(x, y, name = 'outlet')

PumpA = Pump(radius, Point(px, py), name = 'Pump', ref = None, angle = 90.0, label_angle = 0.0)
tmi.add_component(PumpA)

tmi.connect('Pump:outlet', 'outlet')


CAN = Canvas(border_thickness = 0.05, grid = True)
CAN.add_system(tmi)

CAN.draw(save_file = 'tmi.pdf', display = True)
