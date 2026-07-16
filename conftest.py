import os
import sys

# Explicitly add the project root to the Python path so pytest can find the 'src' module on any OS
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
