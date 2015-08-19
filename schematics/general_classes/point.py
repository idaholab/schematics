import sys
from math import sqrt

def print_points(points):
  '''Prints the values of a list of points'''
  sys.stdout.write('[')
  for i, point in enumerate(points):
    sys.stdout.write(str(point))
    if i != (len(points)-1):
      sys.stdout.write(', ')
  print ']'


class Point(object):
  def __init__(self, x = 0.0, y = 0.0):
    self.x = x
    self.y = y


  def to_tuple(self):
    return (self.x, self.y)


  def __str__(self):
    return '(' + str(self.x) + ', ' + str(self.y) + ')'


  def __eq__(self, other):
    return (self.x == other.x) and (self.y == other.y)


  def __ne__(self, other):
    return not self.__eq__(other)


  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)


  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)


  def __abs__(self):
    return sqrt((self.x ** 2) + (self.y ** 2))
