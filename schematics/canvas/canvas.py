from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection

from schematics import Point
from schematics import Rectangle

class Canvas(object):

  def _get_border_dimensions(self):
    self._lower_border_boundries = self.border_thickness
    self._axis_thickness = 1.0 - (2.0 * self.border_thickness)
    self._axis_border = [self._lower_border_boundries, self._lower_border_boundries, self._axis_thickness, self._axis_thickness]


  def __init__(self, components = [], graphs = [], systems = [], width = 12.0, height = 8.0, border_thickness = 0.0, grid = False):
    assert (border_thickness < 0.5) and (border_thickness >= 0.0)

    self.components = components
    self.graphs = graphs
    self.systems = systems
    self.width = width
    self.height = height
    self.border_thickness = border_thickness
    self.grid = grid

    self.fig = plt.figure(figsize = (self.width, self.height))
    self.renderer = self.fig.canvas.renderer
    self.fig.set_facecolor('white')
    self._get_border_dimensions()
    self.ax = plt.axes(self._axis_border)
    self.ax.plot()

    self.colors = None
    self.patches = []
    self.node_patches = []
    self.edge_patches = []
    self.collection = None
    self.node_collection = None
    self.edge_collection = None
    self.labels = []

    self._origin = Point()
    self._axis_size_width = 0.0
    self._axis_size_height = 0.0
    self._axis_pixel_width = 0.0
    self._axis_pixel_height = 0.0
    self._figure_pixel_width = 0.0
    self._figure_pixel_height = 0.0
    self._labels_dimensions  = []
    self._labels_pixel_dimensions = []
    self._patches_dimensions = []
    self._patches_pixel_dimensions = []
    self._PIXELS_PER_UNIT = None

    self._figure_aspect_ratio = float(self.width) / float(self.height)
    self._axis_aspect_ratio  = None
    self._display = None


  def add_component(self, component):
    self.components.append(component)


  def add_graph(self, graph):
    self.graphs.append(graph)


  def add_system(self, system):
    self.systems.append(system)


  def _get_plot_origin(self):
    plt.axis('tight')
    self._origin.x = 0.5 * (plt.axis()[1] + plt.axis()[0])
    self._origin.y = 0.5 * (plt.axis()[3] + plt.axis()[2])


  def _get_plot_scale(self):
    '''Determined the scaled width and height'''
    plt.axis('scaled')
    self._axis_size_height = plt.axis()[3] - plt.axis()[2]
    self._axis_size_width  = plt.axis()[1] - plt.axis()[0]


  def _plot_tight_scaled(self):
    self._get_plot_origin()
    self._get_plot_scale()

    # Adjust plot to optimum origin and remove decorations
    plt.xlim( self._origin.x - (self._axis_size_width * 0.5), self._origin.x + (self._axis_size_width * 0.5) )
    plt.ylim( self._origin.y - (self._axis_size_height * 0.5), self._origin.y + (self._axis_size_height * 0.5) )
    if self.grid:
      plt.grid(linestyle = '--', alpha = 0.5)
      plt.tick_params(axis = 'x', which = 'both', bottom = 'off', top = 'off')
      plt.tick_params(axis = 'y', which = 'both', left = 'off', right = 'off')
    else:
      plt.axis('off')


  def _get_canvas_dimensions(self):
    self._figure_pixel_height = self.fig.get_window_extent().bounds[3]
    self._figure_pixel_width  = self.fig.get_window_extent().bounds[2]
    self._axis_pixel_height = self.ax.get_window_extent().bounds[3]
    self._axis_pixel_width  = self.ax.get_window_extent().bounds[2]
    self._PIXELS_PER_UNIT = self._axis_pixel_height / self._axis_size_height


  def _get_label_dimensions(self):
    for i, label in enumerate(self.labels):
      bb = label.get_window_extent(renderer = self.renderer)
      self._labels_pixel_dimensions.append(Rectangle(bb.width, bb.height))
      self._labels_dimensions.append(Rectangle(bb.width / self._PIXELS_PER_UNIT, bb.height / self._PIXELS_PER_UNIT))


  def _get_patch_dimensions(self):
    for i, patch in enumerate(self.patches):
      bb = patch.get_window_extent(renderer = self.renderer)
      self._patches_pixel_dimensions.append(Rectangle(bb.width, bb.height))
      self._patches_dimensions.append(Rectangle(bb.width / self._PIXELS_PER_UNIT, bb.height / self._PIXELS_PER_UNIT))


  def print_information(self):
    print('origin:                  ', self._origin)
    print('axis [units]:            ', self._axis_size_width, self._axis_size_height)
    print('axis [pixels]:           ', self._axis_pixel_width, self._axis_pixel_height)
    print('figure [inches]:         ', self.width, self.height)
    print('figure [pixels]:         ', self._figure_pixel_width, self._figure_pixel_height)
    print('pixels per unit:         ', self._PIXELS_PER_UNIT)
    print('label dimensions [units]: ', [str(dimension) for dimension in self._labels_dimensions])
    print('label dimensions [pixels]:', [str(dimension) for dimension in self._labels_pixel_dimensions])
    print('patch dimensions [units]: ', [str(dimension) for dimension in self._patches_dimensions])
    print('patch dimensions [pixels]:', [str(dimension) for dimension in self._patches_pixel_dimensions])


  def _plot_fully_scaled(self):
    self._get_plot_origin()
    self._get_plot_scale()
    self._axis_aspect_ratio  = self._axis_size_width / self._axis_size_height

    if self._axis_aspect_ratio > self._figure_aspect_ratio:
      self._axis_size_height = self._axis_size_width / self._figure_aspect_ratio
    else:
      self._axis_size_width = self._axis_size_height * self._figure_aspect_ratio

    plt.xlim( self._origin.x - (self._axis_size_width * 0.5), self._origin.x + (self._axis_size_width * 0.5) )
    plt.ylim( self._origin.y - (self._axis_size_height * 0.5), self._origin.y + (self._axis_size_height * 0.5) )
    self.fig.canvas.draw()


  def _incorporate_systems(self):
    for system in self.systems:
      for component in system.components:
        self.components.append(component)
      self.graphs.append(system.graph)


  def _draw_components(self):
    for component in self.components:
      patches = component.draw_component()
      self.patches.extend(patches)

    if len(self.patches) > 0:
      self.collection = PatchCollection(self.patches, match_original = True)
      self.ax.add_collection(self.collection)


  def _draw_nodes(self):
    for graph in self.graphs:
      self.node_patches.extend( graph.draw_nodes() )
    if len(self.graphs) > 0:
      if len(self.node_patches) > 0:
        self.node_collection = PatchCollection( self.node_patches, match_original = True)
        self.ax.add_collection(self.node_collection)


  def _draw_edges(self):
    for graph in self.graphs:
      self.edge_patches.extend( graph.draw_edges() )
    if len(self.graphs) > 0:
      if len(self.edge_patches) > 0:
        self.edge_collection = PatchCollection( self.edge_patches, match_original = True)
        self.ax.add_collection(self.edge_collection)


  def _draw_labels(self):

    # component labels
    for component in self.components:
      label = component.draw_label()
      if label is not None:
        self.labels.append(label)

    # graph labels
    for graph in self.graphs:
      self.labels.extend(graph.draw_node_labels())
      self.labels.extend(graph.draw_edge_labels())

    # junction labels
    for system in self.systems:
      for junction in system.junctions:
        if junction.name is not None:
          edge_name = junction.labeled_edge

          tail_name = system.graph.edges[edge_name].tail
          head_name = system.graph.edges[edge_name].head

          tail_coords = system.graph.nodes[tail_name]
          head_coords = system.graph.nodes[head_name]

          self.labels.append(junction.draw_label(tail_coords, head_coords))


  def _adjust_labels(self):
    ld_index = 0

    # component labels
    for component in self.components:
      if component.label is not None:
        component.adjust_label(self._labels_dimensions[ld_index])
        ld_index += 1

    def safe_adjust_label(dict, index):
      for comp in dict.values():
        if comp.label is not None:
          comp.adjust_label(self._labels_dimensions[index])
          index += 1
      return index

    # graph labels
    for graph in self.graphs:
      ld_index = safe_adjust_label(graph.nodes, ld_index)
      ld_index = safe_adjust_label(graph.edges, ld_index)

    # junction labels
    for system in self.systems:
      for junction in system.junctions:
        if junction.name is not None:
          junction.adjust_label(self._labels_dimensions[ld_index])
          ld_index += 1

    self.fig.canvas.draw()


  def draw(self, save_file = None, display = False, print_information = False):

    self._incorporate_systems()
    self._draw_components()
    self._draw_nodes()
    self._draw_edges()
    self._draw_labels()
    self._plot_tight_scaled()
    self._get_canvas_dimensions()
    self._get_label_dimensions()
    self._get_patch_dimensions()
    self._adjust_labels()
    self._plot_fully_scaled()

    if print_information:
      self.print_information()

    if (save_file != None):
      assert type(save_file) == str
      plt.savefig(save_file)

    plt.show(block = display)
