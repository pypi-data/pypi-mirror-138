# -*- encoding: utf-8 -*-
import os
import sys
from setuptools import find_packages, setup

__author__ = 'Yeongbin Jo <iam.yeongbin.jo@gmail.com>'

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# shortcuts (publish, clean)
if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()
elif sys.argv[-1] == 'clean':
    import shutil
    if os.path.isdir('build'):
        shutil.rmtree('build')
    if os.path.isdir('dist'):
        shutil.rmtree('dist')
    if os.path.isdir('django_unique_audit.egg-info'):
        shutil.rmtree('django_unique_audit.egg-info')

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-unique-audit',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "beautifulsoup4",
        "django>=2.2,<=4"
    ],
    python_requires=">=3.5",
    license='GPL3',
    description='An app that creates a unique django audit log across multiple instances.',
    long_description_content_type='text/markdown',
    long_description=README,
    url='https://github.com/yeongbin-jo/django-unique-audit',
    author='Yeongbin Jo',
    author_email='iam.yeongbin.jo@gmail.com',
    classifiers=[
        'Environment :: Plugins',
        'Framework :: Django',
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
