from unittest import TestCase

from schematics import Node
from schematics import Point
from copy import deepcopy

class TestNode(TestCase):

  def test_instantiation(self):
    original_count = len(Node._instances)
    node = Node(3, 5)
    self.assertEqual(node.x, 3)
    self.assertEqual(node.y, 5)
    self.assertEqual(node.count, original_count + 1)


  def test_deletion(self):
    node = Node()
    original_count = len(Node._instances)
    del node
    self.assertEqual(len(Node._instances), original_count - 1)


  def test_copy(self):
    node = Node(3, 5)
    original_count = node.count
    tmp_node = deepcopy(node)
    self.assertEqual(tmp_node, node)
    self.assertIsNot(tmp_node, node)
    self.assertEqual(tmp_node.count, original_count + 1)
    self.assertEqual(tmp_node.count, node.count)


  def test_addition(self):
    original_count = len(Node._instances)
    node = Node(3, 5)
    node = node + node
    self.assertEqual(node.x, 6)
    self.assertEqual(node.y, 10)
    self.assertEqual(node.count, original_count + 1)


  def test_subtraction(self):
    original_count = len(Node._instances)
    node = Node(3, 5)
    tmp_node = node - node
    self.assertEqual(tmp_node.x, 0)
    self.assertEqual(tmp_node.y, 0)
    self.assertEqual(node.count, original_count + 2)


  def test_inequality(self):
    node = Node(3, 5)
    tmp_node = Node()
    self.assertNotEqual(tmp_node, node)
