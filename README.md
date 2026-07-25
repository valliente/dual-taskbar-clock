# Dual-Timezone Taskbar Clock

A sleek, glassmorphic desktop application for Windows that displays dual timezones right over your taskbar. Built with Python, PySide6, and Win32 APIs.

## Features
- **Sleek Glassmorphism**: Frameless, semi-transparent window with a modern look.
- **Dual Timezones**: See your local time and a secondary timezone side-by-side with relative offset badges.
- **Highly Customizable**: Right-click to customize colors, fonts, timezones, and time format.
- **Preset Themes**: Includes "Glass Dark", "OLED Black", "Cyberpunk Neon", and "Minimal Frost" themes.
- **Auto-Startup**: Run at Windows startup via the Settings menu.
- **Drag-and-Drop**: Smooth click and drag to reposition anywhere on the screen.

## Installation

Download the `DualTaskbarClock.exe` from the GitHub Releases page and run it. 
No installation required!

## Building from source

1. Clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the compiler:
   ```bash
   pyinstaller --noconsole --onefile --name="DualTaskbarClock" main.py
   ```
4. The executable will be in the `dist/` folder.
