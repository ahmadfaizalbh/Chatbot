# Ollama Installation Guide

This chatbot uses Ollama with Llama 3.2:1b for AI responses. Follow the instructions below for your operating system.

## Windows

### Method 1: Direct Download
1. Download Ollama from: https://ollama.ai/download/windows
2. Run the installer (.exe file)
3. Open Command Prompt or PowerShell
4. Pull the model:
   ```cmd
   ollama pull llama3.2:1b
   ```

### Method 2: Using Winget
```cmd
winget install Ollama.Ollama
ollama pull llama3.2:1b
```

## macOS

### Method 1: Direct Download
1. Download Ollama from: https://ollama.ai/download/mac
2. Open the .dmg file and drag Ollama to Applications
3. Open Terminal
4. Pull the model:
   ```bash
   ollama pull llama3.2:1b
   ```

### Method 2: Using Homebrew
```bash
brew install ollama
ollama pull llama3.2:1b
```

## Linux

### Method 1: Install Script (Recommended)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:1b
```

### Method 2: Manual Installation

#### Ubuntu/Debian
```bash
curl -fsSL https://ollama.ai/gpg | sudo gpg --dearmor -o /usr/share/keyrings/ollama-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/ollama-keyring.gpg] https://repo.ollama.ai ubuntu main" | sudo tee /etc/apt/sources.list.d/ollama.list
sudo apt update
sudo apt install ollama
ollama pull llama3.2:1b
```

#### CentOS/RHEL/Fedora
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:1b
```

## Verification

Test your installation:
```bash
ollama run llama3.2:1b "Hello, how are you?"
```

You should see a response from the AI model.

## Troubleshooting

### Common Issues

1. **"ollama: command not found"**
   - Restart your terminal/command prompt
   - Check if Ollama is in your PATH
   - Try the full path: `/usr/local/bin/ollama` (Linux/Mac)

2. **Model download fails**
   - Check internet connection
   - Try: `ollama pull llama3.2:1b --verbose`

3. **Permission denied (Linux)**
   - Add user to ollama group: `sudo usermod -aG ollama $USER`
   - Logout and login again

4. **Port already in use**
   - Ollama uses port 11434 by default
   - Stop other Ollama instances: `ollama stop`

## System Requirements

- **RAM**: Minimum 4GB (8GB recommended for llama3.2:1b)
- **Storage**: ~2GB for the model
- **OS**: Windows 10+, macOS 10.15+, Linux (most distributions)

## Alternative Models

If llama3.2:1b is too large, try smaller models:
```bash
ollama pull llama3.2:3b    # Larger, better quality
ollama pull phi3:mini      # Smaller, faster
```

Update the model name in the chatbot code:
```python
self.ai_model = "phi3:mini"  # Change this line
```