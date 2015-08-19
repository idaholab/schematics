from schematics import Point, Component


class CoreChannel(Component):
  Component.stats['CoreChannel'] = 0

  def _get_label_locations(self):
    self.center = Point()
    self.center.x = 0.0
    self.center.y = 0.5 * self.height
    self.bottom = None
    self.top = None
    self.left = Point(self.center.x - (0.5 * self.width), self.center.y)
    self.right = Point(self.center.x + (0.5 * self.width), self.center.y)


  def _get_nodes(self):
    self.graph.add_node(self.center.x, self.center.y - (0.5 * self.height), name = 'inlet' )
    self.graph.add_node(self.center.x, self.center.y + (0.5 * self.height), name = 'outlet')


  def __init__(self, width, height, center_of_rotation, flow_channel_percent = 0.75, **kwargs):

    self.height = height
    self.width = width
    self.flow_channel_percent = flow_channel_percent

    super(CoreChannel, self).__init__(center_of_rotation, **kwargs)

    # define list of points outlining the shape of the component
    self._points.append( Point(self.left.x + (flow_channel_percent * self.width), self.graph.nodes['inlet'].y) )
    self._points.append( Point(self.left.x, self._points[-1].y) )
    self._points.append( Point(self._points[-1].x, self.graph.nodes['outlet'].y) )
    self._points.append( Point(self._points[0].x, self._points[-1].y) )
    self._points.append( Point(self._points[0].x, self._points[0].y) )
    # Heat Structure
    self._points.append( Point(self._points[0].x, self._points[-2].y) )
    self._points.append( Point(self.right.x, self._points[-1].y) )
    self._points.append( Point(self.right.x, self._points[0].y) )

    # define connections between points
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    # Heat Structure
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
    self._connections.append( 'lineto' )
