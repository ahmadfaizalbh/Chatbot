#!/usr/bin/env python

from setuptools import setup

chatbot = __import__('chatbot')
version = chatbot.__version__
LANGUAGE_SUPPORT = chatbot.LANGUAGE_SUPPORT
package_data = []
for language in LANGUAGE_SUPPORT:
    package_data.extend([
        "local/%s/default.template" % language,
        "local/%s/words.txt" % language,
        "local/%s/substitutions.json" % language
    ])
setup(
    name='chatbotAI',
    version=version,
    author="Ahmad Faizal B H",
    author_email="ahmadfaizalbh726@gmail.com",
    url="https://github.com/ahmadfaizalbh/Chatbot",
    description="A chatbot AI engine is a chatbot builder platform that provids both bot intelligence and"
                " chat handler with minimal codding",
    long_description=open("README.rst").read(),
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
    package_data={"chatbot":  package_data},
    install_requires=[
          'requests',
      ]
)
