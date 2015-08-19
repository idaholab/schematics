from unittest import TestCase

from schematics import Label
from schematics import Point
from schematics import Rectangle
from math import pi, sqrt

class BasicLabel(Label):
  def __init__(self, center_of_rotation, **kwargs):
    Label.__init__(self, center_of_rotation, **kwargs)

  def _get_label_locations(self):
    self.center = Point(1.0, 0.0)
    self.left = Point()
    self.right = Point(2.0, 0.0)
    self.top = Point(1.0, 1.0)
    self.bottom = Point(1.0, -1.0)


class TestLabel(TestCase):

  def test_instantiation(self):
    label = BasicLabel(Point(), angle = 0.0, ll = 'center', ls = 'test', fs = 14)
    self.assertEqual(label.center_of_rotation.x, 0.0)
    self.assertEqual(label.center_of_rotation.y, 0.0)
    self.assertEqual(label.angle, 0.0)
    self.assertEqual(label.label_location, 'center')
    self.assertEqual(label.label_string, 'test')
    self.assertEqual(label.label_angle, 0.0)
    self.assertEqual(label.label_pad, 1.0)
    self.assertEqual(label.font_size, 14)
    self.assertEqual(label.reflect, None)


  def _check_almost_equal(self, coordinates, x, y):
    self.assertAlmostEqual(coordinates.x, x)
    self.assertAlmostEqual(coordinates.y, y)


  def test_guess_center_label_coordinates(self):
    label = BasicLabel(Point(), a = 0.0, ll = 'center', ls = 'test')
    label._get_label_locations()
    label._guess_label_coordinates()
    self._check_almost_equal(label._label_coordinates, 1.0, 0.0)


  def test_actual_center_label_coordinates(self):
    label = BasicLabel(Point(), a = 45.0, ll = 'center', ls = 'test')
    label._get_label_locations()
    label._get_actual_label_position( Rectangle(1.0, 1.0) )
    self._check_almost_equal(label._label_coordinates, 0.5 * sqrt(2), 0.5 * sqrt(2))


  def test_guess_left_label_coordinates(self):
    label = BasicLabel(Point(), a = 0.0, ll = 'left', ls = 'test')
    label._get_label_locations()
    label._guess_label_coordinates()
    self._check_almost_equal(label._label_coordinates, 0.0, 0.0)


  def test_actual_left_label_coordinates(self):
    label = BasicLabel(Point(), a = 45.0, ll = 'left', ls = 'test')
    label._get_label_locations()
    label._get_actual_label_position( Rectangle(1.0, 1.0) )
    self._check_almost_equal(label._label_coordinates, -0.75 * sqrt(2), -0.75 * sqrt(2))


  def test_guess_right_label_coordinates(self):
    label = BasicLabel(Point(), a = 0.0, ll = 'right', ls = 'test')
    label._get_label_locations()
    label._guess_label_coordinates()
    self._check_almost_equal(label._label_coordinates, 2.0, 0.0)


  def test_actual_right_label_coordinates(self):
    label = BasicLabel(Point(), a = 45.0, ll = 'right', ls = 'test')
    label._get_label_locations()
    label._get_actual_label_position( Rectangle(1.0, 1.0) )
    self._check_almost_equal(label._label_coordinates, 1.75 * sqrt(2), 1.75 * sqrt(2))


  def test_guess_top_label_coordinates(self):
    label = BasicLabel(Point(), a = 0.0, ll = 'top', ls = 'test')
    label._get_label_locations()
    label._guess_label_coordinates()
    self._check_almost_equal(label._label_coordinates, 1.0, 1.0)


  def test_actual_top_label_coordinates(self):
    label = BasicLabel(Point(), a = 90.0, ll = 'top', ls = 'test')
    label._get_label_locations()
    label._get_actual_label_position( Rectangle(1.0, 1.0) )
    self._check_almost_equal(label._label_coordinates, -2.5, 1.0)


  def test_guess_bottom_label_coordinates(self):
    label = BasicLabel(Point(), a = 0.0, ll = 'bottom', ls = 'test')
    label._get_label_locations()
    label._guess_label_coordinates()
    self._check_almost_equal(label._label_coordinates, 1.0, -1.0)


  def test_actual_bottom_label_coordinates(self):
    label = BasicLabel(Point(), a = 90.0, ll = 'bottom', ls = 'test')
    label._get_label_locations()
    label._get_actual_label_position( Rectangle(1.0, 1.0) )
    self._check_almost_equal(label._label_coordinates, 2.5, 1.0)
