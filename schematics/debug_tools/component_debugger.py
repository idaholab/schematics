from __future__ import print_function

def component_debug_switch(description = None):
  import argparse
  parser = argparse.ArgumentParser(description = description)
  parser.add_argument('-db', '--debug', action = 'count',
                     help = 'enter debug mode if flag raised')
  args = parser.parse_args()

  if args.debug:
    from schematics import canvas
    print("Made it here")
