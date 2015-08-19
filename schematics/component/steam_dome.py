import math
from schematics import Point, Component

class SteamDome(Component):
  Component.stats['SteamDome'] = 0

  def _get_label_locations(self):
    self.center = Point(0.0, 0.5 * self.height)
    self.left = Point(self.center.x - 0.5 * self.width, self.center.y)
    self.right = Point(self.center.x + 0.5 * self.width, self.center.y)
    self.top = Point(self.center.x, self.center.y + 0.5 * self.height)
    self.bottom = None


  def _get_nodes(self):
    self.graph.add_node(self.center.x, self.center.y - 0.5 * self.height, name = 'inlet' )


  def __init__(self, width, center_of_rotation, **kwargs):
    aspect_ratio = 1.0 / 3.0
    self.width = width
    self.height = aspect_ratio * self.width

    super(SteamDome, self).__init__(center_of_rotation, **kwargs)

    displacement = self.height * 4.0 * (math.sqrt(2.0) - 1.0) / 3.0
    # define list of points outlining the custom shape
    self._points.append( Point(self.graph.nodes['inlet'].x, self.graph.nodes['inlet'].y) )
    self._points.append( Point(self.left.x, self._points[-1].y) )
    self._points.append( Point(self.left.x, self._points[-1].y + displacement) )
    self._points.append( Point(self.top.x - displacement, self.top.y) )
    self._points.append( Point(self.top.x, self.top.y) )
    self._points.append( Point(self.top.x + displacement, self.top.y) )
    self._points.append( Point(self.right.x, self._points[2].y) )
    self._points.append( Point(self.right.x, self.graph.nodes['inlet'].y) )

    self._connections.append( 'lineto' )
    self._connections.append( 'CURVE4' )
    self._connections.append( 'CuRvE4' )
    self._connections.append( 'lineto' )
