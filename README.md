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