from distutils.debug import DEBUG
from django.conf import settings

def pytest_configure():
    settings.configure()
