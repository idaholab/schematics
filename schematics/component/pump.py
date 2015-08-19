import math
from schematics import Point, Component

class Pump(Component):
  Component.stats['Pump'] = 0


  def _get_label_locations(self):
    self.center = Point(0.0, 0.0)
    self.left = Point(self.center.x - self.radius, self.center.y)
    self.right = Point(self.center.x + self.radius, self.center.y)
    self.top = None
    self.bottom = None


  def _get_nodes(self):
    self.graph.add_node(self.center.x, self.center.y + (1.5 * self.radius), name = 'inlet' ) # TODO: Incorrect
    self.graph.add_node(self.center.x + (0.5 * self.radius), self.center.y - (0.0 * self.radius), name = 'outlet') # TODO: Incorrect


  def __init__(self, radius, center_of_rotation, **kwargs):
    self.radius = radius

    super(Pump, self).__init__(center_of_rotation, **kwargs)

    displacement = self.radius * 4.0 * (math.sqrt(2.0) - 1.0) / 3.0
    # define list of points outlining the custom shape
    self._points.append( Point(self.left.x, self.left.y) )
    self._points.append( Point(self._points[0].x, self._points[0].y + displacement) )
    self._points.append( Point(self.center.x - displacement, self.center.y + self.radius) )
    self._points.append( Point(self.center.x, self._points[-1].y) )
    self._points.append( Point(self.center.x + displacement, self._points[-1].y) )
    self._points.append( Point(self.center.x + self.radius, self._points[1].y) )
    self._points.append( Point(self.right.x, self.right.y) )
    self._points.append( Point(self.right.x, self.right.y - (1.5 * self.radius)) )
    self._points.append( Point(self.center.x, self._points[-1].y) )
    self._points.append( Point(self.center.x, self.center.y - self.radius))
    self._points.append( Point(self._points[2].x, self._points[-1].y))
    self._points.append( Point(self._points[0].x, self._points[0].y - displacement) )

    # define connections between points
    self._connections.append( 'CURVE4' )
    self._connections.append( 'CuRvE4' )
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    self._connections.append( 'curve4' )
