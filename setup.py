#!/usr/bin/env python

import subprocess
import platform
import shutil
from os.path import join, dirname, abspath
from runpy import run_path
from setuptools import setup
from setuptools.command.install import install


def install_ollama():
    """Install Ollama based on the operating system"""
    system = platform.system().lower()
    
    print("\n🚀 Setting up Ollama for AI responses...")
    
    # Check if ollama is already installed
    if shutil.which("ollama"):
        print("✅ Ollama is already installed!")
    else:
        print(f"📦 Installing Ollama for {system}...")
        
        if system == "windows":
            try:
                result = subprocess.run(["winget", "install", "Ollama.Ollama"], 
                                      capture_output=True, text=True, encoding='utf-8', errors='ignore', check=False)
                if result.returncode == 0 or "already installed" in result.stdout.lower():
                    print("✅ Ollama installed successfully!")
                else:
                    raise subprocess.CalledProcessError(result.returncode, result.args)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("❌ Automatic installation failed. Please install manually:")
                print("1. Download from: https://ollama.ai/download/windows")
                print("2. Or use: winget install Ollama.Ollama")
        elif system == "darwin":  # macOS
            try:
                subprocess.run(["brew", "install", "ollama"], check=True)
                print("✅ Ollama installed successfully!")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("❌ Automatic installation failed. Please install manually:")
                print("1. Download from: https://ollama.ai/download/mac")
                print("2. Or use: brew install ollama")
        elif system == "linux":
            try:
                result = subprocess.run(["curl", "-fsSL", "https://ollama.ai/install.sh"], 
                                      capture_output=True, check=True)
                subprocess.run(["sh"], input=result.stdout, check=True)
                print("✅ Ollama installed successfully!")
            except subprocess.CalledProcessError:
                print("❌ Failed to install Ollama automatically.")
                print("Please install manually: curl -fsSL https://ollama.ai/install.sh | sh")
    
    # Try to pull the model using Python ollama package
    try:
        print("📥 Downloading Llama 3.2:1b model...")
        import ollama
        ollama.pull("llama3.2:1b")
        print("✅ Model downloaded successfully!")
    except Exception:
        print("⚠️  Could not download model automatically.")
        print("Please ensure Ollama service is running and try again.")
    
    print("\n🎉 Setup complete! Your chatbot now has AI superpowers!")

class CustomInstall(install):
    """Custom install command that sets up Ollama"""
    
    def run(self):
        # Run the standard installation
        install.run(self)
        
        # Ask user if they want to install Ollama
        try:
            response = input("\n🤖 Install Ollama for AI responses? (y/N): ").lower().strip()
            if response in ['y', 'yes']:
                install_ollama()
            else:
                print("\n📖 You can install Ollama later using the OLLAMA_SETUP.md guide")
        except (KeyboardInterrupt, EOFError):
            print("\n📖 Skipping Ollama setup. See OLLAMA_SETUP.md for manual installation.")

version = run_path(join(abspath(dirname(__file__)), 'chatbot', 'version.py'))
constants = run_path(join(abspath(dirname(__file__)), 'chatbot', 'constants.py'))
LANGUAGE_SUPPORT = constants['LANGUAGE_SUPPORT']
package_data = ["media/send.png", "media/robot.png", "media/user.png", "OLLAMA_SETUP.md"]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for language in LANGUAGE_SUPPORT:
    package_data.extend([
        f"local/{language}/default.template",
        f"local/{language}/words.txt",
        f"local/{language}/substitutions.json"
    ])
package_dir = {
        'chatbot': 'chatbot',
        'chatbot.spellcheck': 'chatbot/spellcheck',
        'chatbot.substitution': 'chatbot/substitution',
        'chatbot.chat_gui': 'chatbot/chat_gui'
    }
if __name__ == "__main__":
    setup(
        name='chatbotAI',
        version=version['__version__'],
        author="Ahmad Faizal B H",
        author_email="ahmadfaizalbh726@gmail.com",
        url="https://github.com/ahmadfaizalbh/Chatbot",
        description="A chatbot AI engine with Ollama integration for state-of-the-art AI responses",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=list(package_dir.keys()),
        license='MIT',
        keywords='chatbot ai engine ollama llama chat builder platform',
        platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
        package_dir=package_dir,
        include_package_data=True,
        package_data={"chatbot":  package_data},
        python_requires='>=3.9',
        cmdclass={'install': CustomInstall},
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
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Communications :: Chat',
        ],
        install_requires=[
              'requests>=2.25.0',
              'ollama>=0.1.0',
          ],
        # No extensions needed - using Ollama for AI
    )
