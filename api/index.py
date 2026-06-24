import os
import sys

# Add the root directory to the python path so that 'app' can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app

app = create_app()

# This tells Vercel to expose 'app'
