#!/usr/bin/env python

from os.path import join, dirname, abspath
from runpy import run_path
from setuptools import setup


version = run_path(join(abspath(dirname(__file__)), 'chatbot', 'version.py'))
constants = run_path(join(abspath(dirname(__file__)), 'chatbot', 'constants.py'))
LANGUAGE_SUPPORT = constants['LANGUAGE_SUPPORT']
package_data = ["media/send.png", "media/robot.png", "media/user.png"]

with open("README.md", "r") as fh:
    long_description = fh.read()

for language in LANGUAGE_SUPPORT:
    package_data.extend([
        "local/%s/default.template" % language,
        "local/%s/words.txt" % language,
        "local/%s/substitutions.json" % language
    ])
package_dir = {
        'chatbot': 'chatbot',
        'chatbot.spellcheck': 'chatbot/spellcheck',
        'chatbot.substitution': 'chatbot/substitution',
        'chatbot.chat_gui': 'chatbot/chat_gui'
    }
setup(
    name='chatbotAI',
    version=version['__version__'],
    author="Ahmad Faizal B H",
    author_email="ahmadfaizalbh726@gmail.com",
    url="https://github.com/ahmadfaizalbh/Chatbot",
    description="A chatbot AI engine is a chatbot builder platform that provides both bot intelligence and"
                " chat handler with minimal codding",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=list(package_dir.keys()),
    license='MIT',
    keywords='chatbot ai engine and chat builder platform',
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    package_dir=package_dir,
    include_package_data=True,
    package_data={"chatbot":  package_data},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Natural Language :: Portuguese (Brazilian)',
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
