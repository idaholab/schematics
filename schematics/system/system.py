from copy import deepcopy

from schematics import Graph
from schematics import Edge
from schematics import Node
from schematics import Junction

from schematics import process_name

class System(object):
  subsystems = []

  def __init__(self, name, systems = []):
    self.name = name
    self.graph = Graph(name = name)
    self.subsystems = systems

    self.unique_edges = []
    self.junctions = []
    self.connections = []
    self.connections_kwargs = []
    self.components = []


  def add_component(self, component):
    # supress component graph drawing
    for node in component.graph.nodes.values():
      node.draw_bool = False
      node.draw_label_bool = False
    for edge in component.graph.edges.values():
      edge.draw_bool = False
      edge.draw_label_bool = False
    self.graph.add_graph(component.graph)
    self.components.append(component)


  def add_node(self, x, y, **kwargs):
    name = self.graph.add_node(x, y, **kwargs)
    self.graph.nodes[name].draw_bool = False
    self.graph.nodes[name].draw_label_bool = False


  def _already_existing_edge(self, nodeA, nodeB):
    tmp_edge = Edge(nodeA, nodeB)
    for edge in self.unique_edges:
      if tmp_edge == self.graph.edges[edge]:
        return edge
    return None


  def connect(self, *nodes, **kwargs):
    self.connections.append(nodes)
    self.connections_kwargs.append(kwargs)

    number_of_nodes = len(nodes)
    iterations = number_of_nodes - 1
    last_iteration = iterations - 1

    junction_edges = []
    for i in range(iterations):
      name = self._already_existing_edge(nodes[i], nodes[i+1])
      if name is None:
        if i == last_iteration:
          name = self.graph.connect(nodes[i], nodes[i+1], directional = True, draw_label = False)
        else:
          name = self.graph.connect(nodes[i], nodes[i+1], directional = False, draw_label = False)
        self.unique_edges.append(name)
      junction_edges.append(name)

    self.junctions.append( Junction(junction_edges, **kwargs) )


  def move(self, x, y):
    displacement = Node(x, y) - self.graph.nodes[self.graph.anchor]
    for node in self.graph.unique_nodes:
      self.graph.nodes[node].x += displacement.x
      self.graph.nodes[node].y += displacement.y
    for component in self.components:
      new_coords = component.center_of_rotation + displacement
      component.move(new_coords.x, new_coords.y)


  def copy(self, x=0.0, y=0.0, **kwargs):
    name = process_name(self.name + '(copy)', kwargs)

    duplicate = System(name, systems = self.subsystems)

    for component in self.components:
      duplicate.add_component(deepcopy(component))

    for name in self.graph.unique_nodes:
      duplicate.add_node(self.graph.nodes[name].x, self.graph.nodes[name].y, name = name)

    for connection, kwargs in zip(self.connections, self.connections_kwargs):
      duplicate.connect(*connection, **kwargs)

    duplicate.move(x, y)
    return duplicate
    # duplicate = deepcopy(self)
    #
    # duplicate.name = name
    # duplicate.graph = self.graph.copy(x=x, y=y, name = name)
    #
    # duplicate.move(x, y)
