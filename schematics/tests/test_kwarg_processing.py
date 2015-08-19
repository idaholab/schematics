from unittest import TestCase

from schematics import KwargProcessing

class TestKwargProcessing(TestCase):

  def test_instantiation(self):
    process_dog = KwargProcessing('dog', 'doggy', 'd')
    self.assertEqual(process_dog.type, None)
    self.assertEqual(process_dog.names, ('dog', 'doggy', 'd'))
    self.assertEqual(process_dog.pop, True)


  def test_no_input(self):
    process_dog = KwargProcessing('dog', 'doggy', 'd')
    self.assertFalse(process_dog(False, 'cat'))


  def test_all_inputs(self):
    process_dog = KwargProcessing('dog', 'doggy', 'd')

    def isDog(**kwargs):
      dog = process_dog(False, kwargs)
      return dog

    self.assertTrue( isDog(d = True) )
    self.assertTrue( isDog(dog = True) )
    self.assertTrue( isDog(doggy = True) )
