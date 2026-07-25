import sys
import json
import os
from datetime import datetime
try:
    from zoneinfo import ZoneInfo, available_timezones
except ImportError:
    from backports.zoneinfo import ZoneInfo, available_timezones
import winreg as reg

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QColor, QFont, QPainter, QBrush, QPen, QAction, QCursor, QFontDatabase
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QMenu, QDialog, QFormLayout, QComboBox, QPushButton,
                               QColorDialog, QFontDialog, QCheckBox, QHBoxLayout,
                               QFrame)

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "clock_settings.json")
APP_NAME = "DualTaskbarClock"
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"

THEMES = {
    "Glass Dark": {"bg": "rgba(15, 23, 42, 217)", "primary": "#FFFFFF", "secondary": "#60A5FA"},
    "OLED Black": {"bg": "rgba(0, 0, 0, 255)", "primary": "#FFFFFF", "secondary": "#A3A3A3"},
    "Cyberpunk Neon": {"bg": "rgba(20, 5, 30, 200)", "primary": "#FDE047", "secondary": "#F472B6"},
    "Minimal Frost": {"bg": "rgba(255, 255, 255, 200)", "primary": "#1F2937", "secondary": "#4B5563"}
}

def get_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        "primary_tz": "Local",
        "secondary_tz": "UTC",
        "use_12h": True,
        "primary_color": "#FFFFFF",
        "secondary_color": "#60A5FA",
        "bg_color": "rgba(15, 23, 42, 217)",
        "font_family": "Segoe UI Variable Display" if "Segoe UI Variable Display" in QFontDatabase.families() else "Arial",
        "font_size": 28,
        "run_on_startup": False
    }

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)
    
    # Manage Startup
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, REG_PATH, 0, reg.KEY_ALL_ACCESS)
        if settings.get("run_on_startup", False):
            reg.SetValueEx(key, APP_NAME, 0, reg.REG_SZ, os.path.abspath(sys.argv[0]))
        else:
            try:
                reg.DeleteValue(key, APP_NAME)
            except:
                pass
        reg.CloseKey(key)
    except Exception as e:
        print("Registry error:", e)

class SettingsDialog(QDialog):
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Customize Clock")
        self.settings = current_settings.copy()
        
        layout = QFormLayout(self)
        
        # Timezones
        self.tz1_cb = QComboBox()
        self.tz1_cb.addItem("Local")
        self.tz2_cb = QComboBox()
        self.tz2_cb.addItem("Local")
        
        tzs = sorted(list(available_timezones()))
        self.tz1_cb.addItems(tzs)
        self.tz2_cb.addItems(tzs)
        
        self.tz1_cb.setCurrentText(self.settings["primary_tz"])
        self.tz2_cb.setCurrentText(self.settings["secondary_tz"])
        
        layout.addRow("Primary Timezone:", self.tz1_cb)
        layout.addRow("Secondary Timezone:", self.tz2_cb)
        
        # 12h/24h Toggle
        self.format_cb = QCheckBox("Use 12-Hour Format")
        self.format_cb.setChecked(self.settings["use_12h"])
        layout.addRow("Time Format:", self.format_cb)
        
        # Font
        self.font_btn = QPushButton("Select Font")
        self.font_btn.clicked.connect(self.choose_font)
        layout.addRow("Font:", self.font_btn)
        
        # Colors
        self.c1_btn = QPushButton("Primary Color")
        self.c1_btn.clicked.connect(lambda: self.choose_color("primary_color", self.c1_btn))
        layout.addRow("Primary Color:", self.c1_btn)
        
        self.c2_btn = QPushButton("Secondary Color")
        self.c2_btn.clicked.connect(lambda: self.choose_color("secondary_color", self.c2_btn))
        layout.addRow("Secondary Color:", self.c2_btn)
        
        self.bg_btn = QPushButton("Background Color")
        self.bg_btn.clicked.connect(lambda: self.choose_color("bg_color", self.bg_btn))
        layout.addRow("Background Color:", self.bg_btn)
        
        # Themes
        self.theme_cb = QComboBox()
        self.theme_cb.addItems(["Custom"] + list(THEMES.keys()))
        self.theme_cb.currentTextChanged.connect(self.apply_theme)
        layout.addRow("Preset Themes:", self.theme_cb)
        
        # Startup
        self.startup_cb = QCheckBox("Run at Windows Startup")
        self.startup_cb.setChecked(self.settings["run_on_startup"])
        layout.addRow("Startup:", self.startup_cb)
        
        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        
        self.update_btn_styles()

    def update_btn_styles(self):
        self.c1_btn.setStyleSheet(f"background-color: {self.settings['primary_color']};")
        self.c2_btn.setStyleSheet(f"background-color: {self.settings['secondary_color']};")
        
        # Handle rgba for stylesheet properly or just let it be text
        bg = self.settings['bg_color']
        if bg.startswith("rgba"):
            self.bg_btn.setStyleSheet(f"background-color: {bg}; color: white;")
        else:
            self.bg_btn.setStyleSheet(f"background-color: {bg};")
            
    def apply_theme(self, theme_name):
        if theme_name in THEMES:
            t = THEMES[theme_name]
            self.settings["primary_color"] = t["primary"]
            self.settings["secondary_color"] = t["secondary"]
            self.settings["bg_color"] = t["bg"]
            self.update_btn_styles()

    def choose_font(self):
        current_font = QFont(self.settings["font_family"], self.settings["font_size"])
        ok, font = QFontDialog.getFont(current_font, self)
        if ok:
            self.settings["font_family"] = font.family()
            self.settings["font_size"] = font.pointSize()

    def choose_color(self, key, btn):
        # We need to handle rgba string to QColor if needed, but for simplicity we will just let QColorDialog handle standard format
        # If it's rgba, parse it
        col_str = self.settings[key]
        if col_str.startswith("rgba"):
            parts = col_str[5:-1].split(',')
            initial = QColor(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
        else:
            initial = QColor(col_str)
            
        color = QColorDialog.getColor(initial, self, "Select Color", QColorDialog.ShowAlphaChannel)
        if color.isValid():
            if color.alpha() < 255:
                self.settings[key] = f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})"
            else:
                self.settings[key] = color.name()
            self.update_btn_styles()

    def get_result(self):
        self.settings["primary_tz"] = self.tz1_cb.currentText()
        self.settings["secondary_tz"] = self.tz2_cb.currentText()
        self.settings["use_12h"] = self.format_cb.isChecked()
        self.settings["run_on_startup"] = self.startup_cb.isChecked()
        return self.settings

class ClockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = get_settings()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 15, 20, 15)
        self.layout.setSpacing(5)
        
        self.primary_label = QLabel()
        self.secondary_label = QLabel()
        
        self.layout.addWidget(self.primary_label)
        self.layout.addWidget(self.secondary_label)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        self.apply_settings()
        self.update_time()
        
        # Position at bottom right (just a default guess, ideally would get screen geometry)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 350, screen.height() - 200)

        self.oldPos = self.pos()

    def apply_settings(self):
        font_prim = QFont(self.settings["font_family"], self.settings["font_size"], QFont.Bold)
        font_sec = QFont(self.settings["font_family"], max(10, self.settings["font_size"] - 8))
        
        self.primary_label.setFont(font_prim)
        self.primary_label.setStyleSheet(f"color: {self.settings['primary_color']};")
        
        self.secondary_label.setFont(font_sec)
        self.secondary_label.setStyleSheet(f"color: {self.settings['secondary_color']};")
        
        self.update() # triggers paintEvent for background

    def get_time_string(self, tz_name):
        dt = datetime.now()
        if tz_name != "Local":
            try:
                dt = datetime.now(ZoneInfo(tz_name))
            except:
                pass
        fmt = "%I:%M:%S %p" if self.settings["use_12h"] else "%H:%M:%S"
        return dt.strftime(fmt)
        
    def get_offset_string(self, tz_name):
        if tz_name == "Local":
            return ""
        try:
            local_dt = datetime.now().astimezone()
            target_dt = datetime.now(ZoneInfo(tz_name))
            
            local_offset = local_dt.utcoffset().total_seconds()
            target_offset = target_dt.utcoffset().total_seconds()
            
            diff_hours = (target_offset - local_offset) / 3600
            
            if diff_hours == 0:
                return " (Same time)"
            elif diff_hours > 0:
                return f" (+{diff_hours:g}h)"
            else:
                return f" ({diff_hours:g}h)"
        except:
            return ""

    def update_time(self):
        p_tz = self.settings["primary_tz"]
        s_tz = self.settings["secondary_tz"]
        
        self.primary_label.setText(f"{self.get_time_string(p_tz)}")
        
        s_str = self.get_time_string(s_tz)
        offset_str = self.get_offset_string(s_tz)
        
        self.secondary_label.setText(f"{s_tz}: {s_str}{offset_str}")
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        bg_color_str = self.settings["bg_color"]
        if bg_color_str.startswith("rgba"):
            parts = bg_color_str[5:-1].split(',')
            color = QColor(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
        else:
            color = QColor(bg_color_str)
            
        painter.setBrush(QBrush(color))
        
        # Border
        pen = QPen(QColor(255, 255, 255, 30))
        pen.setWidth(1)
        painter.setPen(pen)
        
        rect = self.rect()
        rect.setWidth(rect.width() - 1)
        rect.setHeight(rect.height() - 1)
        painter.drawRoundedRect(rect, 8, 8)

    # Drag functionality
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    # Context Menu
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet('''
            QMenu {
                background-color: #1E293B;
                color: white;
                border: 1px solid #334155;
                border-radius: 4px;
            }
            QMenu::item {
                padding: 6px 24px;
            }
            QMenu::item:selected {
                background-color: #3B82F6;
            }
        ''')
        
        customize_action = QAction("Customize Clock...", self)
        customize_action.triggered.connect(self.show_settings)
        menu.addAction(customize_action)
        
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)
        
        menu.exec_(event.globalPos())

    def show_settings(self):
        dlg = SettingsDialog(self.settings, self)
        if dlg.exec_():
            self.settings = dlg.get_result()
            save_settings(self.settings)
            self.apply_settings()
            self.update_time()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    clock = ClockWidget()
    clock.show()
    
    sys.exit(app.exec())
