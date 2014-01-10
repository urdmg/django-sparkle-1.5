import os

from django.conf import settings

SPARKLE_PRIVATE_KEY_PATH = getattr(settings, 'SPARKLE_PRIVATE_KEY_PATH', None)

UPLOAD_PREFIX = getattr(settings, 'SPARKLE_UPLOAD_PREFIX', 'sparkle/')

SYSTEM_PROFILES_VISIBLE = getattr(settings, 'SPARKLE_SYSTEM_PROFILES_VISIBLE', False)