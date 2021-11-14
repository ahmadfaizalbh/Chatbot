#!/usr/bin/env python
from os.path import join, dirname, abspath
from runpy import run_path

from setuptools import setup

version = run_path(join(abspath(dirname(__file__)), 'chatbot', 'version.py'))
constants = run_path(join(abspath(dirname(__file__)), 'chatbot', 'constants.py'))

LANGUAGE_SUPPORT = constants['LANGUAGE_SUPPORT']
package_data = []

with open("README.md", "r") as fh:
    long_description = fh.read()

for language in LANGUAGE_SUPPORT:
    package_data.extend([
        "local/%s/default.template" % language,
        "local/%s/words.txt" % language,
        "local/%s/substitutions.json" % language
    ])
setup(
    name=constants['NAME'],
    version=version['__version__'],
    author=constants['AUTHOR'],
    author_email=constants['AUTHOR_EMAIL'],
    url=constants['URL'],
    description="A chatbot AI engine is a chatbot builder platform that provides both bot intelligence and"
                " chat handler with minimal codding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['chatbot', 'chatbot.spellcheck', 'chatbot.substitution'],
    license='MIT',
    keywords='chatbot ai engine and chat builder platform',
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    package_dir={
        'chatbot': 'chatbot',
        'chatbot.spellcheck': 'chatbot/spellcheck',
        'chatbot.substitution': 'chatbot/substitution'
    },
    include_package_data=True,
    package_data={"chatbot": package_data},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Natural Language :: Portuguese (Brazil)',
        'Natural Language :: Hebrew',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
    ],
    install_requires=[
        'requests',
    ]
)
