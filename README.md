# Deep Shell GTK

A modern terminal-like interface built with GTK and Python, featuring a transparent background with 95% opacity and an embedded terminal.

## Requirements

- Python 3.x
- GTK 3.0
- PyGObject
- VTE Terminal

## Installation

1. Install system dependencies (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-vte-2.91
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/deep-shell-gtk.git
cd deep-shell-gtk
```

## Running the Application

1. Make the main script executable:
```bash
chmod +x main.py
```

2. Run the application:
```bash
./main.py
```

## Features

- Modern, transparent UI with 95% opacity
- Chat-like interface
- Message history with automatic scrolling
- Settings and reset buttons
- Responsive design
- Custom styling with CSS
- Embedded terminal with transparency support
- Split view layout

## License

MIT License

# DeepShell4

An AI-powered terminal interface that combines the power of AI with a traditional terminal experience.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DeepShell4.git
cd DeepShell4
```

2. Set up your API keys:
   - Copy `settings.json.template` to `settings.json`
   - Add your API key to `settings.json`
   ```bash
   cp settings.json.template settings.json
   # Edit settings.json and add your API key
   ```

   **IMPORTANT: Never commit your API keys to the repository!**

## API Keys

This application requires API keys for AI services:
- For Gemini: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- For Groq: Get your API key from [Groq Cloud](https://console.groq.com/)

Store your API keys securely and never share them or commit them to version control.

## Installation

### From Source
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Using Debian Package
```bash
# Build the package
dpkg-deb --build deepshell

# Install the package
sudo dpkg -i deepshell.deb
```

## Features

* AI chat interface with multiple model support (Gemini, Groq)
* Integrated terminal emulator
* Modern GTK-based user interface
* Support for multiple AI providers

## Security Notes

1. Always keep your API keys secure
2. Never commit sensitive credentials to Git
3. Use environment variables or secure credential storage when possible
4. Regularly rotate your API keys
5. Monitor your API usage for any unauthorized access 