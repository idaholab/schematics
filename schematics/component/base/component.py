import sys

import matplotlib.patches as mpatches
import matplotlib.path as mpath

from schematics import Point
from schematics import Transformation
from schematics import Label
from schematics import Graph

from schematics import process_name
from schematics import process_face_color
from schematics import process_edge_color
from schematics import process_line_width


class Component(Label, Transformation):
  stats = {}

  def _connect_nodes(self):
    connected_pairs = []
    for node0 in self.graph.nodes.keys():
      for node1 in self.graph.nodes.keys():
        if node0 != node1:
          pair0 = (node0, node1)
          pair1 = (node1, node0)
          if pair0 not in connected_pairs and pair1 not in connected_pairs:
            connected_pairs.append(pair0)
            self.graph.connect(node0, node1, directional = False)


  def __init__(self, center_of_rotation, **kwargs):
    Component.stats[self.__class__.__name__] += 1

    super(Component, self).__init__(center_of_rotation, **kwargs)
    Transformation.__init__(self, center_of_rotation, **kwargs)

    self.name = process_name(None, kwargs)
    self.label_string = self.name

    self.graph = Graph(name = self.name)
    self._get_nodes()
    self._connect_nodes()

    self.face_color = process_face_color((1.0, 1.0, 1.0), kwargs)
    self.edge_color = process_edge_color((0.0, 0.0, 0.0), kwargs)
    self.line_width = process_line_width(1.5, kwargs)
    self.patch = None

    self._points = []
    self._connections = []


  def _get_path_data(self):
    Path = mpath.Path
    self._path_data = [(Path.MOVETO, self._points[0].to_tuple())]
    point_index = 0
    last_point_index = len(self._points) - 1
    last_connection_index = len(self._connections) - 1

    for connection_index, connection in enumerate(self._connections):
      connection = connection.lower()
      # Line
      if connection == 'lineto':
        point_index += 1
        if point_index <= last_point_index:
          self._path_data.append( (Path.LINETO, self._points[point_index].to_tuple()) )
        elif connection_index == last_connection_index:
          self._path_data.append( (Path.LINETO, self._points[0].to_tuple()) )
        else:
          sys.exit("Error: Incorrect point and connection specification in custom" +
                   "shape component " + self.__class__.__name__ + ". Ran out of " +
                   "points before all connections could be made.")

      # Quadratic Bezier Curve
      elif connection == 'curve3':
        for i in range(2):
          point_index += 1
          if point_index <= last_point_index:
            self._path_data.append( (Path.CURVE4, self._points[point_index].to_tuple()) )
          elif (connection_index == last_connection_index) and (i == 1):
            self._path_data.append( (Path.CURVE4, self._points[0].to_tuple()) )
          else:
            sys.exit("Error: Incorrect point and connection specification in custom" +
                     "shape component " + self.__class__.__name__ + ". Ran out of " +
                     "points before all connections could be made.")

      # Cubic Bezier Curve
      elif connection == 'curve4':
        for i in range(3):
          point_index += 1
          if point_index <= last_point_index:
            self._path_data.append( (Path.CURVE4, self._points[point_index].to_tuple()) )
          elif (connection_index == last_connection_index) and (i == 2):
            self._path_data.append( (Path.CURVE4, self._points[0].to_tuple()) )
          else:
            sys.exit("Error: Incorrect point and connection specification in custom" +
                     "shape component " + self.__class__.__name__ + ". Ran out of " +
                     "points before all connections could be made.")

      else:
        sys.exit("Error: Invalid connection specification in custom shape component "
                 + self.__class__.__name__ + ".")

      if connection_index == last_connection_index:
        if point_index != len(self._points):
          sys.exit("Error: Incorrect point and connection specification in custom" +
                   "shape component " + self.__class__.__name__ + ". Too many points " +
                   "specified for the connection types.")

    self._path_data.append( (Path.CLOSEPOLY, self._points[0].to_tuple()) )


  def move(self, x, y):
    self.center_of_rotation.x = x
    self.center_of_rotation.y = y


  def _get_shape(self):
    for point in self._points:
      self._reflect(point)
      self._rotate(point)

    self._get_path_data()

    self._codes, self._verts = zip(*self._path_data)
    self.path = mpath.Path(self._verts, self._codes)


  def draw_component(self):
    self._get_shape()
    self.graph.move(self.center_of_rotation.x, self.center_of_rotation.y)
    self.graph.reflect(self.reflect)
    self.graph.rotate(self.angle)

    self.patches = [mpatches.PathPatch(self.path, facecolor = self.face_color, edgecolor = self.edge_color, linewidth = self.line_width)]
    return self.patches


# Error messages
  def _get_nodes(self):
    sys.exit('Error: Must define "_get_nodes" method in the ' + self.__class__.__name__ + ' class.')
    # relative to the center of rotation.
