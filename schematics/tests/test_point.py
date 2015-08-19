from unittest import TestCase

from schematics import Point
from copy import deepcopy

class TestPoint(TestCase):

  def test_attributes(self):
    point = Point(3, 5)
    self.assertEqual(point.x, 3)
    self.assertEqual(point.y, 5)

  def test_copy(self):
    point = Point(3, 5)
    tmp_point = deepcopy(point)
    self.assertEqual(tmp_point, point)
    self.assertIsNot(tmp_point, point)


  def test_addition(self):
    point = Point(3, 5)
    tmp_point = point + point
    self.assertEqual(tmp_point.x, 6)
    self.assertEqual(tmp_point.y, 10)


  def test_subtraction(self):
    point = Point(3, 5)
    tmp_point = point - point
    self.assertEqual(tmp_point.x, 0)
    self.assertEqual(tmp_point.y, 0)


  def test_inequality(self):
    point = Point(3, 5)
    tmp_point = Point()
    self.assertNotEqual(tmp_point, point)

  def test_tuple(self):
    point = Point(3, 5)
    tmp_tuple = point.to_tuple()
    self.assertTrue(isinstance(tmp_tuple, tuple))
    self.assertEqual(tmp_tuple[0], 3)
    self.assertEqual(tmp_tuple[1], 5)
