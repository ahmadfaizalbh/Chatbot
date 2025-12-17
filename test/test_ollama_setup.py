#!/usr/bin/env python3
"""
Test script for Ollama setup functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from setup import install_ollama

if __name__ == "__main__":
    print("Testing Ollama setup functionality...")
    install_ollama()