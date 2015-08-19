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

spacing = 0.2
core_channel_width = 0.5
core_channel_height = 2.0
pipe_width = 0.4

# Core
x = 1.5 * (- core_channel_width - spacing)
y = 0.0
CH1 = CoreChannel(
        core_channel_width, core_channel_height,
        Point(x, y),
        name = 'CH1',
        label_angle = 90.0
     )
tmi.add_component(CH1)

x += core_channel_width + spacing
CH2 = CoreChannel(
        core_channel_width, core_channel_height,
        Point(x, y),
        name = 'CH2',
        label_angle = 90.0
      )
tmi.add_component(CH2)

x += core_channel_width + spacing
CH3 = CoreChannel(
        core_channel_width, core_channel_height,
        Point(x, y),
        name = 'CH3',
        label_angle = 90.0
      )
tmi.add_component(CH3)

x += core_channel_width + spacing
Bypass = Pipe(
           core_channel_height, pipe_width,
           Point(x, y),
           name = 'bypass_pipe', a = 90.0
          )
tmi.add_component(Bypass)

length = 2.0
x += core_channel_width + spacing
y = length
DowncomerA = Pipe(
    2.0, pipe_width,
    Point(x, y),
    name = 'DownComer-A', a = -90.0
)
tmi.add_component(DowncomerA)

x *= -1.0
y = length
DowncomerB = Pipe(
    length, pipe_width,
    Point(x, y),
    name = 'DownComer-B', a = -90.0
)
tmi.add_component(DowncomerB)

# Lower Plenum Nodes
x = DowncomerA.center_of_rotation.x
y = -0.6
tmi.add_node(x, y, name = 'DownComer-A:LowerPlenum')

x = DowncomerB.center_of_rotation.x
tmi.add_node(x, y, name = 'DownComer-B:LowerPlenum')

x = 0.0
tmi.add_node(x, y, name = 'LowerPlenum1')
y = -0.3
tmi.add_node(x, y, name = 'LowerPlenum2')

x = Bypass.center_of_rotation.x
tmi.add_node(x, y, name = 'bypass_pipe:LowerPlenum')

x = CH1.center_of_rotation.x
tmi.add_node(x, y, name = 'CH1:LowerPlenum')

x = CH2.center_of_rotation.x
tmi.add_node(x, y, name = 'CH2:LowerPlenum')

x = CH3.center_of_rotation.x
tmi.add_node(x, y, name = 'CH3:LowerPlenum')

# Lower Plenum Connections
tmi.connect(
  'DownComer-B:outlet', 'DownComer-B:LowerPlenum', 'LowerPlenum1', 'LowerPlenum2', 'CH1:LowerPlenum', 'CH1:inlet'
)

tmi.connect(
  'DownComer-B:outlet', 'DownComer-B:LowerPlenum', 'LowerPlenum1', 'LowerPlenum2', 'CH2:LowerPlenum', 'CH2:inlet'
)

tmi.connect(
  'DownComer-A:outlet', 'DownComer-A:LowerPlenum', 'LowerPlenum1', 'LowerPlenum2', 'CH3:LowerPlenum', 'CH3:inlet'
)

tmi.connect(
  'DownComer-A:outlet', 'DownComer-A:LowerPlenum', 'LowerPlenum1', 'LowerPlenum2', 'bypass_pipe:LowerPlenum', 'bypass_pipe:inlet',
  name = 'LowerPlenum', label_edge_number = 1, label_location = 'bottom',
  label_pad = 1.0, label_angle = 0.0, label_shift = 1.0
)

# Hot Leg pipes
x = DowncomerA.center_of_rotation.x
y = core_channel_height + 1.2
Pipe1HLA = Pipe(2.0, pipe_width, Point(x, y), name = 'pipe1-HL-A', ref = None, angle = 90.0)
tmi.add_component(Pipe1HLA)

x *= -1.0
Pipe1HLB = Pipe(2.0, pipe_width, Point(x, y), name = 'pipe1-HL-B', ref = 'y', angle = -90.0)
tmi.add_component(Pipe1HLB)

# Upper Plenum Nodes
x = Bypass.center_of_rotation.x
y = core_channel_height + 0.4
tmi.add_node(x, y, name = 'bypass_pipe:UpperPlenum')

x = CH1.center_of_rotation.x
tmi.add_node(x, y, name = 'CH1:UpperPlenum')

x = CH2.center_of_rotation.x
tmi.add_node(x, y, name = 'CH2:UpperPlenum')

