# Folder Slide Show

A lightweight Python-based image slideshow application that recursively searches directories for images and displays them in a clean, full-featured viewer.

## Features

- **Recursive Directory Search** - Automatically finds all images in nested folder structures
- **Auto-Play Mode** - Images advance automatically with configurable delay
- **Dynamic Delay Control** - Change auto-play delay on the fly with number keys (0-9 seconds)
- **Manual Navigation** - Browse images with arrow keys
- **Fullscreen Support** - Toggle fullscreen mode on/off
- **Resume Functionality** - Remembers your position in each directory and resume where you left off
- **Folder Ignore Filtering** - Exclude images from specific subfolders (e.g., PREVIEW, THUMBNAIL)
- **Aspect Ratio Preservation** - Images are scaled to fit the window while maintaining proportions
- **Multiple Format Support** - Works with `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.tiff`, `.tif`
- **Progress Tracking** - Status bar shows current image position, delay, and file path

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

# Resume from last viewed image
./slideshow.py /path/to/photos --continue

# Disable folder filtering (show all images)
./slideshow.py /path/to/photos --no-ignore
```

### Command Line Options

```
usage: slideshow.py [-h] [-f] [-d DELAY] [-c] [--no-ignore] [directory]

positional arguments:
  directory             Root directory to search for images (default: current directory)

optional arguments:
  -h, --help            Show help message
  -f, --fullscreen      Start in fullscreen mode
  -d DELAY, --delay DELAY
                        Delay between images in seconds (0 = manual only, default: 3)
  -c, --continue        Resume from last viewed image in this directory
  --no-ignore           Disable folder ignore filtering (show all images)
```

## Resume Functionality

The application automatically remembers your position in each directory you view. When you exit and restart with the `--continue` flag, it will resume from where you left off.

**How it works:**
- Position data is saved to `slideshow_state.json` in the script directory
- Each directory's state is tracked independently
- Uses both the image path and index for robust resume (handles file changes)
- If the saved image is in an ignored folder or the image count has changed, it will start from the beginning with an informative message

**Example:**
```bash
# View photos normally
./slideshow.py /Volumes/Photos/Vacation

# Later, resume from where you left off
./slideshow.py /Volumes/Photos/Vacation --continue
```

## Folder Ignore Filtering

Exclude images from specific subfolders (e.g., thumbnails, previews) using an `ignore.json` configuration file.

**Configuration:**
- File location: `ignore.json` in the script directory
- Auto-created with defaults `["PREVIEW", "THUMBNAIL"]` on first run
- Matching is case-sensitive and exact (e.g., "PREVIEW" matches only "PREVIEW", not "preview")

**Example ignore.json:**
```json
{
  "ignore_folders": [
    "PREVIEW",
    "THUMBNAIL",
    "HTML"
  ]
}
```

**Behavior:**
- Any image with a matching folder name in its path is excluded
- Examples (with `"PREVIEW"` in ignore list):
  - ✅ Include: `/photos/2024/vacation/beach.jpg`
  - ❌ Exclude: `/photos/2024/PREVIEW/beach.jpg`
  - ❌ Exclude: `/photos/PREVIEW/2024/beach.jpg`
  - ✅ Include: `/photos/2024/preview/beach.jpg` (case-sensitive)

**Bypass filtering:**
```bash
# Temporarily show all images including ignored folders
./slideshow.py /path/to/photos --no-ignore
```

## Controls

| Key | Action |
|-----|--------|
| `Right Arrow` | Next image |
| `Left Arrow` | Previous image |
| `Space` | Toggle auto-play on/off |
| `0-9` | Set auto-play delay (0=manual, 1-9=seconds) |
| `F` | Toggle fullscreen mode |
| `Q` or `Escape` | Quit application |

## How It Works

The application:
1. Loads ignore list from `ignore.json` (auto-creates with defaults if missing)
2. Recursively scans the specified directory for image files
3. Filters out images in ignored folders (unless `--no-ignore` is used)
4. Sorts images by path for consistent ordering
5. Resumes from saved position if `--continue` flag is used
6. Displays images in a Tkinter window with aspect-ratio-preserving scaling
7. Automatically advances to the next image (if auto-play is enabled)
8. Handles window resizing dynamically
9. Saves current position on exit for resume functionality

## License

This project is open source and available for use.

## Acknowledgments

Built with Python, Tkinter, and Pillow (PIL).
