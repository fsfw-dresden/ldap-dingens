#!/usr/bin/env python3
from setuptools import setup

setup(
    name="ldap_dingens",
    version="0.1",
    description="LDAP web frontend for the FSFW Dresden group",
    url="https://github.com/fsfw-dresden/ldap-dingens",
    author="Dominik Pataky",
    author_email="mail@netdecorator.org",
    license="AGPL",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    keywords="ldap web-frontend flask",
    install_requires=[
        "Flask>=0.10.1",
        "Flask-Login>=0.2.11",
        "Flask-WTF>=0.10",
        "itsdangerous>=0.24",
        "Jinja2>=2.7.3",
        "MarkupSafe>=0.23",
        "SQLAlchemy>=0.9.9",
        "Werkzeug>=0.9.6",
        "WTForms>=2.0",
        "blinker>=1.3"
    ],
    packages=["ldap_dingens"],
    package_data={
        "ldap_dingens": [
            "static/css/*.css",
            "templates/*.html",
            "templates/invite/*.html",
        ]
    },
)
