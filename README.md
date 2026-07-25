# Dual-Timezone Taskbar Clock

A sleek, glassmorphic desktop application for Windows that displays dual timezones right over your taskbar. Built with Python, PySide6, and Win32 APIs.

## Features
- **Sleek Glassmorphism**: Frameless, semi-transparent window with a modern look.
- **Dual Timezones**: See your local time and a secondary timezone side-by-side with relative offset badges.
- **Highly Customizable**: Right-click to customize colors, fonts, timezones, and time format.
- **Preset Themes**: Includes "Glass Dark", "OLED Black", "Cyberpunk Neon", and "Minimal Frost" themes.
- **Auto-Startup**: Run at Windows startup via the Settings menu.
- **Drag-and-Drop & Resizable**: Smooth click and drag to reposition anywhere on the screen, and resize via the bottom right grip.
- **Opacity Control**: Adjust the transparency of the glassmorphism UI.
- **Always on Top Toggle**: Pin or unpin the clock above all other windows.
- **Date & Compact Mode**: Toggle the current date and secondary timezone on or off.

## Installation

1. Download the `DualTaskbarClock_v0.1.3.zip` from the GitHub Releases page.
2. Extract the folder to a safe location on your computer (e.g., `C:\Program Files\DualTaskbarClock`).
3. Run `DualTaskbarClock.exe` inside the extracted folder.
No complex installation required, and this directory-based format prevents false-positive virus detections!

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
