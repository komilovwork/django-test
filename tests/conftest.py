import os
import django
import pytest

# Ensure DJANGO_SETTINGS_MODULE is set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

@pytest.fixture(scope='session', autouse=True)
def setup_django():
    django.setup()
