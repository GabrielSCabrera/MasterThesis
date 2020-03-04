import argparse
import sys

from scripts import *

if '-test' in sys.argv:
    tests.run_tests()
