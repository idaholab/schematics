import sys
from copy import deepcopy
from weakref import WeakValueDictionary
from matplotlib.patches import FancyArrow
from math import pi, cos, sin, atan

RADIANS_PER_DEGREE = 180.0 / pi

from schematics import Point
from schematics import Label

from schematics import process_directional

from schematics import process_label_angle
from schematics import process_label_pad
from schematics import process_font_size
from schematics import process_label_location
from schematics import process_label_shift
from schematics import process_font_size

from schematics import process_draw
from schematics import process_draw_label

from schematics import process_reflect
from schematics import process_width
from schematics import process_head_width_to_width
from schematics import process_head_length_to_head_width
from schematics import process_overhang

from schematics import process_face_color
from schematics import process_alpha


class Edge(Label):
  _instances = WeakValueDictionary()


  @property
  def count(self):
    return len(self._instances)


  def _get_label_locations(self):
    self.center = Point()
    self.top = Point()
    self.bottom = Point()
    self.left = None
    self.right = None


  def __init__(self, tail, head, **kwargs):
    self.tail = tail
    self.head = head
    self.directional = process_directional(True, kwargs)

    if self.tail == self.head:
      sys.exit('Error: Cannot connect a node to itself. (' + str(self.tail) + ' -/-> ' + str(self.head) + ')')

    if self.directional:
      self.string_connector = " --> "
    else:
      self.string_connector = " --- "

    self.label_location = process_label_location('top', kwargs)
    self.label_shift = process_label_shift(0.0, kwargs)
    super(Edge, self).__init__(Point(0.0, 0.0), ll = self.label_location, **kwargs)

    self.reflect = process_reflect(None, kwargs)
    self.angle = None

    # Arrow property processing option
    self.edge_width = process_width(0.025, kwargs)
    self.head_width_to_edge_width = process_head_width_to_width(3.0, kwargs)
    self.head_length_to_head_width = process_head_length_to_head_width(2.0, kwargs)
    self.overhang = process_overhang(0.0, kwargs)
    self.alpha = process_alpha(1.0, kwargs)
    self.face_color = process_face_color((0.0, 0.0, 0.0), kwargs)

    self.draw_bool = process_draw(True, kwargs)
    self.draw_label_bool = process_draw_label(True, kwargs)

    self._instances[id(self)] = self


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

    super(Edge, self)._get_angle_in_radians()


  def draw(self, tail_coords, head_coords, node_radius, **kwargs):
    self.edge_width = process_width(self.edge_width, kwargs)
    self.head_width_to_edge_width = process_head_width_to_width(self.head_width_to_edge_width, kwargs)
    self.head_length_to_head_width = process_head_length_to_head_width(self.head_length_to_head_width, kwargs)
    self.overhang = process_overhang(self.overhang, kwargs)
    self.alpha = process_alpha(self.alpha, kwargs)
    self.face_color = process_face_color(self.face_color, kwargs)

    if self.angle == None:
      self.get_angle(tail_coords, head_coords)

    node_delta = Point( node_radius * cos( self._angle_radians ),
                        node_radius * sin( self._angle_radians )
                      )

    if tail_coords.draw_bool:
      tail_delta = Point(node_delta.x, node_delta.y)
    else:
      tail_delta = Point()

    head_delta = Point(-1.0 * node_delta.x, -1.0 * node_delta.y)

    if self.directional:
      head_width  = self.head_width_to_edge_width * self.edge_width
      head_length = self.head_length_to_head_width * head_width
      if not head_coords.draw_bool:
        head_delta = Point()

    else:
      head_width  = 0.0
      head_length = 0.0
      if not head_coords.draw_bool:
        head_delta = Point( 0.5 * self.edge_width * cos( self._angle_radians ),
                            0.5 * self.edge_width * sin( self._angle_radians )
                          )

    tail_coords = tail_coords + tail_delta
    head_coords = head_coords + head_delta

    delta = head_coords - tail_coords

    if self.draw_bool:
      patch = FancyArrow(
                tail_coords.x, tail_coords.y,
                delta.x, delta.y,
                width = self.edge_width, length_includes_head = True,
                head_width = head_width, head_length = head_length,
                shape = 'full', overhang = self.overhang,
                head_starts_at_zero = False,
                fc = self.face_color, alpha = self.alpha
              )
      return patch
    else:
      return None


  def draw_label(self, tail_coords, head_coords, name, **kwargs):
    self.label_shift = process_label_shift(self.label_shift, kwargs)
    self.label_string = name

    self.center_of_rotation.x = 0.5 * (tail_coords.x + head_coords.x)
    self.center_of_rotation.y = 0.5 * (tail_coords.y + head_coords.y)

    if self.angle == None:
      self.get_angle(tail_coords, head_coords)

    length = abs(tail_coords - head_coords)
    self.center_of_rotation.x += self.label_shift * 0.5 * length * cos(self._angle_radians)
    self.center_of_rotation.y += self.label_shift * 0.5 * length * sin(self._angle_radians)

    if self.draw_label_bool:
      super(Edge, self).draw_label()
      return self.label
    else:
      return None


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

  def __str__(self):
    return str(self.tail) + self.string_connector + str(self.head)


  def __eq__(self, other):
    return ((self.tail == other.tail) and (self.head == other.head)) \
        or ((self.tail == other.head) and (self.head == other.tail))


  def has_node(self, node):
    return (node == self.tail) or (node == self.head)


  def __ne__(self, other):
    return not self.__eq__(other)


  def __deepcopy__(self, memo):
    return Edge(deepcopy(self.tail, memo), deepcopy(self.head, memo),
                dir = deepcopy(self.directional, memo),
                ll = deepcopy(self.label_location, memo),
                la = deepcopy(self.label_angle, memo),
                lp = deepcopy(self.label_pad, memo),
                fs = deepcopy(self.font_size, memo),
                label_shift = deepcopy(self.label_shift, memo)
               )
