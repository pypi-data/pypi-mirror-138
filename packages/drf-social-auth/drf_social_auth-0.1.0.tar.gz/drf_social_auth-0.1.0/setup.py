#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
from setuptools import find_packages, setup


try:
    import django
    from django.conf import settings

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="tests.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",

            "rest_framework"
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        FIXTURE_DIRS=['tests/fixtures'],
        GOOGLE_CLIENT_ID='test',
        GOOGLE_CLIENT_SECRET='test',
        GOOGLE_REDIRECT_URI='test'
    )
    django.setup()


except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements.txt")


name = 'drf_social_auth'
package = 'rest_framework_social_auth'
description = 'DRF_social_auth is an ultra-lightweight solution for social authentication support in Django REST Framework.'
url = 'https://github.com/coaxsoft/drf-social-auth'
author = 'Vitalii Bazhenov'
author_email = 'vitalii.bazhenov@coaxsoft.com'
license = 'ISC'


def read(f):
    return open(f, 'r', encoding='utf-8').read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


version = get_version(package)


setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author=author,
    author_email=author_email,
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    keywords='django rest_framework drf social auth',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
    project_urls={
        'Source': url,
    },
)
