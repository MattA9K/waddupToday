import os
import sys
sys.path = ['/var/www/django_site'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'cms.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
