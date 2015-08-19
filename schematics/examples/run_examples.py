from schematics import ExampleDebugger
command_line_parser = ExampleDebugger('Pentagon graph test case.')
command_line_parser.add_argument('-dir', default = '.', help='directory to be run')
args = command_line_parser.parse()

from subprocess import check_output
from subprocess import call
from os import chdir, getcwd

def run_all(prefix = ''):
  files = check_output(['ls']).splitlines()
  if __file__ in files:
    files.remove(__file__)

  for file in files:
    if file[-3:] == '.py':
      if prefix == '':
        print '\nprocessing...', file
      else:
        print '\nprocessing...', prefix + '/' + file
      call(['python', file])

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
