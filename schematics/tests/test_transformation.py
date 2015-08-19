from unittest import TestCase

from schematics import Transformation
from schematics import Point
from math import pi

class TestTransformation(TestCase):

  def test_instantiation(self):
    transformer = Transformation(Point(), angle = 90.0, reflect = 'x')
    self.assertEqual(transformer.center_of_rotation.x, 0.0)
    self.assertEqual(transformer.center_of_rotation.y, 0.0)
    self.assertEqual(transformer.angle, 90.0)
    self.assertAlmostEqual(transformer._angle_radians, (0.5 * pi))
    self.assertEqual(transformer.reflect, 'x')


  def test_reflection(self):
    transformer = Transformation(Point(), angle = 90.0, reflect = 'x')
    old_point = Point(0.0, 1.0)
    transformer._reflect(old_point)
    self.assertEqual(old_point.x, 0.0)
    self.assertEqual(old_point.y, -1.0)

    transformer = Transformation(Point(), angle = 90.0, reflect = 'y')
    old_point = Point(1.0, 0.0)
    transformer._reflect(old_point)
    self.assertEqual(old_point.x, -1.0)
    self.assertEqual(old_point.y, 0.0)


  def test_rotation(self):
    transformer = Transformation(Point(), angle = 90.0, reflect = 'x')
    old_point = Point(0.0, 1.0)
    transformer._rotate(old_point)
    self.assertAlmostEqual(old_point.x, -1.0)
    self.assertAlmostEqual(old_point.y, 0.0)


  def test_reflection_and_rotation(self):
    transformer = Transformation(Point(1.0, 1.0), angle = 90.0, reflect = 'y')
    old_point = Point(1.0, 0.0)
    transformer._reflect(old_point)
    transformer._rotate(old_point)
    self.assertAlmostEqual(old_point.x, 1.0)
    self.assertAlmostEqual(old_point.y, 0.0)
