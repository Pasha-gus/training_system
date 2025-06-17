from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
        "TEST": {
            "NAME": BASE_DIR / "test_db.sqlite3",
        },
        "ATOMIC_REQUESTS": False,
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

CELERY_BROKER_URL = None
CELERY_RESULT_BACKEND = None
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'