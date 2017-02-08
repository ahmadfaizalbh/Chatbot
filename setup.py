#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup

setup(
    name = 'chatbotAI',
    version='0.1.1.0',
    author = "Ahmad Faizal B H",
    author_email = "ahmadfaizalbh726@gmail.com",
    url="https://github.com/ahmadfaizalbh/Chatbot",
    description="A chatbot AI engine is a chatbot builder platform that provids both bot intelligence and chat handler with minimal codding",
    long_description=open("README.rst").read(),
    packages=['chatbot'],
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    package_dir={ 'chatbot': 'chatbot'}
)
