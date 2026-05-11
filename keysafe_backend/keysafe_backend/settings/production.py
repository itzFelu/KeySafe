from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "itzfelu.pythonanywhere.com"
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

MIDDLEWARE.insert(
    1,
    "whitenoise.middleware.WhiteNoiseMiddleware"
)