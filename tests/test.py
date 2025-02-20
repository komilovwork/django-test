from django.conf import settings
import pytest

def test_secret_key():
    assert hasattr(settings, 'SECRET_KEY')  # Check if SECRET_KEY exists
    assert settings.SECRET_KEY is not None  # Ensure it's not None

def test_debug():
    assert hasattr(settings, 'DEBUG')  # Check if SECRET_KEY exists
    assert settings.DEBUG is not None  # Ensure it's not None

def func(x):
    return x + 1

def test_answer():
    assert func(4) == 5

def test_function():
    assert 5 == 5

def test1_function():
    assert 5 == 5