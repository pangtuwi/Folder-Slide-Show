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
- Dynamic delay control (change delay on the fly with number keys 0-9)
- Image rotation (rotate clockwise/counter-clockwise with ,/. keys)
- Manual navigation (arrow keys)
- Fullscreen mode toggle
- Resume from last viewed image (--continue)
- Start at specific image index (--start-index)
- Folder filtering with ignore.json
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

# Resume from last viewed image
./slideshow.py /path/to/photos --continue

# Start at specific image index (0-based)
./slideshow.py /path/to/photos --start-index 42

# Disable folder filtering
./slideshow.py /path/to/photos --no-ignore
```

Or explicitly use Homebrew Python:

```bash
/opt/homebrew/bin/python3.12 slideshow.py /path/to/photos
```

## Application Controls

- Right Arrow: Next image
- Left Arrow: Previous image
- Space: Toggle auto-play
- 0-9: Set auto-play delay (0=manual mode, 1-9=seconds)
- , (comma): Rotate image counter-clockwise (90°)
- . (period): Rotate image clockwise (90°)
- F: Toggle fullscreen
- Q: Quit without saving position
- Escape: Quit and save position (for use with --continue)

## Resume Functionality

The application can save your position when you quit (press Escape) and resume from where you left off.

**State File**: `slideshow_state.json` (in project directory)

**How it works**:
- Tracks last viewed image for each directory separately
- Saves both image path (relative) and index for robustness
- Uses path-based resume (most reliable)
- Falls back to index-based resume if path not found and image count unchanged
- Starts from beginning if filtering changes image count

**Usage**: Run with `--continue` flag to resume from last position

**Resume Strategy**:
1. Try to find saved image by path (works even if filtering changed)
2. Use saved index only if total image count matches
3. Default to beginning with informative message if count changed

## Start Index Option

Start the slideshow at a specific image using the `--start-index` option.

**Usage**: `./slideshow.py /path/to/photos --start-index 42`

**How it works**:
- Index is 0-based (first image = 0, second = 1, etc.)
- Overrides `--continue` if both are specified
- Validates index is within valid range (0 to total_images-1)
- Falls back to beginning with warning if index is invalid

**Examples**:
```bash
# Start at the 43rd image (index 42)
./slideshow.py /path/to/photos --start-index 42

# Start at 10th image with 5 second delay
./slideshow.py /path/to/photos -s 10 --delay 5
```

## Folder Ignore Functionality

Exclude images in specific subfolders from the slideshow using an ignore list.

**Ignore File**: `ignore.json` (in project directory)

**Structure**:
```json
{
  "ignore_folders": [
    "PREVIEW",
    "THUMBNAIL"
  ]
}
```

**Behavior**:
- Auto-created with defaults on first run if missing
- Case-sensitive exact folder name matching
- Excludes images if ANY parent folder matches ignore list
- Fails open (allows all images) on errors

**Examples**:
- If ignore list contains `["PREVIEW"]`:
  - ✅ Include: `/photos/2024/vacation/beach.jpg`
  - ❌ Exclude: `/photos/2024/PREVIEW/beach.jpg`
  - ❌ Exclude: `/photos/PREVIEW/2024/beach.jpg`
  - ✅ Include: `/photos/2024/preview/beach.jpg` (case-sensitive)

**Usage**:
- Filtering enabled by default
- Use `--no-ignore` flag to bypass filtering temporarily
- Edit `ignore.json` to customize folder list

**Integration with Resume**:
- Resume checks if saved image is in ignored folder
- Provides clear message when saved image is filtered
- Only uses index fallback if image count unchanged
- Prevents resuming at wrong image when filtering changes

## Architecture

Single-file application with `ImageSlideshow` class that:
1. Recursively finds images using `Path.rglob()` with optional folder filtering
2. Filters images based on ignore.json configuration
3. Maintains image list sorted by path
4. Uses Tkinter Label for image display with aspect-ratio-preserving thumbnail resizing
5. Implements auto-advance timer with `root.after()` scheduling
6. Handles window resize events with debouncing to redisplay current image at new size
7. Uses PhotoImage to convert PIL images for Tkinter display
8. Saves/restores slideshow position via JSON state file

**Module-level Functions**:
- State management: `load_state()`, `save_state()`, `get_state_file_path()`, `normalize_directory_path()`
- Folder filtering: `load_ignore_list()`, `get_ignore_file_path()`, `should_ignore_path()`

## Known Issues

- **macOS System Python**: The built-in Python on macOS has a broken Tkinter that doesn't render widgets properly. Always use Homebrew Python 3.12 with `python-tk@3.12`.
- **Window Resize**: Resize handling is debounced (100ms delay) to prevent performance issues during window resizing.
