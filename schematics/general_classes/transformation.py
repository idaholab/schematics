from math import pi, sin, cos
from point import Point

from schematics import process_angle
from schematics import process_reflect

DEGREES_PER_RADIAN = pi / 180.0


class Transformation(object):

  def _get_angle_in_radians(self):
    self._angle_radians = self.angle * DEGREES_PER_RADIAN


  def _rotate(self, old):
    # 'old' coordinates are relative to the center of rotation
    # 'new' coordinates are absolute
    new = Point()
    new.x = self.center_of_rotation.x + (old.x * cos(self._angle_radians)) - (old.y * sin(self._angle_radians))
    new.y = self.center_of_rotation.y + (old.x * sin(self._angle_radians)) + (old.y * cos(self._angle_radians))
    old.x = new.x
    old.y = new.y


  def _reflect(self, point):
    # deals in relative coordinates
    if self.reflect == 'x':
      point.y *= -1
    elif self.reflect == 'y':
      point.x *= -1


  def __init__(self, center_of_rotation, **kwargs):
    self.center_of_rotation = center_of_rotation
    self.angle = process_angle(0.0, kwargs)
    self._get_angle_in_radians()
    self.reflect = process_reflect(None, kwargs)
