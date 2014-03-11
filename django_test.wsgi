import os
import sys
sys.path = ['/root/django-test-server/django_test'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_test.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

