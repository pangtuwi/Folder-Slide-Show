#!/opt/homebrew/bin/python3.12
"""
Image Slideshow from Complex Directory Structure
Recursively finds and displays images from nested folders
"""

import os
import sys
from pathlib import Path
from tkinter import Tk, Label, Canvas
from PIL import Image, ImageTk
import argparse


class ImageSlideshow:
    def __init__(self, root_dir, fullscreen=False, delay=3000):
        """
        Initialize the slideshow
        
        Args:
            root_dir: Root directory to search for images
            fullscreen: Whether to start in fullscreen mode
            delay: Auto-advance delay in milliseconds (0 = manual only)
        """
        self.root_dir = Path(root_dir)
        self.fullscreen = fullscreen
        self.delay = delay
        self.current_index = 0
        self.auto_play = delay > 0
        self.timer_id = None
        self.resize_timer_id = None
        
        # Supported image extensions
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
        
        # Find all images
        print(f"Searching for images in {self.root_dir}...")
        self.image_paths = self.find_images()
        print(f"Found {len(self.image_paths)} images")
        
        if not self.image_paths:
            print("No images found!")
            sys.exit(1)
        
        # Setup GUI
        self.root = Tk()
        self.root.title("Image Slideshow")
        
        if self.fullscreen:
            self.root.attributes('-fullscreen', True)
        else:
            self.root.geometry("1024x768")
        
        self.root.configure(bg='black')

        # Create label for image display
        self.image_label = Label(self.root, bg='black')
        self.image_label.pack(fill='both', expand=True)

        # Create label for image info
        self.info_label = Label(
            self.root,
            text="Loading...",
            bg='darkgray',
            fg='white',
            font=('Arial', 12),
            pady=5
        )
        self.info_label.pack(side='bottom', fill='x')
        
        # Bind keyboard events
        self.root.bind('<Escape>', lambda e: self.quit())
        self.root.bind('q', lambda e: self.quit())
        self.root.bind('<Right>', lambda e: self.next_image())
        self.root.bind('<Left>', lambda e: self.previous_image())
        self.root.bind('<space>', lambda e: self.toggle_auto_play())
        self.root.bind('f', lambda e: self.toggle_fullscreen())
        self.root.bind('<Configure>', self.on_resize)
    
    def find_images(self):
        """Recursively find all image files"""
        image_paths = []
        
        for ext in self.image_extensions:
            # Use rglob for recursive search with pattern
            image_paths.extend(self.root_dir.rglob(f'*{ext}'))
            # Also search for uppercase extensions
            image_paths.extend(self.root_dir.rglob(f'*{ext.upper()}'))
        
        # Sort by path for consistent order
        image_paths.sort()
        return image_paths
    
    def display_image(self):
        """Display the current image"""
        if not self.image_paths:
            return

        # Cancel any pending timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        image_path = self.image_paths[self.current_index]

        try:
            # Load and display image
            img = Image.open(image_path)

            # Get window size
            window_width = self.image_label.winfo_width()
            window_height = self.image_label.winfo_height()

            # Handle case where window isn't fully initialized yet
            if window_width <= 1:
                window_width = 1024
            if window_height <= 1:
                window_height = 768 - 40  # Account for info label

            # Resize image to fit window while maintaining aspect ratio
            img.thumbnail((window_width, window_height), Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            self.photo = ImageTk.PhotoImage(img)

            # Display image in label
            self.image_label.config(image=self.photo)

            # Update info label
            relative_path = image_path.relative_to(self.root_dir)
            status = "▶ AUTO" if self.auto_play else "⏸ MANUAL"
            self.info_label.config(
                text=f"{status} | {self.current_index + 1}/{len(self.image_paths)} | {relative_path}"
            )

            # Force GUI update
            self.root.update_idletasks()

            # Schedule next image if auto-play is enabled
            if self.auto_play and self.delay > 0:
                self.timer_id = self.root.after(self.delay, self.next_image)
                
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            # Skip to next image
            self.next_image()
    
    def next_image(self):
        """Show next image"""
        self.current_index = (self.current_index + 1) % len(self.image_paths)
        self.display_image()
    
    def previous_image(self):
        """Show previous image"""
        self.current_index = (self.current_index - 1) % len(self.image_paths)
        self.display_image()
    
    def toggle_auto_play(self):
        """Toggle auto-play mode"""
        self.auto_play = not self.auto_play
        if self.auto_play and self.delay > 0:
            self.display_image()  # Restart timer
        else:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
            # Update info label
            relative_path = self.image_paths[self.current_index].relative_to(self.root_dir)
            self.info_label.config(
                text=f"⏸ MANUAL | {self.current_index + 1}/{len(self.image_paths)} | {relative_path}"
            )
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
    
    def on_resize(self, event):
        """Handle window resize"""
        # Only redisplay for image label resize events, and debounce
        if event.widget != self.image_label:
            return

        # Cancel pending resize timer
        if self.resize_timer_id:
            self.root.after_cancel(self.resize_timer_id)

        # Schedule redisplay after a short delay (debounce)
        if hasattr(self, 'image_paths') and self.image_paths:
            self.resize_timer_id = self.root.after(100, self.display_image)
    
    def quit(self):
        """Quit the application"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        if self.resize_timer_id:
            self.root.after_cancel(self.resize_timer_id)
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Start the slideshow"""
        print("\nControls:")
        print("  Right Arrow / Left Arrow: Next / Previous image")
        print("  Space: Toggle auto-play")
        print("  F: Toggle fullscreen")
        print("  Q or Escape: Quit")
        print("\nStarting slideshow...\n")
        # Ensure window is visible and raised
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        # Schedule first image display after mainloop starts
        self.root.after(100, self.display_image)
        self.root.mainloop()


def main():
    parser = argparse.ArgumentParser(
        description='Image slideshow from complex directory structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Controls:
  Right Arrow    Next image
  Left Arrow     Previous image
  Space          Toggle auto-play
  F              Toggle fullscreen
  Q or Escape    Quit

Examples:
  %(prog)s /path/to/photos
  %(prog)s /path/to/photos --fullscreen --delay 5
  %(prog)s . --delay 0  (manual mode, current directory)
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Root directory to search for images (default: current directory)'
    )
    
    parser.add_argument(
        '-f', '--fullscreen',
        action='store_true',
        help='Start in fullscreen mode'
    )
    
    parser.add_argument(
        '-d', '--delay',
        type=int,
        default=3,
        help='Delay between images in seconds (0 = manual only, default: 3)'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory")
        sys.exit(1)
    
    # Convert delay to milliseconds
    delay_ms = args.delay * 1000
    
    # Create and run slideshow
    slideshow = ImageSlideshow(args.directory, args.fullscreen, delay_ms)
    slideshow.run()


if __name__ == '__main__':
    main()