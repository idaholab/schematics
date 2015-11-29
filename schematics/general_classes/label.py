import sys
import matplotlib.pyplot as plt
from math import pi, sin, cos

from schematics import Transformation
from schematics import Point
from schematics import process_label_location
from schematics import process_label_string
from schematics import process_label_angle
from schematics import process_label_pad
from schematics import process_font_size

class Label(Transformation):

  def __init__(self, center_of_rotation, **kwargs):
    super(Label, self).__init__(center_of_rotation, **kwargs)

    self._get_label_locations()
    self.label_location = process_label_location('center', kwargs)
    self.label_string = process_label_string(None, kwargs)
    self.label_angle = process_label_angle(0.0, kwargs)
    self.label_pad = process_label_pad(1.0, kwargs)
    self.font_size = process_font_size(12, kwargs)
    self.label = None


  def _reflect_label_location(self):
    self._reflect(self.center)
    if self.top is not None:
      self._reflect(self.top)
    if self.bottom is not None:
      self._reflect(self.bottom)
    if self.left is not None:
      self._reflect(self.left)
    if self.right is not None:
      self._reflect(self.right)


  def _invalid_label_location_error(self, location):
    sys.exit('Error: ' + location + ' label location selected when it is not ' +
             'available. (' + self.__class__.__name__ + ')')


  def _guess_label_coordinates(self):
    self._reflect_label_location()
    self._label_coordinates = Point(self.center.x, self.center.y)

    if self.label_location == 'top':
      if self.top is None:
        self._invalid_label_location_error('top')
      else:
        self._label_coordinates.y = self.top.y

    elif self.label_location == 'bottom':
      if self.bottom is None:
        self._invalid_label_location_error('bottom')
      else:
        self._label_coordinates.y = self.bottom.y

    elif self.label_location == 'left':
      if self.left is None:
        self._invalid_label_location_error('left')
      else:
        self._label_coordinates.x = self.left.x

    elif self.label_location == 'right':
      if self.right is None:
        self._invalid_label_location_error('right')
      else:
        self._label_coordinates.x = self.right.x

    self._rotate(self._label_coordinates)


  def _get_actual_label_position(self, label_dimensions):
    self._label_coordinates = Point(self.center.x, self.center.y)

    if self.label_location == 'bottom' or self.label_location == 'top':
      # calculate padding
      padding = abs( 0.5 * cos((pi * self.label_angle) / 180.0) )
      padding = (self.label_pad + padding) * label_dimensions.height
      padding += abs( 0.5 * label_dimensions.width * sin((pi * self.label_angle) / 180.0) )
      if self.reflect == 'x':
        padding *= -1.0
        self.label_angle *= -1.0
      elif self.reflect == 'y':
        self.label_angle *= -1.0

      # determine label coordinates
      if self.label_location == 'bottom':
        self._label_coordinates.y = self.bottom.y - padding
      else:
        self._label_coordinates.y = self.top.y + padding

    elif self.label_location == 'left' or self.label_location == 'right':
      # claculate padding
      padding = abs( 0.5 * sin((pi * self.label_angle) / 180.0) )
      padding = (self.label_pad + padding) * label_dimensions.height
      padding += abs( 0.5 * label_dimensions.width * cos((pi * self.label_angle) / 180.0) )
      if self.reflect == 'y':
        padding *= -1.0
        self.label_angle *= -1.0
      elif self.reflect == 'x':
        self.label_angle *= -1.0

      # determine label coordinates
      if self.label_location == 'left':
        self._label_coordinates.x = self.left.x - padding
      else:
        self._label_coordinates.x = self.right.x + padding

    self._rotate(self._label_coordinates)


  def draw_label(self, **kwargs):
    self.label_angle = process_label_angle(self.label_angle, kwargs)
    self.label_pad = process_label_pad(self.label_pad, kwargs)
    self.font_size = process_font_size(self.font_size, kwargs)
    self.label_location = process_label_location(self.label_location, kwargs)

    if self.label_string is not None:
      self._guess_label_coordinates()
      self.label = plt.text(self._label_coordinates.x,
                            self._label_coordinates.y, self.label_string,
                            ha="center", va="center", size=self.font_size,
                            rotation=0.0
                           )
      return self.label
    else:
      return None


  def adjust_label(self, label_dimensions):
    self._get_actual_label_position(label_dimensions)
    self.label.set_x(self._label_coordinates.x)
    self.label.set_y(self._label_coordinates.y)
    self.label.set_rotation(self.angle + self.label_angle)


# Error messages
  def _get_label_locations(self):
    sys.exit('Error: Must define "_get_label_locations" method in the ' + self.__class__.__name__ + ' class.')
    # define coordinates for self.center, self.left, self.right, self.top, self.bottom
    # relative to the center of rotation.
