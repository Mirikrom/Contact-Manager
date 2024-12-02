import os
import sys

# Django loyihangiz joylashgan papkani aniqlang
project_path = '/home/mirikrom/contacts_manager'
if project_path not in sys.path:
    sys.path.append(project_path)

# Django sozlamalar faylini ko'rsating
os.environ['DJANGO_SETTINGS_MODULE'] = 'contacts.settings'

# WSGI applicationni yarating
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()