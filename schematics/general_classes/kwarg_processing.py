import sys

class KwargProcessing(object):
  all_names = []

  def __init__(self, *names, **pop):
    self.type = None
    self.names = names

    # Warn user about potential name conflicts
    for name in self.names:
      if name not in KwargProcessing.all_names:
        KwargProcessing.all_names.append(name)
      else:
        print 'Warning: "' + name + '" duplicated when defining kwarg processors.'

    if 'pop' in pop:
      self.pop = pop['pop']
    else:
      self.pop = True


  def __call__(self, default, kwargs):
    # processing default and setting type
    self.default = default
    # determine type of the default
    if self.type is None:
      if self.default is None:
        self.type = type('string')
      else:
        self.type = type(self.default)

    # check that default type is consistent if kwarg has already been used
    else:
      default_type = type(self.default)

      default_is_number = (default_type == float) or (default_type == int)
      type_is_number = (self.type == float) or (self.type == int)
      one_is_and_other_isnt_number = (default_is_number and not type_is_number) or (type_is_number and not default_is_number)

      default_is_string = (default_type == str) or (self.default is None)
      type_is_string = (self.type == str)
      one_is_and_other_isnt_string = (default_is_string and not type_is_string) or (type_is_string and not default_is_string)

      type_isnt_number_or_string = not ((self.type == str) or (self.type == int) or (self.type == float))

      if (self.type != default_type):
        if (one_is_and_other_isnt_number or one_is_and_other_isnt_string or type_isnt_number_or_string):
          sys.exit('Error: the default\'s type is not consistent with what was ' +
                   'previously sepcified. (' + str(self.names) + ')')

    # checking if kwarg is supplied and returns value if it is and is valid
    declared_names = []
    for name in self.names:
      if name in kwargs:
        declared_names.append(name)

    if len(declared_names) == 0:
      return self.default

    elif len(declared_names) == 1:
      if self.pop:
        value = kwargs.pop(declared_names[0])
      else:
        value = kwargs[declared_names[0]]

      # type checking
      value_type = type(value)
      if value_type == self.type:
        return value

      elif self.type == float or self.type == int:
        if value_type == float or value_type == int:
          return value
        else:
          sys.exit('Error: invalid data type for the variable "' + self.names[0] +
                  '" ' + str(self.names) + '. Expected a value of the type '
                  + str(self.type) + '.')

      elif self.type == str:
        if value is None or value_type == str:
          return value
        else:
          sys.exit('Error: invalid data type for the variable "' + self.names[0] +
                  '" ' + str(self.names) + '. Expected a value of the type '
                  + str(self.type) + '.')

    else:
      sys.exit('Error: the variable "' + self.names[0] + '" was specified '
               'multiple times. ' + str(self.names))


# Common KwargProcessing Instances:
from copy import copy
process_name = KwargProcessing('name', 'n')

process_angle = KwargProcessing('angle', 'a', pop = False)
process_reflect = KwargProcessing('reflect', 'ref', pop = False)

process_label_location = KwargProcessing('label_location', 'll')
process_label_string = KwargProcessing('label_string', 'ls')
process_label_angle = KwargProcessing('label_angle', 'la')
process_label_pad = KwargProcessing('label_padding', 'label_pad', 'lp')
process_label_shift = KwargProcessing('label_shift', 'shift')
process_font_size = KwargProcessing('font_size', 'fs')
process_face_color = KwargProcessing('face_color', 'fc')
process_edge_color = KwargProcessing('edge_color', 'ec')
process_line_width = KwargProcessing('line_width', 'lw')
process_alpha = KwargProcessing('alpha')
process_face_alpha = KwargProcessing('face_alpha')
process_edge_alpha = KwargProcessing('edge_alpha')

process_radius = KwargProcessing('radius', 'rad')

process_directional = KwargProcessing('directional', 'direction', 'dir')
process_width = KwargProcessing('width', 'w')
process_head_width_to_width = KwargProcessing('head_width_to_width', 'hw_to_w')
process_head_length_to_head_width = KwargProcessing('head_length_to_head_width', 'hl_to_hw')
process_overhang = KwargProcessing('overhang', 'oh')

process_graphs = KwargProcessing('graphs', 'g')

process_label_edge_number = KwargProcessing('label_edge_number', 'len')

process_draw = KwargProcessing('draw', 'd')
process_draw_label = KwargProcessing('draw_label', 'dl')
