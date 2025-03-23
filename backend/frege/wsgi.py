import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frege.settings")

application = get_wsgi_application()

application = WhiteNoise(application, root=settings.STATIC_ROOT)
application.add_files(settings.MEDIA_ROOT, prefix='media')