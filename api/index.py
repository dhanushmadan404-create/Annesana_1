import sys
import os

# Add the 'backend' folder to the system path so we can import from it
# This tells python that the backend code is located one directory up, then in 'backend/'
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

# Import the FastAPI 'app' from main.py
from main import app
