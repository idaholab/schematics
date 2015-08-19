from unittest import TestCase

from schematics import Edge
from copy import deepcopy

class TestEdge(TestCase):

  def test_attributes(self):
    edge = Edge('tail', 'head', directional = True)
    self.assertEqual(edge.tail, 'tail')
    self.assertEqual(edge.head, 'head')
    self.assertTrue(edge.directional)
    self.assertEqual(edge.string_connector, ' --> ')
    edge = Edge('tail', 'head', directional = False)
    self.assertFalse(edge.directional)
    self.assertEqual(edge.string_connector, ' --- ')


  def test_copy(self):
    edge = Edge('tail', 'head', directional = True)
    tmp_edge = deepcopy(edge)
    self.assertEqual(tmp_edge, edge)
    self.assertIsNot(tmp_edge, edge)


  def test_has_node(self):
    edge = Edge('tail', 'head', directional = True)
    self.assertTrue(edge.has_node('tail'))
    self.assertTrue(edge.has_node('head'))


  def test_equality(self):
    edge = Edge('tail', 'head', directional = True)
    tmp_edge = deepcopy(edge)
    tmp_edge.directional = False
    self.assertEqual(tmp_edge, edge)


  def test_inequality(self):
    edge = Edge('tail', 'head', directional = True)
    tmp_edge = Edge('bob', 'head', directional = True)
    self.assertNotEqual(tmp_edge, edge)


  def test_edge_number(self):
    original_count = len(Edge._instances)
    tmp_edge = Edge('tail', 'head')
    self.assertEqual(tmp_edge.count, original_count + 1)
    del tmp_edge
    self.assertEqual(len(Edge._instances), original_count)
