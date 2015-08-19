import sys

class Rectangle(object):
  def __init__(self, width = 1.0, height = 1.0):
    self.width = width
    self.height = height

  def __str__(self):
    return '(w = ' + str(self.width) + ', h = ' + str(self.height) + ')'
