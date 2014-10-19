"""
WSGI config for procyon.

"""
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "procyon.settings")

import procyon.startup as startup
startup.run()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
