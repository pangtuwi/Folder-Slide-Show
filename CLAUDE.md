# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Folder Slide Show - Image Slideshow Application

A Python-based image slideshow application that recursively searches directories for images and displays them in a Tkinter GUI.

**Tech Stack**:
- Python 3.12 (via Homebrew - required for working Tkinter on macOS)
- Tkinter (GUI) - installed via `python-tk@3.12`
- Pillow/PIL (image processing)

**Key Features**:
- Recursive directory search for images
- Auto-play with configurable delay
- Manual navigation (arrow keys)
- Fullscreen mode toggle
- Supports: .jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff, .tif

## Installation

**Important**: macOS system Python (`/usr/bin/python3`) has a broken Tkinter implementation that doesn't render widgets. You MUST use Homebrew Python.

```bash
# Install Homebrew Python
brew install python@3.12

# Install Tkinter support
brew install python-tk@3.12

# Install Pillow
/opt/homebrew/bin/python3.12 -m pip install --break-system-packages Pillow
```

## Running the Application

The script has a shebang pointing to `/opt/homebrew/bin/python3.12`, so you can run it directly:

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

Or explicitly use Homebrew Python:

```bash
/opt/homebrew/bin/python3.12 slideshow.py /path/to/photos
```

## Application Controls

- Right Arrow: Next image
- Left Arrow: Previous image
- Space: Toggle auto-play
- F: Toggle fullscreen
- Q or Escape: Quit

## Architecture

Single-file application with `ImageSlideshow` class that:
1. Recursively finds images using `Path.rglob()`
2. Maintains image list sorted by path
3. Uses Tkinter Label for image display with aspect-ratio-preserving thumbnail resizing
4. Implements auto-advance timer with `root.after()` scheduling
5. Handles window resize events with debouncing to redisplay current image at new size
6. Uses PhotoImage to convert PIL images for Tkinter display

## Known Issues

- **macOS System Python**: The built-in Python on macOS has a broken Tkinter that doesn't render widgets properly. Always use Homebrew Python 3.12 with `python-tk@3.12`.
- **Window Resize**: Resize handling is debounced (100ms delay) to prevent performance issues during window resizing.
