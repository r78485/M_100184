import os
import sys

# Ensure project root is on Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from school_management.wsgi import application

# Vercel serverless function entrypoints
app = application
handler = application
