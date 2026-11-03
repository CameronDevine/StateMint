import os
import sys

# Let the test modules import each other (test_features reuses test_suite).
sys.path.insert(0, os.path.dirname(__file__))
