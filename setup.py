#!/usr/bin/env python
from distutils.core import setup
    
setup(
    name = 'chatbot',
    version='0.1.0.2',
    author = "Ahmad Faizal B H",
    author_email = "ahmadfaizalbh726@gmail.com",
    description = ("A python chatbot"),
    packages=['chatbot'],
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    package_dir={ 'chatbot': 'chatbot'}
)
