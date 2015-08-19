import sys
from copy import deepcopy
from weakref import WeakValueDictionary
from matplotlib.patches import Circle

from schematics import Point
from schematics import Label

from schematics import process_radius
from schematics import process_line_width
from schematics import process_face_color
from schematics import process_alpha
from schematics import process_edge_color
from schematics import process_label_location
from schematics import process_label_angle
from schematics import process_label_pad
from schematics import process_font_size

from schematics import process_draw
from schematics import process_draw_label


class Node(Point, Label):
  _instances = WeakValueDictionary()

  @property
  def count(self):
    return len(self._instances)


  def _get_label_locations(self):
    self.center = Point()
    self.left   = Point(self.center.x - self.radius, self.center.y)
    self.right  = Point(self.center.x + self.radius, self.center.y)
    self.top    = Point(self.center.x, self.center.y + self.radius)
    self.bottom = Point(self.center.x, self.center.y - self.radius)


  def __init__(self, x = 0.0, y = 0.0, **kwargs):
    self.radius = process_radius(0.05, kwargs)
    self.line_width = process_line_width(1.5, kwargs)
    self.face_color = process_face_color((1.0, 1.0, 1.0), kwargs)
    self.alpha = process_alpha(1.0, kwargs)
    self.edge_color = process_edge_color((0.0, 0.0, 0.0), kwargs)


    Label.__init__(self, Point(x, y), **kwargs)
    super(Node, self).__init__(x, y)

    self.draw_bool = process_draw(True, kwargs)
    self.draw_label_bool = process_draw_label(True, kwargs)

    self._instances[id(self)] = self


  def move(self, displacement):
    self.x += displacement.x
    self.y += displacement.y
    self.center_of_rotation.x += displacement.x
    self.center_of_rotation.y += displacement.y


  def draw(self, **kwargs):
    self.radius = process_radius(self.radius, kwargs)
    self.line_width = process_line_width(self.line_width, kwargs)
    self.face_color = process_face_color(self.face_color, kwargs)
    self.alpha = process_alpha(self.alpha, kwargs)
    self.edge_color = process_edge_color(self.edge_color, kwargs)

    if self.draw_bool:
      patch = Circle((self.x, self.y), radius = self.radius,
                     fc = self.face_color, alpha = self.alpha,
                     ec = self.edge_color, lw = self.line_width
                    )
      return patch

    else:
      self.radius = 0.0
      return None


  def draw_label(self, name, **kwargs):
    self.label_angle = process_label_angle(self.label_angle, kwargs)
    self.label_pad = process_label_pad(self.label_pad, kwargs)
    self.font_size = process_font_size(self.font_size, kwargs)
    self.label_location = process_label_location(self.label_location, kwargs)

    self._get_label_locations()
    if self.draw_label_bool:
      self.label_string = name
      super(Node, self).draw_label()
      return self.label
    else:
      return None


  def __str__(self):
    return super(Node, self).__str__()


  def __deepcopy__(self, memo):
    return Node(deepcopy(self.x, memo), deepcopy(self.y, memo),
                ll = deepcopy(self.label_location, memo),
                ls = deepcopy(self.label_string, memo),
                la = deepcopy(self.label_angle, memo),
                lp = deepcopy(self.label_pad, memo),
                fs = deepcopy(self.font_size, memo),
                a = deepcopy(self.angle, memo),
                ref = deepcopy(self.reflect, memo),
                d = deepcopy(self.draw_bool, memo)
               )


  def __add__(self, other):
    return Node(self.x + other.x, self.y + other.y)


  def __sub__(self, other):
    return Node(self.x - other.x, self.y - other.y)
