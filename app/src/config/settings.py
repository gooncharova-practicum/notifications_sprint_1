import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY") or get_random_secret_key()

DEBUG = os.environ.get("DEBUG", False) == "True"

ALLOWED_HOSTS = list((os.environ.get("ALLOWED_HOSTS") or "127.0.0.1,").split(","))
CSRF_TRUSTED_ORIGINS = list(
    (os.environ.get("CSRF_TRUSTED_ORIGINS") or "http://127.0.0.1,").split(",")
)

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = "/var/www/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCALE_PATHS = ["notify/locale"]

CORS_ORIGIN_ALLOW_ALL = os.environ.get("CORS_ORIGIN_ALLOW_ALL", False) == "True"

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}

FASTAPI_PROJECT_TITLE = os.environ.get("FASTAPI_PROJECT_TITLE")
FASTAPI_PROJECT_DESCRIPTION = os.environ.get("FASTAPI_PROJECT_DESCRIPTION")
FASTAPI_PROJECT_VERSION = os.environ.get("FASTAPI_PROJECT_VERSION")
FASTAPI_DOCS_URL = "/api/v1/swagger"
FASTAPI_OPENAPI_URL = "/api/v1/openapi.json"

include(
    "components/*.py",
)
