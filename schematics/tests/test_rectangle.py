from unittest import TestCase

from schematics import Rectangle
from copy import deepcopy

class TestRectangle(TestCase):

  def test_attributes(self):
    rectangle = Rectangle(3, 5)
    self.assertEqual(rectangle.width, 3)
    self.assertEqual(rectangle.height, 5)
