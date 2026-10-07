# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# PythonAnywhere WSGI configuration file for Sand Aggregates (LJ ENTERPRISE)
#
# Replace the contents of /var/www/<username>_pythonanywhere_com_wsgi.py with this!
# (Make sure to replace '<your-username>' with your actual PythonAnywhere username)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import sys

# 1. Project path: where manage.py and settings.py are located
# Adjust the username if needed:
USERNAME = '<your-username>'
project_home = f'/home/{USERNAME}/Sand_aggregates/sand_aggregates'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 2. Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'sand_aggregates.settings'

# 3. Optional: load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(project_home, '.env'))
except ImportError:
    pass

# 4. Set up Django WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
