"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
import os, sys
print("DJANGO_SETTINGS_MODULE:", os.getenv("DJANGO_SETTINGS_MODULE"))
print("PYTHONPATH:", "\n".join(sys.path))
print("Existe core/__init__.py?", os.path.exists(os.path.join(sys.path[0], "core", "__init__.py")))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
