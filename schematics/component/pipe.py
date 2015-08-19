# component definition
from schematics import Point, Component
from copy import deepcopy

class Pipe(Component):
  Component.stats['Pipe'] = 0


  def _get_label_locations(self):
    self.center = Point()
    self.center.x = 0.5 * self.length
    self.center.y = 0.0

    self.bottom = Point(self.center.x, self.center.y - 0.5 * self.width)
    self.top = Point(self.center.x, self.center.y + 0.5 * self.width)
    self.left = None
    self.right = None


  def _get_nodes(self):
    self.graph.add_node(self.center.x - (0.5 * self.length), self.center.y, name = 'inlet' )
    self.graph.add_node(self.center.x + (0.5 * self.length), self.center.y, name = 'outlet')


  def __init__(self, length, width, center_of_rotation, **kwargs):
    self.length = length
    self.width = width

    super(Pipe, self).__init__(center_of_rotation, **kwargs)

    # define list of points outlining the custom shape
    self._points.append( Point() )
    self._points.append( Point(self.graph.nodes['inlet'].x,  self.top.y) )
    self._points.append( Point(self.graph.nodes['outlet'].x, self._points[1].y) )
    self._points.append( Point(self.graph.nodes['outlet'].x, self.bottom.y) )
    self._points.append( Point(self.graph.nodes['inlet'].x, self.bottom.y) )

    # define connections between points
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )


  def __deepcopy__(self, memo):
    return Pipe(
                deepcopy(self.length, memo),
                deepcopy(self.width, memo),
                deepcopy(self.center_of_rotation, memo),
                n  = deepcopy(self.name, memo),
                ll = deepcopy(self.label_location, memo),
                ls = deepcopy(self.label_string, memo),
                la = deepcopy(self.label_angle, memo),
                lp = deepcopy(self.label_pad, memo),
                fs = deepcopy(self.font_size, memo),
                a = deepcopy(self.angle, memo),
                ref = deepcopy(self.reflect, memo),
                fc = deepcopy(self.face_color, memo),
                ec = deepcopy(self.edge_color, memo),
                lw = deepcopy(self.line_width, memo)
               )

# debugging routine
if __name__ == '__main__':
  from schematics import component_debug_switch
  debugging = component_debug_switch('The component Pipe')

  from schematics import Canvas

  component = Pipe( 1.0, 0.5, Point(0.0, 0.0), name = 'Pipe', a = 0.0,
                   ll = 'top', lp = 1.0, ls = 'Component', la = 0.0, fs = 12
                  )

  CAN = Canvas(border_thickness = 0.05, grid = False)

  CAN.add_component(component)
  CAN.add_graph(component.graph)

  CAN.draw(display = True)
