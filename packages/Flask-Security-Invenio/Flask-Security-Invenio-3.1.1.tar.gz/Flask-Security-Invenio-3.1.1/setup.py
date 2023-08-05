# -*- coding: utf-8 -*-

"""Simple security for Flask apps."""

import io
import re
from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with io.open('flask_security/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

tests_require = [
    'bcrypt>=3.1.0',
    'check-manifest>=0.42',
    'coverage>=5.3,<6',
    'Flask-Sphinx-Themes>=1.0.2',
    'Flask-SQLAlchemy>=2.5.1',
    'mock>=1.3.0',
    'msgcheck>=2.9',
    'pytest-cov>=2.10.1',
    'pytest-flask>=1.0.0',
    'pytest-isort>=1.2.0',
    'pytest-pycodestyle>=2.2.0',
    'pytest-pydocstyle>=2.2.0',
    'pytest>=6,<7',
]

extras_require = {
    'docs': [
        'Sphinx>=4.2.0',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=2.8',
]

install_requires = [
    'email-validator>=1.0.5',
    'Flask-BabelEx>=0.9.4',
    'Flask-Login>=0.4.0',
    'Flask-Mail>=0.9.1',
    'Flask-Principal>=0.4.0',
    'Flask-WTF>=1.0.0',
    'Flask>=2.0',
    'itsdangerous>=2.0',
    'passlib>=1.7',
]

packages = find_packages()

setup(
    name='Flask-Security-Invenio',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='flask security',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    maintainer='CERN',
    maintainer_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/flask-security-invenio',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