x = CH3.center_of_rotation.x
tmi.add_node(x, y, name = 'CH3:UpperPlenum')

x = 0.0
tmi.add_node(x, y, name = 'UpperPlenum1')

y += 0.4
tmi.add_node(x, y, name = 'UpperPlenum2')

x = Pipe1HLA.center_of_rotation.x
tmi.add_node(x, y, name = 'pipe1-HL-A:UpperPlenum')

x *= -1.0
tmi.add_node(x, y, name = 'pipe1-HL-B:UpperPlenum')

# Upper Plenum Connections
tmi.connect(
  'CH1:outlet', 'CH1:UpperPlenum', 'UpperPlenum1', 'UpperPlenum2', 'pipe1-HL-B:UpperPlenum', 'pipe1-HL-B:inlet'
)

tmi.connect(
  'CH2:outlet', 'CH2:UpperPlenum', 'UpperPlenum1', 'UpperPlenum2', 'pipe1-HL-B:UpperPlenum', 'pipe1-HL-B:inlet'
)

tmi.connect(
  'CH3:outlet', 'CH3:UpperPlenum', 'UpperPlenum1', 'UpperPlenum2', 'pipe1-HL-A:UpperPlenum', 'pipe1-HL-A:inlet'
)

tmi.connect(
  'bypass_pipe:outlet', 'bypass_pipe:UpperPlenum', 'UpperPlenum1', 'UpperPlenum2', 'pipe1-HL-A:UpperPlenum', 'pipe1-HL-A:inlet',
  name = 'UpperPlenum', label_edge_number = 3, label_location = 'bottom',
  label_pad = 1.0, label_angle = 0.0, label_shift = -1.0
)

# Cold Leg pipes
length = 2.0
x = DowncomerA.center_of_rotation.x + pipe_width + length
y = core_channel_height + 0.3
Pipe1CLA = Pipe(length, pipe_width, Point(x, y), name = 'pipe1-CL-A', ref = 'y')
tmi.add_component(Pipe1CLA)

x *= -1.0
Pipe1CLB = Pipe(length, pipe_width, Point(x, y), name = 'pipe1-CL-B', ref = None)
tmi.add_component(Pipe1CLB)

# Cold Leg Nodes
x = DowncomerA.center_of_rotation.x
y = Pipe1CLA.center_of_rotation.y
tmi.add_node(x, y, name = 'Branch2-A')

x = DowncomerB.center_of_rotation.x
tmi.add_node(x, y, name = 'Branch2-B')

# Cold Leg Connections
tmi.connect(
  'pipe1-CL-A:outlet', 'Branch2-A', 'DownComer-A:inlet',
  name = 'Branch2-A', label_edge_number = 0, label_location = 'top',
  label_pad = 0.75, label_angle = 0.0, label_shift = 2.0
)

tmi.connect(
  'pipe1-CL-B:outlet', 'Branch2-B', 'DownComer-B:inlet',
  name = 'Branch2-B', label_edge_number = 0, label_location = 'bottom',
  label_pad = 0.75, label_angle = 0.0, label_shift = 2.0
)

# Pump
radius = pipe_width
spacing = 0.5
x = Pipe1CLA.center_of_rotation.x + spacing + (1.5 * radius)
y = Pipe1CLA.center_of_rotation.y - (0.5 * radius)
PumpA = Pump(radius, Point(x, y), name = 'Pump-A', ref = 'x', angle = 90.0, label_angle = 90.0, label_location = 'left')
tmi.add_component(PumpA)

tmi.connect('Pump-A:outlet', 'pipe1-CL-A:inlet')

x *= -1.0
PumpB = Pump(radius, Point(x, y), name = 'Pump-B', ref = None, angle = 90.0, label_angle = -90.0, label_location = 'left')
tmi.add_component(PumpB)

tmi.connect('Pump-B:outlet', 'pipe1-CL-B:inlet')

# More Cold Leg Pipes
length = 2.0
x = PumpA.center_of_rotation.x + radius + length + spacing
y = PumpA.center_of_rotation.y
Pipe2CLA = Pipe(length, pipe_width, Point(x, y), name = 'pipe2-CL-A', ref = 'y')
tmi.add_component(Pipe2CLA)

tmi.connect('pipe2-CL-A:outlet', 'Pump-A:inlet')

x *= -1.0
Pipe2CLB = Pipe(length, pipe_width, Point(x, y), name = 'pipe2-CL-B', ref = None)
tmi.add_component(Pipe2CLB)

tmi.connect('pipe2-CL-B:outlet', 'Pump-B:inlet')

