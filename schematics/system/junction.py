from schematics import Label
from schematics import Point

from math import pi, cos, sin, atan
RADIANS_PER_DEGREE = 180.0 / pi

from schematics import process_label_edge_number
from schematics import process_label_location
from schematics import process_label_shift
from schematics import process_name
from schematics import process_reflect

class Junction(Label):

  def _get_label_locations(self):
    self.center = Point()
    self.top = Point()
    self.bottom = Point()
    self.left = None
    self.right = None


  def __init__(self, junction_edges, **kwargs):
    self.junction_edges = junction_edges
    self.label_edge_number = process_label_edge_number(0, kwargs)
    self.labeled_edge = self.junction_edges[self.label_edge_number]
    self.label_location = process_label_location('top', kwargs)
    self.label_shift = process_label_shift(0.0, kwargs)
    self.name = process_name(None, kwargs)
    super(Junction, self).__init__(Point(0.0, 0.0), ll = self.label_location, **kwargs)
    self.label_string = self.name
    self.reflect = process_reflect(None, kwargs)
    self.angle = None


  def get_angle(self, tail_coords, head_coords):
    triangle = head_coords - tail_coords
    if triangle.x > 0.0:
      self.angle = RADIANS_PER_DEGREE * atan(triangle.y / triangle.x)

    elif triangle.x < 0.0:
      self.angle = 180.0 + ( RADIANS_PER_DEGREE * atan(triangle.y / triangle.x) )

    else:
      if triangle.y > 0.0:
        self.angle = 90.0
      elif triangle.y < 0.0:
        self.angle = 270.0
      else:
        sys.exit('Error: cannot connect a node to itself. The head and ' +
                 'tail coordinates are identicle. (' + str(self) + ')')

    super(Junction, self)._get_angle_in_radians()


  def draw_label(self, tail_coords, head_coords, **kwargs):
    self.label_shift = process_label_shift(self.label_shift, kwargs)

    self.center_of_rotation.x = 0.5 * (tail_coords.x + head_coords.x)
    self.center_of_rotation.y = 0.5 * (tail_coords.y + head_coords.y)

    if self.angle == None:
      self.get_angle(tail_coords, head_coords)

    length = abs(tail_coords - head_coords)
    self.center_of_rotation.x += self.label_shift * 0.5 * length * cos(self._angle_radians)
    self.center_of_rotation.y += self.label_shift * 0.5 * length * sin(self._angle_radians)

    super(Junction, self).draw_label()
    return self.label


  def _get_actual_label_position(self, label_dimensions):
    self._label_coordinates = Point(self.center.x, self.center.y)

    if self.label_location == 'bottom' or self.label_location == 'top':

      if self.reflect == 'x':
        self.label_angle *= -1.0
      elif self.reflect == 'y':
        self.label_angle *= -1.0

      # calculate padding
      padding_angle = (pi * (self.angle - self.label_angle)) / 180.0
      padding = abs( 0.5 * cos(padding_angle) )
      padding = (self.label_pad + padding) * label_dimensions.height
      padding += abs( 0.5 * label_dimensions.width * sin(padding_angle) )

      # determine label coordinates
      if self.label_location == 'top':
        self._label_coordinates.y = self.bottom.y - padding
      else:
        self._label_coordinates.y = self.top.y + padding

    self._rotate(self._label_coordinates)


  def adjust_label(self, label_dimensions):
    self._get_actual_label_position(label_dimensions)
    self.label.set_x(self._label_coordinates.x)
    self.label.set_y(self._label_coordinates.y)
    self.label.set_rotation(self.label_angle)
