from __future__ import absolute_import, print_function

import os
import sys
import unittest
import logging

def assert_path(module):
    module = os.path.abspath( module )

    if module not in sys.path:
        sys.path.insert( 0, module )

assert_path( os.path.join( os.path.basename( os.path.realpath( __file__ ) ), '..', 'source' ) )

from .test_trees import TestTrees
from .test_tools import TestStandalone
from .test_reconstructor import TestReconstructor

try:
    from .test_nearley.test_nearley import TestNearley
except ImportError:
    pass

# from .test_selectors import TestSelectors
# from .test_grammars import TestPythonG, TestConfigG

from .test_parser import (
        TestLalrStandard,
        TestEarleyStandard,
        TestCykStandard,
        TestLalrContextual,
        # TestEarleyScanless,
        TestEarleyDynamic,

        # TestFullEarleyScanless,
        TestFullEarleyDynamic,

        TestParsers,
        )

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    unittest.main()