# More Hot Leg Pipes
x = Pipe1CLA.center_of_rotation.x - length
y = Pipe1HLA.center_of_rotation.y + 0.2 + length
Pipe2HLA = Pipe(length, pipe_width, Point(x, y), name = 'pipe2-HL-A', angle = 0.0)
tmi.add_component(Pipe2HLA)

x *= -1.0
Pipe2HLB = Pipe(length, pipe_width, Point(x, y), name = 'pipe2-HL-B', angle = 0.0, ref = 'y')
tmi.add_component(Pipe2HLB)

x = Pipe1HLA.center_of_rotation.x
tmi.add_node(x, y, name = 'scafold1')
tmi.connect('pipe1-HL-A:outlet', 'scafold1', 'pipe2-HL-A:inlet')

x = Pipe1HLB.center_of_rotation.x
tmi.add_node(x, y, name = 'scafold2')
tmi.connect('pipe1-HL-B:outlet', 'scafold2', 'pipe2-HL-B:inlet')

# primary heat exchanger
hx_length = length * 1.5
hx_width = pipe_width * 2.0
x = Pipe2HLA.center_of_rotation.x + (2.0 * length)
y = Pipe2HLA.center_of_rotation.y + (hx_length - length)
HXA = Pipe(hx_length, hx_width, Point(x, y), name = 'HX-A(primary)', angle = -90.0)
tmi.add_component(HXA)

x *= -1.0
HXB = Pipe(hx_length, hx_width, Point(x, y), name = 'HX-B(primary)', angle = -90.0)
tmi.add_component(HXB)

# hotleg connection to heat exchanger
x = Pipe2HLA.center_of_rotation.x + length + 0.4
y = Pipe2HLA.center_of_rotation.y
tmi.add_node(x, y, name = 'Branch3-A:1')
tmi.add_node(-1.0 * x, y, name = 'Branch3-B:1')

y = HXA.center_of_rotation.y + 0.4
tmi.add_node(x, y, name = 'Branch3-A:2')
tmi.add_node(-1.0 * x, y, name = 'Branch3-B:2')

x = HXA.center_of_rotation.x
tmi.add_node(x, y, name = 'Branch3-A:3')
tmi.add_node(-1.0 * x, y, name = 'Branch3-B:3')

tmi.connect(
  'pipe2-HL-A:outlet', 'Branch3-A:1', 'Branch3-A:2', 'Branch3-A:3', 'HX-A(primary):inlet',
  name = 'Branch3-A', label_edge_number = 1, label_location = 'bottom',
  label_pad = 1.0, label_angle = 0.0, label_shift = 1.0
)

tmi.connect(
  'pipe2-HL-B:outlet', 'Branch3-B:1', 'Branch3-B:2', 'Branch3-B:3', 'HX-B(primary):inlet',
  name = 'Branch3-B', label_edge_number = 1, label_location = 'top',
  label_pad = 1.0, label_angle = 0.0, label_shift = 1.0
)

# coldleg connection to heat exchanger
x = HXA.center_of_rotation.x
y = HXA.center_of_rotation.y - hx_length - 0.4
tmi.add_node(x, y, name = 'Branch6-A:1')
tmi.add_node(-1.0 * x, y, name = 'Branch6-B:1')

x = Pipe2CLA.center_of_rotation.x + 0.4
tmi.add_node(x, y, name = 'Branch6-A:2')
tmi.add_node(-1.0 * x, y, name = 'Branch6-B:2')

y = Pipe2CLA.center_of_rotation.y
tmi.add_node(x, y, name = 'Branch6-A:3')
tmi.add_node(-1.0 * x, y, name = 'Branch6-B:3')

tmi.connect(
  'HX-A(primary):outlet', 'Branch6-A:1', 'Branch6-A:2', 'Branch6-A:3', 'pipe2-CL-A:inlet',
  name = 'Branch6-A', label_edge_number = 1, label_location = 'bottom',
  label_pad = 1.0, label_angle = 0.0, label_shift = 1.0
)

tmi.connect(
  'HX-B(primary):outlet', 'Branch6-B:1', 'Branch6-B:2', 'Branch6-B:3', 'pipe2-CL-B:inlet',
  name = 'Branch6-B', label_edge_number = 1, label_location = 'top',
  label_pad = 1.0, label_angle = 0.0, label_shift = 1.0
)


# draw
CAN = Canvas(border_thickness = 0.0, grid = False)
CAN.add_system(tmi)

CAN.draw(save_file = 'tmi.pdf', display = True)
