import os
import unittest
import logging
import sys
from optparse import OptionParser

sys.path.insert(1, "./lib")

# parser = OptionParser()
# parser.add_option("-l", "--log", dest="loglevel", default=str(logging.WARNING))

# (options, args) = parser.parse_args()
# print("options: ", options, args)


# if "loglevel" in options.keys():


# options = defaultdict(options)

# loglevel


numeric_level = logging.DEBUG
print("Logging level: ", numeric_level)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level)

all_tests = unittest.TestLoader().discover(os.path.join(os.path.dirname(__file__), "test"), "test_*.py")
unittest.TextTestRunner(verbosity=2).run(all_tests)