# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## PhotoViewer - Image Slideshow Application

A Python-based image slideshow application that recursively searches directories for images and displays them in a Tkinter GUI.

**Tech Stack**:
- Python 3
- Tkinter (GUI)
- Pillow/PIL (image processing)

**Key Features**:
- Recursive directory search for images
- Auto-play with configurable delay
- Manual navigation (arrow keys)
- Fullscreen mode toggle
- Supports: .jpg, .jpeg, .png, .gif, .bmp, .webp, .tiff, .tif

## Running the Application

```bash
# Run with default settings (current directory, 3 second delay)
python3 slideshow.py

# Run with specific directory
python3 slideshow.py /path/to/photos

# Run in fullscreen with 5 second delay
python3 slideshow.py /path/to/photos --fullscreen --delay 5

# Manual mode (no auto-advance)
python3 slideshow.py --delay 0
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
3. Uses Tkinter Canvas for image display with aspect-ratio-preserving thumbnail resizing
4. Implements auto-advance timer with `root.after()` scheduling
5. Handles window resize events to redisplay current image at new size
