from __future__ import print_function

from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Pentagon graph test case.')
command_line_parser.add_argument('-dir', default = '.', help='directory to be run')
args = command_line_parser.parse()

import sys
from subprocess import call
from os import chdir, getcwd, listdir
from os.path import join

def run_all(prefix = ''):
  path = getcwd()
  files = listdir(path)
  if __file__ in files:
    files.remove(__file__)

  # remove files
  remove_files = []
  for file in files:
    if file[0] == '.':
      remove_files.append(file)
  for file in remove_files:
    files.remove(file)

  for file in files:
    if file[-3:] == '.py':
      if prefix == '':
        print('\nprocessing...', file)
      else:
        print('\nprocessing...', prefix + '/' + file)
      call([sys.executable, file])

    elif file[-4:] != '.pdf':
      original_dir = getcwd()
      chdir(file)
      prefix = prefix + '/' + file
      run_all(prefix)
      chop_length = -1 * (len(file) + 1)
      prefix = prefix[:chop_length]
      chdir(original_dir)

original_dir = getcwd()
chdir(args.dir)
run_all()
chdir(original_dir)
