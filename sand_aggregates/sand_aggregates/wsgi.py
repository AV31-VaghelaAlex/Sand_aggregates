"""
WSGI config for sand_aggregates project.
Production and WSGI server compatible (e.g. PythonAnywhere, Gunicorn).
"""

import os
import sys
from pathlib import Path

# Ensure project root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Load .env variables if present
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sand_aggregates.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
