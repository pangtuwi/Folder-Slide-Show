# Folder Slide Show

A lightweight Python-based image slideshow application that recursively searches directories for images and displays them in a clean, full-featured viewer.

## Features

- **Recursive Directory Search** - Automatically finds all images in nested folder structures
- **Auto-Play Mode** - Images advance automatically with configurable delay
- **Manual Navigation** - Browse images with arrow keys
- **Fullscreen Support** - Toggle fullscreen mode on/off
- **Aspect Ratio Preservation** - Images are scaled to fit the window while maintaining proportions
- **Multiple Format Support** - Works with `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.tiff`, `.tif`
- **Progress Tracking** - Status bar shows current image position and file path

## Requirements

- **Python 3.12** (via Homebrew) with Tkinter support
- **Pillow** (PIL) library

### macOS Installation

The system Python on macOS has a broken Tkinter implementation. You must use Homebrew Python:

```bash
# Install Homebrew Python
brew install python@3.12

# Install Tkinter support
brew install python-tk@3.12

# Install Pillow
/opt/homebrew/bin/python3.12 -m pip install --break-system-packages Pillow
```

## Usage

### Basic Usage

```bash
# Run with default settings (current directory, 3 second delay)
./slideshow.py

# Run with specific directory
./slideshow.py /path/to/photos

# Run in fullscreen with 5 second delay
./slideshow.py /path/to/photos --fullscreen --delay 5

# Manual mode (no auto-advance)
./slideshow.py /path/to/photos --delay 0
```

### Command Line Options

```
usage: slideshow.py [-h] [-f] [-d DELAY] [directory]

positional arguments:
  directory             Root directory to search for images (default: current directory)

optional arguments:
  -h, --help            Show help message
  -f, --fullscreen      Start in fullscreen mode
  -d DELAY, --delay DELAY
                        Delay between images in seconds (0 = manual only, default: 3)
```

## Controls

| Key | Action |
|-----|--------|
| `Right Arrow` | Next image |
| `Left Arrow` | Previous image |
| `Space` | Toggle auto-play on/off |
| `F` | Toggle fullscreen mode |
| `Q` or `Escape` | Quit application |

## How It Works

The application:
1. Recursively scans the specified directory for image files
2. Sorts images by path for consistent ordering
3. Displays images in a Tkinter window with aspect-ratio-preserving scaling
4. Automatically advances to the next image (if auto-play is enabled)
5. Handles window resizing dynamically

## License

This project is open source and available for use.

## Acknowledgments

Built with Python, Tkinter, and Pillow (PIL).
