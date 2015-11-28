from __future__ import print_function
import sys
from copy import deepcopy
import matplotlib.pyplot as plt
from collections import OrderedDict
from math import cos, sin

from schematics import Point
from schematics import Transformation
from schematics import Node
from schematics import Edge
from schematics import process_graphs
from schematics import process_name
from schematics import process_line_width
from schematics import process_radius

class Graph(Transformation):
  graphs = []

  def _mangle_dictionary(self, graph, dictionary):
    for name in dictionary.keys():
      dictionary[graph.name + ':' + name] = dictionary.pop(name)


  def _mangle_list(self, graph, list):
    for i, elem in enumerate(list):
      list[i] = graph.name + ':' + elem


  def _mangle_subgraphs(self, prefix, graph):
    index = Graph.graphs.index(graph.name)
    graph.name = prefix + ":" + graph.name
    Graph.graphs[index] = graph.name

    for graph in graph.subgraphs:
      self._mangle_subgraphs(prefix, graph)


  def _mangle_graph(self, graph):
    graph.namespace = graph.name + ':' + graph.namespace
    graph.namespace_size = len(graph.namespace)

    for edge in graph.edges.values():
      edge.tail = graph.name + ':' + edge.tail
      edge.head = graph.name + ':' + edge.head

    self._mangle_dictionary(graph, graph.edges)
    self._mangle_dictionary(graph, graph.nodes)

    graph.anchor = graph.name + ':' + graph.anchor
    self._mangle_list(graph, graph.anchored_nodes)
    self._mangle_list(graph, graph.anchored_edges)
    self._mangle_list(graph, graph.unique_unanchored_edges)
    self._mangle_list(graph, graph.unique_nodes)
    self._mangle_list(graph, graph.unique_anchored_edges)

    self._mangle_subgraphs(self.name, graph)


  def add_graph(self, graph):
    self._mangle_graph(graph)

    self.subgraphs.append(graph)
    self.nodes.update(graph.nodes)
    self.edges.update(graph.edges)

    graph.anchor_graph()
    if graph.anchored:
      self.anchored_subgraphs.append(graph)


  def __init__(self, **kwargs):
    '''
    default arguments:
      name (str)
      graphs (list of graphs)
    '''

    self.node_line_width = process_line_width(1.5, kwargs)
    self.node_radius = process_radius(0.05, kwargs)

    self.namespace = ''
    self.namespace_size = 0
    self.nodes = OrderedDict()
    self.edges = OrderedDict()
    self.anchor = None
    self.anchored = False
    self.anchored_nodes = []
    self.anchored_edges = []
    # uniqueness -- just added to a graph. i.e. doesn't exist within a subgraph
    self.unique_nodes = []
    self.unique_anchored_edges = []
    self.unique_unanchored_edges = []
    self.subgraphs = []
    self.anchored_subgraphs = [] # subgraphs that are internally anchored and anchored.

    self.angle = 0.0
    self._angle_radians = 0.0

    self.name = process_name("Graph " + str(len(Graph.graphs)), kwargs)

    Graph.graphs.append(self.name)

    graphs = process_graphs([], kwargs)
    if len(graphs):
      for i, graph in enumerate(graphs):
        self.add_graph(graph)

        if i == 0:
          self.anchor = graph.anchor
          self.anchored_nodes.extend(graph.anchored_nodes)
          self.anchored_edges.extend(graph.anchored_edges)


  def add_node(self, x, y, **kwargs):
    '''
    positional arguments:
      x (number)
      y (number)

    keyword arguments:
      name (str)
      anchor (bool):
        True - node is the anchor node.
        False - node is not the anchor node unless it is the first
                node added to the graph.
    '''
    name = process_name("Node " + str( len(Node._instances) ), kwargs)

    # location
    self.nodes[name] = Node(x, y, label_string = name, **kwargs)
    self.unique_nodes.append(name)

    # anchor
    if ('anchor' in kwargs):
      if kwargs['anchor']:
        self.anchor = name
        self.anchored_nodes = [self.anchor]
    elif self.anchor is None:
      self.anchor = name
      self.anchored_nodes = [self.anchor]

    return name


  def _check_if_node_exists(self, node):
    if node not in self.nodes:
      sys.exit('Error: Cannot connect ' + node + '. Not a part of the graph.')


  def _check_if_edge_exists(self, nodeA, nodeB, name):
    tmp_edge = Edge(nodeA, nodeB)
    for key, edge in self.edges.items():
      if edge == tmp_edge:
        print('Warning: Edge', name,'from', nodeA, 'to', nodeB, 'was previously specified.', key,'is being overwritten.')
        del self.edges[key]


  def _extend_anchored_nodes_with_subgraphs(self, graph):
    for node in graph.anchored_nodes:
      if node not in self.anchored_nodes:
        self.anchored_nodes.append(node)


  def _extend_anchored_edges_with_subgraphs(self, graph):
    for edge in graph.anchored_edges:
      if edge not in self.anchored_edges:
        self.anchored_edges.append(edge)


  def _anchor_subgraph(self, anchored_node):
    for graph in self.subgraphs:
      if anchored_node in graph.nodes:
        if graph.anchored:

          self._extend_anchored_nodes_with_subgraphs(graph)
          self._extend_anchored_edges_with_subgraphs(graph)
          break

        else:
          original_anchor = graph.anchor
          graph.change_anchor(anchored_node)

          # add subgraph's anchored nodes and edges to graph's anchored nodes
          self._extend_anchored_nodes_with_subgraphs(graph)
          self._extend_anchored_edges_with_subgraphs(graph)

          graph.change_anchor(original_anchor)
          break


  def connect(self, tail, head, **kwargs):
    '''
    positional arguments:
      tail (str): name of the 'tail' node
      head (str): name of the 'head' node (where the arrow points to)

    keyword arguments:
      name (str): name of the edge
      directional (bool): True - draw arrow pointing twords the head.
                          False - draw straight line between nodes.
    '''
    name = process_name("Edge " + str( len(Edge._instances) ), kwargs)

    self._check_if_node_exists(tail)
    self._check_if_node_exists(head)
    self._check_if_edge_exists(tail, head, name)

    self.edges[name] = Edge(tail, head, **kwargs)

    if tail in self.anchored_nodes:
      self.anchored_edges.append(name)
      self.unique_anchored_edges.append(name)
      if head not in self.anchored_nodes:
        self.anchored_nodes.append(head)
        self._anchor_subgraph(head)
    elif head in self.anchored_nodes:
      self.anchored_edges.append(name)
      self.unique_anchored_edges.append(name)
      if tail not in self.anchored_nodes:
        self.anchored_nodes.append(tail)
        self._anchor_subgraph(tail)
    else:
      self.unique_unanchored_edges.append(name)

    self.anchor_graph()
    return name


  def _nodes_and_anchored_nodes_match(self):
    if len(self.anchored_nodes) != len(self.nodes):
      return False
    for node in self.nodes.keys():
      if node not in self.anchored_nodes:
        return False
    return True


  def _anchor_connected_nodes(self, edge):
    if self.edges[edge].tail in self.anchored_nodes:
      if self.edges[edge].head not in self.anchored_nodes:
        self.anchored_nodes.append(self.edges[edge].head)
      self.anchored_edges.append(edge)
      return edge

    elif self.edges[edge].head in self.anchored_nodes:
      if self.edges[edge].tail not in self.anchored_nodes:
        self.anchored_nodes.append(self.edges[edge].tail)
      self.anchored_edges.append(edge)
      return edge

    else:
      return None


  def _anchor_unique_nodes(self):
    start_of_search = len(self.unique_anchored_edges)
    newly_anchored_edges = []
    for edge in self.unique_unanchored_edges:
      anchored_edge = self._anchor_connected_nodes(edge)
      if anchored_edge != None:
        newly_anchored_edges.append(anchored_edge)

    for edge in newly_anchored_edges:
      self.unique_unanchored_edges.remove(edge)
      self.unique_anchored_edges.append(edge)

    return start_of_search


  def _subgraph_is_connected(self, subgraph, start_of_search):
    for edge in self.unique_anchored_edges[start_of_search:]:
      for node in subgraph.nodes.keys():
        if self.edges[edge].has_node(node):
          return True
    return False


  def anchor_graph(self):
    self.anchored = self._nodes_and_anchored_nodes_match()

    if not self.anchored:

      # anchor subgraphs
      n_subgraphs = len(self.subgraphs)
      for i in range(n_subgraphs):

        unanchored_subgraphs = [subgraph for subgraph in self.subgraphs if subgraph not in self.anchored_subgraphs]
        if len(unanchored_subgraphs) == 0:
          break

        start_of_search = self._anchor_unique_nodes()
        for subgraph in unanchored_subgraphs:
          if self._subgraph_is_connected(subgraph, start_of_search):
            if subgraph.anchored:
              self.anchored_subgraphs.append(subgraph)
              self.anchored_nodes.extend([name for name in subgraph.nodes.keys()])
              self.anchored_edges.extend([name for name in subgraph.edges.keys()])

      # anchor remainder of nodes
      unanchored_edges = [edge for edge in self.edges.keys() if edge not in self.anchored_edges]
      n_unanchored_nodes = len([node for node in self.nodes.keys() if node not in self.anchored_nodes])
      for i in range(n_unanchored_nodes):
        if len(unanchored_edges) == 0:
          break

        newly_anchored_edges = []
        for edge in unanchored_edges:
          anchored_edge = self._anchor_connected_nodes(edge)
          if anchored_edge != None:
            newly_anchored_edges.append(anchored_edge)

        for edge in newly_anchored_edges:
          unanchored_edges.remove(edge)

      self.anchored = self._nodes_and_anchored_nodes_match()


  def change_anchor(self, new):
    '''
    positional argument:
      new (str): name of the new anchor node
    '''
    self._check_if_node_exists(new)
    self.anchor = new

    if not self.anchored:
      self.anchored_nodes = []
      self.anchored_edges = []
      self.unique_unanchored_edges.extend(self.unique_anchored_edges)
      self.unique_anchored_edges = []
      self.anchor_graph()


  def draw_nodes(self):
    patches = []

    for node in self.nodes.values():
      patch = node.draw(radius = self.node_radius, line_width = self.node_line_width)
      if patch is not None:
        patches.append(patch)

    return patches


  def draw_node_labels(self):
    labels = []
    for name, node in self.nodes.items():
      label = node.draw_label(name)
      if label is not None:
        labels.append(label)
    return labels


  def draw_edges(self):
    patches = []

    for edge in self.edges.values():
      patch = edge.draw(self.nodes[edge.tail], self.nodes[edge.head], self.node_radius)
      if patch is not None:
        patches.append(patch)

    return patches


  def draw_edge_labels(self):
    labels = []
    for name, edge in self.edges.items():
      label = edge.draw_label(self.nodes[edge.tail], self.nodes[edge.head], name)
      if label is not None:
        labels.append(label)
    return labels


  def _filter_and_print_dictionary(self, dictionary, select_keys):
    print_string = ''
    size = len(select_keys)
    if len(select_keys):
      print_string += '\n'
      for i, key in enumerate(select_keys):
        print_string += key + ": " + str(dictionary[key])
        if i < (size - 1):
          print_string += '\n'
    else:
      print_string += ' None'
    return print_string


  def _print_mangled_dictionary(self, dictionary, mangle_length):
    print_string = ''
    size = len(dictionary)
    if size:
      print_string += '\n'
      for i, (key, value) in enumerate(dictionary.items()):
        print_string += key[mangle_length:] + ": " + str(value)
        if i < (size - 1):
          print_string += '\n'
    else:
      print_string += ' None'
    return print_string


  def __str__(self):
    # header
    print_string = self.name + '\n'
    print_string += (len(self.name) * '-') + '\n'

    # graph composed of subgraphs
    total_of_subgraphs = len(self.subgraphs)
    if total_of_subgraphs:

      # list of subgraphs
      print_string += '\nSubgraphs: '
      for i, subgraph in enumerate(self.subgraphs):
        print_string += subgraph.name
        if i < (total_of_subgraphs-1):
          print_string += ', '
        else:
          print_string += '\n'

      # list of unique nodes
      print_string += '\nUnique Nodes:'
      print_string += self._filter_and_print_dictionary(self.nodes, self.unique_nodes)
      print_string += '\n'

      # anchor node
      print_string += '\nAnchor:\n'
      print_string += self.anchor + ': ' + str(self.nodes[self.anchor]) + '\n'

      # list of unique edges
      print_string += '\nUnique Edges:'
      print_string += self._filter_and_print_dictionary(self.edges, self.unique_anchored_edges)
      print_string += '\n'

      # anchored
      print_string += '\nAnchored: ' + str(self.anchored)

      # depth first, recursively add the subgraphs' information
      print_string += '\n' * 3
      for i, subgraph in enumerate(self.subgraphs):
        print_string += str(subgraph)
        if i < (total_of_subgraphs - 1):
          print_string += '\n' * 3

    # base graph
    else:

      # list of nodes
      print_string += '\nNodes:'
      print_string += self._print_mangled_dictionary(self.nodes, self.namespace_size)
      print_string += '\n'

      # name of anchor node
      print_string += '\nAnchor:\n'
      print_string += self.anchor[self.namespace_size:] + ': ' + str(self.nodes[self.anchor]) + '\n'

      # list of edges
      print_string += '\nEdges:'
      print_string += self._print_mangled_dictionary(self.edges, self.namespace_size)
      print_string += '\n'

      # anchored
      print_string += '\nAnchored: ' + str(self.anchored)

    return print_string


  def reflect(self, axis):
    '''
    positional argument:
      axis (str): either 'x' or 'y'
    '''
    self.reflect = axis
    self.center_of_rotation = self.nodes[self.anchor]
    for node in self.nodes.values():
      # move node locations
      old_coord = node - self.center_of_rotation
      new_coord = node - self.center_of_rotation
      self._reflect(new_coord)
      displacement = new_coord - old_coord
      node.move(displacement)

      node.reflect = self.reflect

    def swap_label_location(label_location):
      if label_location == 'bottom':
        return 'top'
      elif label_location == 'top':
        return 'bottom'

    for edge in self.edges.values():
      edge.reflect = self.reflect
      edge.label_location = swap_label_location(edge.label_location)


  def rotate(self, angle):
    '''
    positional argument:
      angle (number in degrees)
    '''
    self.center_of_rotation = Point(self.nodes[self.anchor].x, self.nodes[self.anchor].y)
    self.angle = angle
    self._get_angle_in_radians()

    for edge in self.edges.values():
      if edge.angle == None:
        edge.get_angle( self.nodes[edge.tail], self.nodes[edge.head] )
      edge.angle += self.angle
      edge.label_angle += self.angle
      edge._get_angle_in_radians()

    for node in self.nodes.values():
      # move node and its center of rotation
      old_rel_location = node - self.center_of_rotation
      new_rel_location = node - self.center_of_rotation
      self._rotate(new_rel_location)
      new_rel_location -= self.center_of_rotation
      displacement = new_rel_location - old_rel_location
      node.move(displacement)

      # determine new node angle
      node.angle += self.angle
      node._get_angle_in_radians()


  def move(self, x, y):
    displacement = Node(x, y) - self.nodes[self.anchor]
    for node in self.nodes.values():
      node.move(displacement)


  def _remangle_subgraph_names(self, graph, new_name, old_name):
    for subgraph in graph.subgraphs:
      subgraph.name = new_name + subgraph.name[len(old_name):]
      Graph.graphs.append(subgraph.name)
      self._remangle_subgraph_names(subgraph, new_name, old_name)


  def copy(self, x=0.0, y=0.0, **kwargs):
    '''
    default arguments:
      x (number)
      y (number)

    keyword arguments:
      name (str)
    '''
    name = process_name(self.name + '(copy)', kwargs)

    duplicate = deepcopy(self)

    self._remangle_subgraph_names(duplicate, name, duplicate.name)
    duplicate.name = name
    duplicate.move(x, y)
    Graph.graphs.append(duplicate.name)
    return duplicate


  def general_info(self):
    print_string = 'Number of Graphs: ' + str(len(Graph.graphs)) + '\n'
    print_string += 'Number of Nodes: ' + str(len(Node._instances)) + '\n'
    print_string += 'Number of Edges: ' + str(len(Edge._instances)) + '\n'
    print_string += 'Graphs:\n' + str(Graph.graphs)

    return print_string


  def __del__(self):
    for subgraph in self.subgraphs:
      subgraph.__del__()
    if len(Graph.graphs) != 0:
      Graph.graphs.remove(self.name)
