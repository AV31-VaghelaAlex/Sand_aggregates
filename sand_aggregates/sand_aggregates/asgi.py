"""
ASGI config for sand_aggregates project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sand_aggregates.settings')

application = get_asgi_application()
