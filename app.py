import os
from school_management.wsgi import application

# Expose 'app' for Render's default 'gunicorn app:app' start command
app = application
application = application
