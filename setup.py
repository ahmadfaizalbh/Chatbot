#!/usr/bin/env python

from setuptools import setup

version = __import__('chatbot').__version__

setup(
    name='chatbotAI',
    version=version,
    author="Ahmad Faizal B H",
    author_email="ahmadfaizalbh726@gmail.com",
    url="https://github.com/ahmadfaizalbh/Chatbot",
    description="A chatbot AI engine is a chatbot builder platform that provids both bot intelligence and"
                " chat handler with minimal codding",
    long_description=open("README.rst").read(),
    packages=['chatbot', 'chatbot.spellcheck'],
    license='MIT',
    keywords='chatbot ai engine and chat builder platform',
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    package_dir={'chatbot': 'chatbot', 'chatbot.spellcheck': 'chatbot/spellcheck'},
    include_package_data=True,
    package_data={"chatbot":  ["local/en/default.template",
                               "local/en/words.txt",
                               "local/en/substitutions.json",
                               "local/pt-br/default.template"]},
    install_requires=[
          'requests',
      ]
)
