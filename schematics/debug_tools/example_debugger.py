import sys
from subprocess import call
from os import getcwd
from os import chdir
import pdb
import argparse

class ExampleDebugger(argparse.ArgumentParser):

  def __init__(self, description = None):

    super(ExampleDebugger, self).__init__(description = description)
    self.add_argument('-t', '--test', action = 'count',
                      help = 'run unittests before running example.')
    self.add_argument('-i', '--install', action = 'count',
                      help = 'install app before running example.')
    self.add_argument('-db', '--debug', action = 'count',
                      help = 'enter debug mode if flag raised')

  def parse(self):
    args = self.parse_args()

    def run_setup_script(command):
      original_dir = getcwd()
      chdir('../..')
      call([sys.executable, 'setup.py', command])
      chdir(original_dir)
      sys.exit('\nSchematics ' + command + 'ed ... ')

    if args.test:
      run_setup_script('test')
    del(args.test)

    if args.install:
      run_setup_script('install')
    del(args.install)

    if args.debug:
      pdb.set_trace()
    del(args.debug)

    return args
