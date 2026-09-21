"""
WSGI config for sand_aggregates project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sand_aggregates.settings')

application = get_wsgi_application()
