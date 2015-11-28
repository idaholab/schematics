from __future__ import print_function
from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Simple Pipe.')
command_line_parser.parse()

from schematics import Point
from schematics import Canvas
from schematics import Pipe
from schematics import Component

CAN = Canvas(border_thickness = 0.05, grid = True)

print(Component.stats)

CAN.add_component( Pipe(0.75, 0.3, Point(1.0, 1.0), name = 'Component', a = 0.0,
                        ll = 'bottom', lp = 1.0, la = 0.0,
                        fs = 10
                       )
                 )

# CAN.add_component( Pipe(0.75, 0.3, Point(-1.0, -1.0), name = '-90 degrees', a = -90.0,
#                         ll = 'top', lp = 1.0, la = 0.0
#                        )
#                  )
#
# CAN.add_component( Pipe(0.75, 0.3, Point(0.0, -1.0), name = '-45 degrees', a = -45.0,
#                         ll = 'top', lp = 1.0, la = 0.0
#                        )
#                  )
#
# CAN.add_component( Pipe(0.75, 0.3, Point(1.0, -1.0), name = '0 degrees', a = 0.0,
#                         ll = 'top', lp = 1.0, la = 0.0
#                        )
#                  )
#
# CAN.add_component( Pipe(0.75, 0.3, Point(2.0, -1.0), name = '45 degrees', a = 45.0,
#                         ll = 'top', lp = 1.0, la = 0.0
#                        )
#                  )
#
# CAN.add_component( Pipe(0.75, 0.3, Point(3.0, -1.0), name = '90 degrees', a = 90.0,
#                         ll = 'top', lp = 1.0, la = 0.0
#                        )
#                  )
#
# CAN.add_component( Pipe(5, 0.025, Point(-1.0, -3.0), name = 'long-skinny', a = 0.0,
#                         ll = 'top', lp = 1.0, la = 0.0
#                        )
#                  )

print(Component.stats)

CAN.draw(save_file = 'test.pdf', display = True, print_information = False)
