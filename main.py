"""
Attract-Mode Plus Layout Designer
A visual GUI tool for creating layout.nut files for Attract-Mode Plus frontend.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import customtkinter as ctk
import json
import os
import math

# ── CustomTkinter appearance ─────────────────────────────────────────────────
ctk.set_default_color_theme("blue")

# ─── Default Layout State ────────────────────────────────────────────────────

DEFAULT_LAYOUT = {
    "width": 1920,
    "height": 1080,
    "elements": [],
    "modules": [],
    "snippets": [],
    "globals": {
        "orient": "RotateNone",
        "font": "Arial",
        "font_size": 24,
    }
}

ELEMENT_TYPES = sorted(["snap", "wheel", "boxart", "marquee", "flyer", "fanart",
                 "video", "text", "artwork", "shader_layer", "surface"])

MODULE_LIST = [
    ("animate",          "animate.nut",          "Property animation system (fade, move, scale, spin)"),
    ("blur",             "blur.nut",              "Used for background glass effects"),
    ("config",           "config.nut",            "User-configurable layout settings via AM+ config menu"),
    ("conveyor",         "conveyor.nut",          "Scrolling artwork conveyor belt display"),
    ("conveyor_helper",  "conveyor_helper.nut",   "Helper utilities for conveyor belt layouts"),
    ("fade",             "fade.nut",              "Screen transition fade effects between selections"),
    ("file",             "file.nut",              "File I/O: read and write files from layouts"),
    ("file_format",      "file_format.nut",       "Parse and format structured file data (CSV, etc.)"),
    ("file_layout",      "file_layout.nut",       "Load and manage multiple layout files dynamically"),
    ("flow",             "flow.nut",              "Adds animation keyframes to Inertia"),
    ("gtc",              "gtc.nut",               "Game & system tag/category filtering helpers"),
    ("gtc_kb",           "gtc_kb.nut",            "Keyboard input support for gtc module"),
    ("inertia",          "inertia.nut",           "Inertia/momentum-based smooth scrolling movement"),
    ("mask",             "mask.nut",              "Alpha mask and clipping region support"),
    ("math",             "math.nut",              "Extended math utilities (lerp, clamp, easing, etc.)"),
    ("objects",          "objects.nut",           "Used to simplify creating common UI elements"),
    ("perspective",      "perspective.nut",       "Used for 3d/skewed cabinet art effects"),
    ("pan_and_scan",     "pan_and_scan.nut",      "Pan and scan artwork zooming/panning effect"),
    ("surface",          "surface.nut",           "Helper module for managing complex layers"),
    ("wheel",            "wheel.nut",             "Wheel artwork list navigation and display"),
]

ORIENT_OPTIONS = ["RotateNone", "RotateLeft", "RotateRight", "RotateFlip"]
BLEND_OPTIONS = ["None", "Alpha", "Premult", "Add", "Screen", "Multiply"]
TRIGGER_OPTIONS = ["ToNewSelection", "FromOldSelection", "EndNavigation",
                   "StartLayout", "EndLayout", "ScreenSaver"]

# AM+ fe.add_text() magic tokens — shown in the meta picker dropdown
META_TOKENS = [
    # ── Game info ──────────────────────────────────────────────────────────
    "[Title]",
    "[TitleFull]",
    "[Year]",
    "[Manufacturer]",
    "[Category]",
    "[Players]",
    "[PlayedCount]",
    "[PlayedTime]",
    "[Rating]",
    "[Series]",
    "[Language]",
    "[Region]",
    "[AltTitle]",
    "[CloneOf]",
    "[Control]",
    "[DisplayCount]",
    "[DisplayType]",
    "[Rotation]",
    "[Status]",
    "[EmulatorName]",
    "[SystemName]",
    "[RomName]",
    # ── List / navigation ──────────────────────────────────────────────────
    "[ListSize]",
    "[ListEntry]",
    "[FilterName]",
    # ── Clock / time ──────────────────────────────────────────────────────
    "[!%H:%M]",
    "[!%H:%M:%S]",
    "[!%d/%m/%Y]",
    "[!%A, %d %B %Y]",
    # ── System ────────────────────────────────────────────────────────────
    "[ScreenWidth]",
    "[ScreenHeight]",
    # ── Custom literal ────────────────────────────────────────────────────
    "-- custom --",
]


# ─── Colour themes ────────────────────────────────────────────────────────────

THEMES = {
    "Arctic Light": {
        "bg": "#eef2f7", "panel": "#dde4ef", "panel2": "#cdd6e8",
        "accent": "#0066cc", "accent2": "#cc4400", "text": "#1a2a3a",
        "text_dim": "#6688aa", "border": "#aabbcc", "canvas_bg": "#e0e8f4",
        "selected": "#c0d8f0", "elem_fill": "#d0e4f8",
        "elem_border": "#0066cc", "elem_sel": "#cc4400",
        "_ctk_mode": "light",
    },
    "Slate Pro": {
        "bg": "#1a1d23", "panel": "#21252d", "panel2": "#292d38",
        "accent": "#5eaeff", "accent2": "#f0a050", "text": "#d8dce8",
        "text_dim": "#6878a0", "border": "#363c4a", "canvas_bg": "#12141a",
        "selected": "#1e2d45", "elem_fill": "#1a2535",
        "elem_border": "#5eaeff", "elem_sel": "#f0a050",
        "_ctk_mode": "dark",
    },
    "Cyan Night": {
        "bg": "#0d0d1a", "panel": "#13132b", "panel2": "#1a1a35",
        "accent": "#00e5ff", "accent2": "#ff6b35", "text": "#e8e8ff",
        "text_dim": "#7777aa", "border": "#2a2a5a", "canvas_bg": "#080810",
        "selected": "#0a2a35", "elem_fill": "#0d2030",
        "elem_border": "#00e5ff", "elem_sel": "#ff6b35",
        "_ctk_mode": "dark",
    },
    "Amber Dark": {
        "bg": "#0f0e09", "panel": "#1a180e", "panel2": "#242010",
        "accent": "#ffb300", "accent2": "#ff5722", "text": "#fff8e1",
        "text_dim": "#a08060", "border": "#3a3010", "canvas_bg": "#080700",
        "selected": "#2a2000", "elem_fill": "#1a1500",
        "elem_border": "#ffb300", "elem_sel": "#ff5722",
        "_ctk_mode": "dark",
    },
    "Green Matrix": {
        "bg": "#050f05", "panel": "#0a1a0a", "panel2": "#0f220f",
        "accent": "#00ff41", "accent2": "#ffff00", "text": "#ccffcc",
        "text_dim": "#447744", "border": "#1a3a1a", "canvas_bg": "#020802",
        "selected": "#0a200a", "elem_fill": "#081508",
        "elem_border": "#00ff41", "elem_sel": "#ffff00",
        "_ctk_mode": "dark",
    },
    "Purple Haze": {
        "bg": "#0e0814", "panel": "#170d20", "panel2": "#20122c",
        "accent": "#cc66ff", "accent2": "#ff66aa", "text": "#f0e6ff",
        "text_dim": "#8855aa", "border": "#3a1a5a", "canvas_bg": "#080510",
        "selected": "#200a35", "elem_fill": "#180820",
        "elem_border": "#cc66ff", "elem_sel": "#ff66aa",
        "_ctk_mode": "dark",
    },
    "Red Alert": {
        "bg": "#110505", "panel": "#1c0a0a", "panel2": "#260e0e",
        "accent": "#ff3333", "accent2": "#ff9900", "text": "#ffe8e8",
        "text_dim": "#aa5555", "border": "#4a1010", "canvas_bg": "#080202",
        "selected": "#2a0808", "elem_fill": "#1a0505",
        "elem_border": "#ff3333", "elem_sel": "#ff9900",
        "_ctk_mode": "dark",
    },
    "Warm Mocha": {
        "bg": "#151210", "panel": "#1e1a16", "panel2": "#28221c",
        "accent": "#d4915a", "accent2": "#a8c060", "text": "#ede0d0",
        "text_dim": "#8a7060", "border": "#3a2e24", "canvas_bg": "#0e0c0a",
        "selected": "#2a1e14", "elem_fill": "#1e1610",
        "elem_border": "#d4915a", "elem_sel": "#a8c060",
        "_ctk_mode": "dark",
    },
}

# Active theme name — starts on Arctic Light
_ACTIVE_THEME = "Arctic Light"

# Start CTK in the correct mode for the default theme
ctk.set_appearance_mode(THEMES[_ACTIVE_THEME]["_ctk_mode"])

# Global colours dict — always reflects the active theme
COLORS = {k: v for k, v in THEMES[_ACTIVE_THEME].items() if not k.startswith("_")}


def _sync_colors(theme_name=None):
    """Update COLORS from the named theme (or keep current if None)."""
    global _ACTIVE_THEME
    if theme_name:
        _ACTIVE_THEME = theme_name
    t = THEMES[_ACTIVE_THEME]
    COLORS.update({k: v for k, v in t.items() if not k.startswith("_")})
    ctk.set_appearance_mode(t["_ctk_mode"])


# ─── Layout Element ───────────────────────────────────────────────────────────

class LayoutElement:
    def __init__(self, etype="snap", name=None):
        self.type = etype
        self.name = name or f"{etype}_{id(self) % 10000}"
        self.x = 100
        self.y = 100
        self.width = 300
        self.height = 200
        self.rotation = 0
        self.alpha = 255
        self.blend_mode = "Alpha"
        self.visible = True
        self.zorder = 0
        self.trigger = "ToNewSelection"
        self.anim_enabled = False
        self.anim_type = "fade"
        self.anim_duration = 300
        self.extra = {}
        # type-specific
        if etype == "text":
            self.text_string = "[Title]"
            self.font = "Arial"
            self.font_size = 24
            self.font_color = "#ffffff"
            self.align = "Left"
        if etype in ("snap", "video"):
            self.preserve_aspect_ratio = True
            self.no_audio = False
            # Advanced transforms
            self.pinch   = 0.0
            self.skew_x  = 0.0
            self.skew_y  = 0.0
            # RGB tint (255 = no tint on that channel)
            self.red     = 255
            self.green   = 255
            self.blue    = 255
        if etype == "wheel":
            self.width = 200
            self.height = 200
            self.preserve_aspect_ratio = True

    def to_nut(self, indent=0, lw=1920, lh=1080):
        pad = " " * indent
        lines = []
        vname = self.name.replace(" ", "_").replace("-", "_")

        # Convert pixel values to dynamic flw/flh expressions
        ex = _px_to_expr(self.x,     lw, "flw")
        ey = _px_to_expr(self.y,     lh, "flh")
        ew = _px_to_expr(self.width,  lw, "flw")
        eh = _px_to_expr(self.height, lh, "flh")

        if self.type == "text":
            lines.append(f'{pad}local {vname} = fe.add_text("{self.text_string}", {ex}, {ey}, {ew}, {eh});')
            lines.append(f'{pad}{vname}.font = "{getattr(self, "font", "Arial")}";')
            lines.append(f'{pad}{vname}.char_size = {getattr(self, "font_size", 24)};')
            color = getattr(self, "font_color", "#ffffff").lstrip("#")
            r, g, b = int(color[0:2],16), int(color[2:4],16), int(color[4:6],16)
            lines.append(f'{pad}{vname}.set_rgb({r}, {g}, {b});')
            lines.append(f'{pad}{vname}.align = Align.{getattr(self, "align", "Left")};')
        elif self.type == "clock":
            lines.append(f'{pad}local {vname} = fe.add_text("[!%H:%M]", {ex}, {ey}, {ew}, {eh});')
        elif self.type == "surface":
            lines.append(f'{pad}local {vname} = fe.add_surface({ew}, {eh});')
            lines.append(f'{pad}{vname}.x = {ex};')
            lines.append(f'{pad}{vname}.y = {ey};')
        else:
            art_map = {
                "snap": "snap", "wheel": "wheel", "boxart": "boxart",
                "marquee": "marquee", "flyer": "flyer", "fanart": "fanart",
                "video": "snap", "artwork": "artwork",
            }
            art_name = art_map.get(self.type, self.type)
            lines.append(f'{pad}local {vname} = fe.add_artwork("{art_name}", {ex}, {ey}, {ew}, {eh});')
            if getattr(self, "preserve_aspect_ratio", False):
                lines.append(f'{pad}{vname}.preserve_aspect_ratio = true;')
            if getattr(self, "no_audio", False):
                lines.append(f'{pad}{vname}.video_flags = Vid.NoAudio;')
            # Advanced transforms (only emit if non-default)
            if getattr(self, "pinch",  0.0) != 0.0:
                lines.append(f'{pad}{vname}.pinch = {round(self.pinch, 4)};')
            if getattr(self, "skew_x", 0.0) != 0.0:
                lines.append(f'{pad}{vname}.skew_x = {round(self.skew_x, 4)};')
            if getattr(self, "skew_y", 0.0) != 0.0:
                lines.append(f'{pad}{vname}.skew_y = {round(self.skew_y, 4)};')
            # RGB tint (only emit if not pure white 255,255,255)
            r = getattr(self, "red",   255)
            g = getattr(self, "green", 255)
            b = getattr(self, "blue",  255)
            if (r, g, b) != (255, 255, 255):
                lines.append(f'{pad}{vname}.red = {r};')
                lines.append(f'{pad}{vname}.green = {g};')
                lines.append(f'{pad}{vname}.blue = {b};')

        if self.rotation != 0:
            lines.append(f'{pad}{vname}.rotation = {self.rotation};')
        if self.alpha != 255:
            lines.append(f'{pad}{vname}.alpha = {self.alpha};')
        if self.blend_mode != "None":
            lines.append(f'{pad}{vname}.blend_mode = BlendMode.{self.blend_mode};')
        if not self.visible:
            lines.append(f'{pad}{vname}.visible = false;')
        if self.zorder != 0:
            lines.append(f'{pad}{vname}.zorder = {self.zorder};')

        if self.anim_enabled:
            lines.append(f'{pad}animation.add( PropertyAnimation( {vname}, {{')
            lines.append(f'{pad}    "when": Transition.{self.trigger},')
            lines.append(f'{pad}    "duration": {self.anim_duration},')
            lines.append(f'{pad}    "property": "alpha",')
            lines.append(f'{pad}    "start": 0,')
            lines.append(f'{pad}    "end": 255,')
            lines.append(f'{pad}    "tween": Tween.Linear')
            lines.append(f'{pad}}} ) );')

        return "\n".join(lines)

# ─── Dynamic expression helper ───────────────────────────────────────────────

def _px_to_expr(value, layout_dim, dim_var):
    """
    Convert a pixel int into a clean flw/flh expression.
      - Exact match:      flw
      - Half:             flw/2
      - Other fraction:   flw*0.375  (rounded to 3dp)
      - Near-zero:        0
    """
    if layout_dim == 0:
        return str(value)
    if value == 0:
        return "0"
    ratio = value / layout_dim
    if abs(ratio - 1.0) < 0.001:
        return dim_var
    # Check clean fractions  1/2 1/3 2/3 1/4 3/4 1/5 2/5 3/5 4/5 1/6 5/6 1/8 3/8 5/8 7/8
    for num, den in [(1,2),(1,3),(2,3),(1,4),(3,4),(1,5),(2,5),(3,5),(4,5),
                     (1,6),(5,6),(1,8),(3,8),(5,8),(7,8),(1,10),(3,10),(7,10),(9,10)]:
        if abs(ratio - num/den) < 0.002:
            if num == 1:
                return f"{dim_var}/{den}"
            else:
                return f"{dim_var}*{num}/{den}"
    # Fall back to multiplier rounded to 3 dp
    r = round(ratio, 3)
    # Remove trailing zeros
    rs = f"{r:.3f}".rstrip("0").rstrip(".")
    return f"{dim_var}*{rs}"


# ─── Canvas Preview ───────────────────────────────────────────────────────────

class LayoutCanvas(tk.Canvas):
    # ── PERFORMANCE SETTINGS ─────────────────────────────────────────────────
    # Increase DRAG_THROTTLE_MS to skip more frames during drag (smoother but
    # less responsive). 16 = ~60fps cap, 33 = ~30fps, 50 = ~20fps, 0 = unlimited
    DRAG_THROTTLE_MS = 0

    # Set GRID_SPACING to a larger number (200, 400) for fewer grid lines and
    # faster redraws. Set to 0 to disable the grid entirely.
    GRID_SPACING = 0

    # Set SHOW_GRID to False to skip drawing grid lines entirely (fastest).
    SHOW_GRID = False

    # Set SHOW_ICONS to False to skip emoji icons inside elements (faster with
    # many elements on screen).
    SHOW_ICONS = False
    # ─────────────────────────────────────────────────────────────────────────

    def __init__(self, parent, app, **kw):
        super().__init__(parent, bg=COLORS["canvas_bg"], highlightthickness=0, **kw)
        self.app = app
        self.scale = 0.4
        self.offset_x = 20
        self.offset_y = 20
        self.drag_data = {"item": None, "x": 0, "y": 0, "elem": None, "mode": None}
        self.resize_handle_size = 6
        self._drag_pending = False
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Button-3>", self.on_right_click)
        self.bind("<Configure>", lambda e: self.redraw())

    def world_to_screen(self, x, y):
        return (x * self.scale + self.offset_x, y * self.scale + self.offset_y)

    def screen_to_world(self, sx, sy):
        return ((sx - self.offset_x) / self.scale, (sy - self.offset_y) / self.scale)

    def redraw(self):
        self.delete("all")
        layout = self.app.layout
        w, h = layout["width"], layout["height"]
        sx, sy = self.world_to_screen(0, 0)
        ex, ey = self.world_to_screen(w, h)

        # Draw screen boundary
        self.create_rectangle(sx, sy, ex, ey, fill="#0a0a18", outline=COLORS["accent"], width=2)
        
        # Grid (controlled by SHOW_GRID and GRID_SPACING class vars)
        if self.SHOW_GRID and self.GRID_SPACING > 0:
            grid = self.GRID_SPACING
            for gx in range(0, w+1, grid):
                x1, y1 = self.world_to_screen(gx, 0)
                x2, y2 = self.world_to_screen(gx, h)
                self.create_line(x1, y1, x2, y2, fill="#1a1a3a", dash=(2,4))
            for gy in range(0, h+1, grid):
                x1, y1 = self.world_to_screen(0, gy)
                x2, y2 = self.world_to_screen(w, gy)
                self.create_line(x1, y1, x2, y2, fill="#1a1a3a", dash=(2,4))

        # Resolution label
        self.create_text(sx+4, sy+4, text=f"{w}×{h}", fill=COLORS["text_dim"],
                         anchor="nw", font=("Courier", 11))

        # Draw elements (sorted by zorder)
        sorted_elems = sorted(layout["elements"], key=lambda e: e.zorder)
        selected = self.app.selected_element

        for elem in sorted_elems:
            if not elem.visible:
                continue
            ex1, ey1 = self.world_to_screen(elem.x, elem.y)
            ex2, ey2 = self.world_to_screen(elem.x + elem.width, elem.y + elem.height)

            is_sel = (elem is selected)
            fill = "#331a00" if is_sel else COLORS["elem_fill"]
            border = COLORS["elem_sel"] if is_sel else COLORS["elem_border"]
            bw = 2 if is_sel else 1
            stipple = "gray25" if is_sel else "gray12"

            self.create_rectangle(ex1, ey1, ex2, ey2, fill=fill, stipple=stipple,
                                  outline=border, width=bw, tags=f"elem_{id(elem)}")
            
            # Type icon/label (controlled by SHOW_ICONS class var)
            cx = (ex1 + ex2) / 2
            cy = (ey1 + ey2) / 2
            if self.SHOW_ICONS:
                icon = {"snap": "📷", "wheel": "🎡", "boxart": "📦", "marquee": "📺",
                        "video": "▶", "text": "T", "flyer": "🗞", "fanart": "🖼",
                        "surface": "▣", "artwork": "🎨", "shader_layer": "✨"
                        }.get(elem.type, "?")
                self.create_text(cx, cy - 8, text=icon, font=("Arial", 14), fill=border)
            self.create_text(cx, cy + 8, text=elem.name, font=("Courier", 11), fill=border)

            # Resize handle (bottom-right)
            if is_sel:
                hs = self.resize_handle_size
                self.create_rectangle(ex2 - hs, ey2 - hs, ex2 + hs, ey2 + hs,
                                      fill=COLORS["accent2"], outline="white", tags=f"resize_{id(elem)}")
                # Dimension readout
                self.create_text(ex2 + 4, ey1, text=f"{elem.width}×{elem.height}",
                                 fill=COLORS["accent2"], anchor="nw", font=("Courier", 11))
                self.create_text(ex1, ey1 - 12, text=f"({elem.x}, {elem.y})",
                                 fill=COLORS["accent2"], anchor="nw", font=("Courier", 11))

    def find_element_at(self, sx, sy):
        wx, wy = self.screen_to_world(sx, sy)
        # Search topmost (highest zorder) first so clicks land on the visible element
        for elem in sorted(self.app.layout["elements"], key=lambda e: e.zorder, reverse=True):
            if not elem.visible:
                continue
            if elem.x <= wx <= elem.x + elem.width and elem.y <= wy <= elem.y + elem.height:
                return elem
        return None

    def is_on_resize_handle(self, elem, sx, sy):
        hs = self.resize_handle_size + 2
        ex2, ey2 = self.world_to_screen(elem.x + elem.width, elem.y + elem.height)
        return abs(sx - ex2) <= hs and abs(sy - ey2) <= hs

    def on_click(self, event):
        # Check resize handle on already-selected element FIRST (highest priority)
        sel = self.app.selected_element
        if sel and sel.visible and self.is_on_resize_handle(sel, event.x, event.y):
            self.drag_data = {"item": sel, "x": event.x, "y": event.y,
                              "elem": sel, "mode": "resize",
                              "orig_w": sel.width, "orig_h": sel.height}
            self.redraw()
            return

        elem = self.find_element_at(event.x, event.y)
        if elem:
            self.app.select_element(elem)
            self.drag_data = {"item": elem, "x": event.x, "y": event.y,
                              "elem": elem, "mode": "move",
                              "orig_x": elem.x, "orig_y": elem.y}
        else:
            self.app.select_element(None)
            self.drag_data = {"item": None}
        self.redraw()

    def on_drag(self, event):
        d = self.drag_data
        if not d.get("item"):
            return
        dx = (event.x - d["x"]) / self.scale
        dy = (event.y - d["y"]) / self.scale
        elem = d["elem"]
        if d["mode"] == "move":
            elem.x = max(0, int(d["orig_x"] + dx))
            elem.y = max(0, int(d["orig_y"] + dy))
        elif d["mode"] == "resize":
            elem.width = max(10, int(d["orig_w"] + dx))
            elem.height = max(10, int(d["orig_h"] + dy))
        self.app.refresh_props()
        # Throttle canvas redraws during drag using DRAG_THROTTLE_MS
        if self.DRAG_THROTTLE_MS == 0:
            self.redraw()
        elif not self._drag_pending:
            self._drag_pending = True
            self.after(self.DRAG_THROTTLE_MS, self._throttled_redraw)

    def _throttled_redraw(self):
        self._drag_pending = False
        if self.drag_data.get("item"):
            self.redraw()

    def on_release(self, event):
        if self.drag_data.get("item"):
            # Now update code and list once drag is finished
            self.app.update_code()
            self.app.refresh_element_list()
        self.drag_data = {"item": None}

    def on_right_click(self, event):
        elem = self.find_element_at(event.x, event.y)
        if elem:
            m = tk.Menu(self, tearoff=0, bg=COLORS["panel"], fg=COLORS["text"])
            m.add_command(label=f"Delete '{elem.name}'",
                          command=lambda: self.app.delete_element(elem))
            m.add_command(label="Duplicate",
                          command=lambda: self.app.duplicate_element(elem))
            m.add_separator()
            m.add_command(label="Bring Forward", command=lambda: self.app.change_zorder(elem, 1))
            m.add_command(label="Send Backward", command=lambda: self.app.change_zorder(elem, -1))
            m.tk_popup(event.x_root, event.y_root)

# ─── Properties Panel ─────────────────────────────────────────────────────────

class PropertiesPanel(ctk.CTkFrame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, fg_color=COLORS["panel"], **kw)
        self.app = app
        self.vars = {}
        self._build_ui()

    def _sep_label(self, parent, text):
        tk.Label(parent, text=f" {text} ",
                 bg=COLORS["border"], fg=COLORS["accent"],
                 font=("Courier", 12, "bold")).pack(fill="x", padx=4, pady=(10, 3))

    def _entry(self, parent, key, label, row=None, width=10):
        f = tk.Frame(parent, bg=COLORS["panel"])
        f.pack(fill="x", padx=6, pady=2)
        tk.Label(f, text=label, bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 12), anchor="w").pack(side="top", anchor="w")
        v = tk.StringVar()
        e = ctk.CTkEntry(f, textvariable=v,
                         fg_color=COLORS["panel2"], text_color=COLORS["text"],
                         border_color=COLORS["border"],
                         font=ctk.CTkFont(family="Courier", size=12),
                         height=28)
        e.pack(side="top", fill="x", expand=True)
        v.trace_add("write", lambda *a: self._on_change(key, v.get()))
        self.vars[key] = v
        return v

    def _combo(self, parent, key, label, values):
        f = tk.Frame(parent, bg=COLORS["panel"])
        f.pack(fill="x", padx=6, pady=2)
        tk.Label(f, text=label, bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 12), anchor="w").pack(side="top", anchor="w")
        v = tk.StringVar()
        c = ctk.CTkComboBox(f, variable=v, values=values, state="readonly",
                            fg_color=COLORS["panel2"],
                            button_color=COLORS["border"],
                            dropdown_fg_color=COLORS["panel"],
                            text_color=COLORS["text"],
                            font=ctk.CTkFont(family="Courier", size=12),
                            height=28)
        c.pack(side="top", fill="x", expand=True)
        c.configure(width=1)   # let pack geometry control width
        v.trace_add("write", lambda *a: self._on_change(key, v.get()))
        self.vars[key] = v
        return v

    def _check(self, parent, key, label):
        v = tk.BooleanVar()
        cb = ctk.CTkCheckBox(parent, text=label, variable=v,
                             text_color=COLORS["text"],
                             fg_color=COLORS["accent"],
                             hover_color=COLORS["accent"],
                             font=ctk.CTkFont(family="Courier", size=12),
                             command=lambda: self._on_change(key, v.get()))
        cb.pack(anchor="w", padx=8, pady=3)
        self.vars[key] = v
        return v

    def _build_ui(self):
        ctk.CTkLabel(self, text="◈ PROPERTIES", text_color=COLORS["accent"],
                     font=ctk.CTkFont(family="Courier", size=13, weight="bold")).pack(
                         anchor="w", padx=8, pady=(10, 4))

        self.no_sel = ctk.CTkLabel(self,
                                    text="No element selected.\nClick an element\non the canvas.",
                                    text_color=COLORS["text_dim"],
                                    font=ctk.CTkFont(family="Courier", size=12),
                                    justify="center")
        self.no_sel.pack(pady=20)

        self.prop_frame = tk.Frame(self, bg=COLORS["panel"])

        self._sep_label(self.prop_frame, "POSITION & SIZE")
        self._entry(self.prop_frame, "name",     "Name")
        self._entry(self.prop_frame, "x",        "X")
        self._entry(self.prop_frame, "y",        "Y")
        self._entry(self.prop_frame, "width",    "Width")
        self._entry(self.prop_frame, "height",   "Height")
        self._entry(self.prop_frame, "rotation", "Rotation")
        self._entry(self.prop_frame, "zorder",   "Z-Order")

        self._sep_label(self.prop_frame, "SNAP / VIDEO TRANSFORMS")
        self._entry(self.prop_frame, "pinch",  "Pinch")
        self._entry(self.prop_frame, "skew_x", "Skew X")
        self._entry(self.prop_frame, "skew_y", "Skew Y")

        self._sep_label(self.prop_frame, "RGB TINT  (snap / video)")
        self._entry(self.prop_frame, "red",   "Red  (0-255)")
        self._entry(self.prop_frame, "green", "Green (0-255)")
        self._entry(self.prop_frame, "blue",  "Blue  (0-255)")

        self._sep_label(self.prop_frame, "APPEARANCE")
        self._entry(self.prop_frame, "alpha", "Alpha (0-255)")
        self._combo(self.prop_frame, "blend_mode", "Blend Mode", BLEND_OPTIONS)
        self._check(self.prop_frame, "visible", "Visible")
        self._check(self.prop_frame, "preserve_aspect_ratio", "Preserve Aspect")
        self._check(self.prop_frame, "no_audio", "No Audio (Vid.NoAudio)")

        self._sep_label(self.prop_frame, "TEXT (if text type)")

        # ── Meta token picker ─────────────────────────────────────────────
        mf = tk.Frame(self.prop_frame, bg=COLORS["panel"])
        mf.pack(fill="x", padx=6, pady=2)
        tk.Label(mf, text="Meta Token", bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 12), anchor="w").pack(side="top", anchor="w")
        self._meta_var = tk.StringVar(value="[Title]")
        self._meta_combo = ctk.CTkComboBox(
            mf, variable=self._meta_var,
            values=META_TOKENS,
            state="readonly",
            fg_color=COLORS["panel2"],
            button_color=COLORS["border"],
            dropdown_fg_color=COLORS["panel"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Courier", size=12),
            height=28,
            command=lambda v: self._on_meta_pick(v))
        self._meta_combo.pack(side="top", fill="x", expand=True)
        self._meta_combo.configure(width=1)

        # ── Custom string override (shown only when "-- custom --" picked) ──
        self._custom_frame = tk.Frame(self.prop_frame, bg=COLORS["panel"])
        cf_inner = tk.Frame(self._custom_frame, bg=COLORS["panel"])
        cf_inner.pack(fill="x", padx=6, pady=1)
        tk.Label(cf_inner, text="Custom String", bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 12), anchor="w").pack(side="top", anchor="w")
        self._custom_str_var = tk.StringVar()
        ctk.CTkEntry(cf_inner, textvariable=self._custom_str_var,
                     fg_color=COLORS["panel2"], text_color=COLORS["text"],
                     border_color=COLORS["border"],
                     font=ctk.CTkFont(family="Courier", size=12),
                     height=28).pack(side="top", fill="x", expand=True)
        self._custom_str_var.trace_add("write",
            lambda *a: self._on_change("text_string", self._custom_str_var.get()))
        self.vars["text_string"] = self._meta_var

        self._entry(self.prop_frame, "font",      "Font")
        self._entry(self.prop_frame, "font_size", "Font Size")
        self._combo(self.prop_frame, "align", "Align", ["Left", "Centre", "Right"])

        # Font color button
        fc = tk.Frame(self.prop_frame, bg=COLORS["panel"])
        fc.pack(fill="x", padx=6, pady=2)
        tk.Label(fc, text="Font Color", bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 12), anchor="w").pack(side="top", anchor="w")
        self._font_color_val = "#ffffff"
        self.color_btn = ctk.CTkButton(fc, text="  Choose Color  ", height=28,
                                        fg_color="#ffffff", text_color="#000000",
                                        hover_color=COLORS["accent"],
                                        font=ctk.CTkFont(family="Courier", size=12),
                                        command=self._pick_color)
        self.color_btn.pack(side="top", fill="x", expand=True)
        self.vars["font_color"] = "#ffffff"

        self._sep_label(self.prop_frame, "ANIMATION")
        self._check(self.prop_frame, "anim_enabled",  "Enable Animation")
        self._combo(self.prop_frame, "trigger",       "Trigger", TRIGGER_OPTIONS)
        self._entry(self.prop_frame, "anim_duration", "Duration (ms)")

    def _pick_color(self):
        elem = self.app.selected_element
        if not elem:
            return
        init = getattr(elem, "font_color", "#ffffff")
        color = colorchooser.askcolor(color=init, title="Font Color")[1]
        if color:
            elem.font_color = color
            self._font_color_val = color
            self.color_btn.configure(fg_color=color,
                                     text_color="#000000" if _is_light(color) else "#ffffff")
            self.app.update_code()
            self.app.canvas.redraw()

    def _on_meta_pick(self, value):
        if value == "-- custom --":
            self._custom_frame.pack(fill="x", after=self._meta_combo.master)
            self._on_change("text_string", self._custom_str_var.get())
        else:
            self._custom_frame.pack_forget()
            self._on_change("text_string", value)

    def _on_change(self, key, value):
        elem = self.app.selected_element
        if not elem:
            return
        try:
            if key in ("x", "y", "width", "height", "rotation", "zorder"):
                setattr(elem, key, int(float(value)))
            elif key in ("alpha", "red", "green", "blue"):
                setattr(elem, key, max(0, min(255, int(float(value)))))
            elif key in ("pinch", "skew_x", "skew_y"):
                setattr(elem, key, round(float(value), 4))
            elif key in ("font_size", "anim_duration"):
                setattr(elem, key, int(float(value)))
            elif key in ("visible", "preserve_aspect_ratio", "no_audio", "anim_enabled"):
                setattr(elem, key, bool(value))
            else:
                setattr(elem, key, value)
            self.app.update_code()
            self.app.canvas.redraw()
            self.app.refresh_element_list()
        except (ValueError, TypeError):
            pass

    def load_element(self, elem):
        self.no_sel.pack_forget()
        self.prop_frame.pack(fill="both", expand=True)

        str_keys = ["name", "blend_mode", "trigger", "align", "font", "anim_type"]
        int_keys = ["x", "y", "width", "height", "rotation", "alpha", "zorder",
                    "font_size", "anim_duration", "red", "green", "blue"]
        float_keys = ["pinch", "skew_x", "skew_y"]
        bool_keys = ["visible", "preserve_aspect_ratio", "no_audio", "anim_enabled"]

        for k in str_keys + int_keys:
            if k in self.vars:
                v = getattr(elem, k, "")
                self.vars[k].set(str(v) if v is not None else "")
        for k in float_keys:
            if k in self.vars:
                v = getattr(elem, k, 0.0)
                self.vars[k].set(str(v) if v is not None else "0.0")
        for k in bool_keys:
            if k in self.vars:
                self.vars[k].set(getattr(elem, k, False))

        # ── Restore meta picker / custom text field ───────────────────────
        ts = getattr(elem, "text_string", "[Title]")
        if ts in META_TOKENS and ts != "-- custom --":
            self._meta_var.set(ts)
            self._custom_frame.pack_forget()
        else:
            self._meta_var.set("-- custom --")
            self._custom_str_var.set(ts)
            self._custom_frame.pack(fill="x")

        fc = getattr(elem, "font_color", "#ffffff")
        self._font_color_val = fc
        self.color_btn.configure(fg_color=fc,
                                  text_color="#000000" if _is_light(fc) else "#ffffff")
        self.vars["font_color"] = fc

    def clear(self):
        self.prop_frame.pack_forget()
        self.no_sel.pack(pady=20)


def _is_light(hex_color):
    """Return True if a hex colour is perceived as light (for readable button text)."""
    try:
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return (r * 299 + g * 587 + b * 114) / 1000 > 128
    except Exception:
        return False

# ─── Main Application ─────────────────────────────────────────────────────────

class AttractLayoutBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()
        _sync_colors("Arctic Light")   # default theme; also sets CTK appearance mode
        self.title("Attract-Mode Plus  ·  Layout Designer")
        self.geometry("1400x820")
        self.resizable(True, True)

        self.layout = dict(DEFAULT_LAYOUT)
        self.layout["elements"] = []
        self.layout["modules"] = []
        self.layout["snippets"] = []
        self.selected_element = None
        self._suppress_code_update = False

        self._apply_style()
        self._build_ui()
        self.update_code()

    def _apply_style(self):
        # ttk styling is still needed for Treeview and Combobox widgets
        # that don't have CTK equivalents.
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=COLORS["panel2"],
                        background=COLORS["panel2"], foreground=COLORS["text"],
                        selectbackground=COLORS["border"],
                        font=("Courier", 10))
        style.configure("Sash", sashthickness=5, relief="flat",
                        background=COLORS["border"])
        style.configure("Rom.Treeview",
                        background=COLORS["panel2"],
                        foreground=COLORS["text"],
                        fieldbackground=COLORS["panel2"],
                        rowheight=22,
                        font=("Courier", 11))
        style.configure("Rom.Treeview.Heading",
                        background=COLORS["border"],
                        foreground=COLORS["accent"],
                        font=("Courier", 11, "bold"),
                        relief="flat")
        style.map("Rom.Treeview",
                  background=[("selected", COLORS["border"])],
                  foreground=[("selected", COLORS["accent"])])
        style.map("Rom.Treeview.Heading",
                  background=[("active", COLORS["panel2"])])

    def _btn(self, parent, text, cmd, color=None, small=False):
        # color arg is ignored — all buttons now use the theme palette consistently
        font_size = 11 if small else 12
        b = ctk.CTkButton(
            parent, text=text, command=cmd,
            fg_color=COLORS["panel2"],
            hover_color=COLORS["accent"],
            text_color=COLORS["text"],
            font=ctk.CTkFont(family="Courier", size=font_size,
                             weight="bold" if not small else "normal"),
            corner_radius=4,
            height=28 if small else 32,
        )
        return b

    def _build_ui(self):
        # ── Top bar ──
        topbar = ctk.CTkFrame(self, fg_color=COLORS["panel"], height=46, corner_radius=0)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        ctk.CTkLabel(topbar, text="⚡ ATTRACT-MODE PLUS  LAYOUT DESIGNER",
                     text_color=COLORS["accent"],
                     font=ctk.CTkFont(family="Courier", size=13, weight="bold")).pack(
                         side="left", padx=16, pady=10)

        for txt, cmd in [("💾 Save .nut", self.save_nut),
                         ("📂 Load .nut", self.load_nut),
                         ("🗑 Clear All", self.clear_all),
                         ("❓ Help",      self.show_help),
                         ("🎨 Theme",     self.show_theme_picker)]:
            self._btn(topbar, txt, cmd).pack(side="right", padx=4, pady=6)

        # ── Resolution bar ──
        resbar = ctk.CTkFrame(self, fg_color=COLORS["panel2"], height=30, corner_radius=0)
        resbar.pack(fill="x", side="top")
        resbar.pack_propagate(False)

        ctk.CTkLabel(resbar, text="W:", text_color=COLORS["text_dim"],
                     font=ctk.CTkFont(family="Courier", size=11)).pack(side="left", padx=(8, 2))
        self.res_w_var = tk.StringVar(value="1920")
        res_w_entry = ctk.CTkEntry(resbar, textvariable=self.res_w_var, width=60,
                                   fg_color=COLORS["panel"], text_color=COLORS["accent"],
                                   border_color=COLORS["border"],
                                   font=ctk.CTkFont(family="Courier", size=10))
        res_w_entry.pack(side="left", pady=4)
        res_w_entry.bind("<Return>", self._apply_resolution)
        res_w_entry.bind("<FocusOut>", self._apply_resolution)
        self.res_w_var.trace_add("write", lambda *a: self._apply_resolution())

        ctk.CTkLabel(resbar, text="H:", text_color=COLORS["text_dim"],
                     font=ctk.CTkFont(family="Courier", size=11)).pack(side="left", padx=(6, 2))
        self.res_h_var = tk.StringVar(value="1080")
        res_h_entry = ctk.CTkEntry(resbar, textvariable=self.res_h_var, width=60,
                                   fg_color=COLORS["panel"], text_color=COLORS["accent"],
                                   border_color=COLORS["border"],
                                   font=ctk.CTkFont(family="Courier", size=10))
        res_h_entry.pack(side="left", pady=4)
        res_h_entry.bind("<Return>", self._apply_resolution)
        res_h_entry.bind("<FocusOut>", self._apply_resolution)
        self.res_h_var.trace_add("write", lambda *a: self._apply_resolution())

        ctk.CTkLabel(resbar, text="Presets:", text_color=COLORS["text_dim"],
                     font=ctk.CTkFont(family="Courier", size=11)).pack(side="left", padx=(10, 2))
        self.preset_var = tk.StringVar(value="— pick —")
        presets = ["— pick —", "3840x2160", "2560x1440", "1920x1080",
                   "1600x900", "1366x768", "1280x720", "1024x768",
                   "800x600", "640x480"]
        preset_cb = ctk.CTkComboBox(resbar, variable=self.preset_var,
                                    values=presets, state="readonly",
                                    width=130,
                                    fg_color=COLORS["panel2"],
                                    button_color=COLORS["border"],
                                    dropdown_fg_color=COLORS["panel"],
                                    text_color=COLORS["text"],
                                    font=ctk.CTkFont(family="Courier", size=11),
                                    command=lambda v: self._apply_preset())
        preset_cb.pack(side="left", padx=4, pady=2)

        ctk.CTkLabel(resbar, text="Canvas Zoom:", text_color=COLORS["text_dim"],
                     font=ctk.CTkFont(family="Courier", size=11)).pack(side="left", padx=(16, 4))
        self.zoom_var = tk.DoubleVar(value=0.4)
        zoom_scale = ctk.CTkSlider(resbar, from_=0.1, to=1.0, variable=self.zoom_var,
                                   width=120, progress_color=COLORS["accent"],
                                   button_color=COLORS["accent"],
                                   command=lambda v: self._apply_zoom(float(v)))
        zoom_scale.pack(side="left")

        # ── Main area — three-pane PanedWindow (raw tk, no CTK equivalent) ──
        main = tk.PanedWindow(self, orient="horizontal", bg=COLORS["border"],
                              sashwidth=5, sashrelief="flat", handlesize=0)
        main.pack(fill="both", expand=True)

        # Left panel — fixed width, does not stretch
        left = tk.Frame(main, bg=COLORS["panel"])
        main.add(left, minsize=220, width=260, stretch="never")

        left_nb = ctk.CTkTabview(left, fg_color=COLORS["panel"],
                                  segmented_button_fg_color=COLORS["panel"],
                                  segmented_button_selected_color=COLORS["accent"],
                                  segmented_button_selected_hover_color=COLORS["accent"],
                                  segmented_button_unselected_color=COLORS["panel2"],
                                  segmented_button_unselected_hover_color=COLORS["border"],
                                  text_color=COLORS["text"],
                                  text_color_disabled=COLORS["text_dim"])
        left_nb.pack(fill="both", expand=True)

        for tab_name in ["Elements", "Modules", "Romlist", "CFG Gen", "Snippets"]:
            left_nb.add(tab_name)

        self._build_elements_tab(left_nb.tab("Elements"))
        self._build_modules_tab(left_nb.tab("Modules"))
        self._build_romlist_tab(left_nb.tab("Romlist"))
        self._build_cfg_tab(left_nb.tab("CFG Gen"))
        self._build_snippets_tab(left_nb.tab("Snippets"))

        # Center: Canvas
        center = tk.Frame(main, bg=COLORS["bg"])
        main.add(center, minsize=300, width=700, stretch="always")

        canvas_label = tk.Label(center,
                                text="◈ LAYOUT PREVIEW  (drag to move · drag corner to resize · right-click for options)",
                                bg=COLORS["bg"], fg=COLORS["text_dim"],
                                font=("Courier", 11))
        canvas_label.pack(anchor="w", padx=8, pady=2)

        self.canvas = LayoutCanvas(center, self)
        self.canvas.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # Right: Properties + Code tabs — fixed width, does not stretch
        right = tk.Frame(main, bg=COLORS["panel"])
        main.add(right, minsize=280, width=340, stretch="never")

        right_nb = ctk.CTkTabview(right, fg_color=COLORS["panel"],
                                   segmented_button_fg_color=COLORS["panel"],
                                   segmented_button_selected_color=COLORS["accent"],
                                   segmented_button_selected_hover_color=COLORS["accent"],
                                   segmented_button_unselected_color=COLORS["panel2"],
                                   segmented_button_unselected_hover_color=COLORS["border"],
                                   text_color=COLORS["text"],
                                   text_color_disabled=COLORS["text_dim"])
        right_nb.pack(fill="both", expand=True)

        for tab_name in ["Properties", "layout.nut", "Reference", "AM+ Docs"]:
            right_nb.add(tab_name)

        # Props tab — scrollable
        props_tab = right_nb.tab("Properties")
        ps = ctk.CTkScrollableFrame(props_tab, fg_color=COLORS["panel"])
        ps.pack(fill="both", expand=True)
        self.props = PropertiesPanel(ps, self)
        self.props.pack(fill="both", expand=True)

        self._build_code_tab(right_nb.tab("layout.nut"))
        self._build_reference_tab(right_nb.tab("Reference"))
        self._build_docs_tab(right_nb.tab("AM+ Docs"))

    def _toggle_appearance(self):
        # Legacy method — theming now handled via show_theme_picker / apply_theme
        self.show_theme_picker()


    def _build_elements_tab(self, parent):
        # Vertical PanedWindow — user can drag the sash to resize both sections
        pane = tk.PanedWindow(parent, orient="vertical",
                              bg=COLORS["border"], sashwidth=5,
                              sashrelief="flat", handlesize=0)
        pane.pack(fill="both", expand=True)

        # ── Top pane: type picker + add button ────────────────────────────────
        top = tk.Frame(pane, bg=COLORS["panel"])
        pane.add(top, minsize=120, stretch="always")

        ctk.CTkLabel(top, text="◈ ADD ELEMENT", text_color=COLORS["accent"],
                     font=ctk.CTkFont(family="Courier", size=10, weight="bold")).pack(
                         anchor="w", padx=8, pady=(8, 4))

        self.new_elem_type = tk.StringVar(value="snap")
        type_frame = ctk.CTkScrollableFrame(top, fg_color=COLORS["panel"])
        type_frame.pack(fill="both", expand=True, padx=6)
        for et in ELEMENT_TYPES:
            icon = {"snap": "📷", "wheel": "🎡", "boxart": "📦", "marquee": "📺",
                    "video": "▶", "text": "T", "flyer": "🗞", "fanart": "🖼",
                    "surface": "▣", "artwork": "🎨", "shader_layer": "✨"}.get(et, "?")
            rb = ctk.CTkRadioButton(type_frame, text=f"{icon} {et}",
                                    variable=self.new_elem_type, value=et,
                                    text_color=COLORS["text"],
                                    fg_color=COLORS["accent"],
                                    hover_color=COLORS["accent"],
                                    font=ctk.CTkFont(family="Courier", size=11))
            rb.pack(anchor="w", pady=2)

        self._btn(top, "+ Add Element", self.add_element,
                  color=None).pack(fill="x", padx=6, pady=6)

        # ── Bottom pane: element list ─────────────────────────────────────────
        bottom = tk.Frame(pane, bg=COLORS["panel"])
        pane.add(bottom, minsize=80, stretch="always")

        ctk.CTkLabel(bottom, text="◈ ELEMENT LIST", text_color=COLORS["accent"],
                     font=ctk.CTkFont(family="Courier", size=10, weight="bold")).pack(
                         anchor="w", padx=8, pady=(8, 2))

        list_frame = tk.Frame(bottom, bg=COLORS["panel"])
        list_frame.pack(fill="both", expand=True, padx=4)
        sb = tk.Scrollbar(list_frame)
        sb.pack(side="right", fill="y")
        self.elem_listbox = tk.Listbox(list_frame, yscrollcommand=sb.set,
                                       bg=COLORS["panel2"], fg=COLORS["text"],
                                       selectbackground="#2d5a5a",
                                       selectforeground=COLORS["text"],
                                       font=("Courier", 11), relief="flat",
                                       activestyle="none", bd=0)
        self.elem_listbox.pack(fill="both", expand=True)
        sb.config(command=self.elem_listbox.yview)
        self.elem_listbox.bind("<<ListboxSelect>>", self._on_list_select)

        btn_row = tk.Frame(bottom, bg=COLORS["panel"])
        btn_row.pack(fill="x", padx=4, pady=4)
        self._btn(btn_row, "↑", lambda: self.change_zorder(self.selected_element, 1),
                  small=True).pack(side="left", padx=2)
        self._btn(btn_row, "↓", lambda: self.change_zorder(self.selected_element, -1),
                  small=True).pack(side="left", padx=2)
        self._btn(btn_row, "⊕ Dupe", lambda: self.duplicate_element(self.selected_element),
                  small=True).pack(side="left", padx=2)
        self._btn(btn_row, "✕ Del", lambda: self.delete_element(self.selected_element),
                  small=True).pack(side="left", padx=2)

    def _build_modules_tab(self, parent):
        ctk.CTkLabel(parent, text="◈ MODULES", text_color=COLORS["accent"],
                     font=ctk.CTkFont(family="Courier", size=10, weight="bold")).pack(
                         anchor="w", padx=8, pady=(8, 4))
        ctk.CTkLabel(parent, text="Check to include  ·  hover for info",
                     text_color=COLORS["text_dim"],
                     font=ctk.CTkFont(family="Courier", size=11)).pack(
                         anchor="w", padx=8, pady=(0, 4))

        # ── Scrollable module list using CTkScrollableFrame ──
        mod_scroll = ctk.CTkScrollableFrame(parent, fg_color=COLORS["panel"])
        mod_scroll.pack(fill="both", expand=True, padx=4, pady=(0, 2))

        # ── Floating tooltip ──
        self._tt_win = None

        def _show_tt(e, text):
            if self._tt_win:
                self._tt_win.destroy()
            tw = tk.Toplevel(self)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{e.x_root+16}+{e.y_root+10}")
            tw.attributes("-topmost", True)
            border = tk.Frame(tw, bg=COLORS["accent"], padx=1, pady=1)
            border.pack()
            inner = tk.Frame(border, bg=COLORS["panel"], padx=10, pady=7)
            inner.pack()
            tk.Label(inner, text=text, bg=COLORS["panel"], fg=COLORS["text"],
                     font=("Courier", 11), justify="left", wraplength=270).pack()
            self._tt_win = tw

        def _hide_tt(e):
            if self._tt_win:
                self._tt_win.destroy()
                self._tt_win = None

        # ── Info bar ──
        self.mod_info_var = tk.StringVar(value="  Hover a module to see details")
        mod_info = tk.Label(parent, textvariable=self.mod_info_var,
                            bg=COLORS["panel2"], fg=COLORS["accent"],
                            font=("Courier", 11), wraplength=215,
                            justify="left", anchor="nw", padx=6, pady=5)
        mod_info.pack(fill="x", padx=4, pady=(0, 2))

        # ── Module rows ──
        self.module_vars = {}
        for name, file, desc in MODULE_LIST:
            v = tk.BooleanVar(value=False)
            self.module_vars[name] = v
            tip = f"  {name}\n  file: {file}\n\n  {desc}"

            row = tk.Frame(mod_scroll, bg=COLORS["panel"],
                           highlightthickness=1,
                           highlightbackground=COLORS["panel"])
            row.pack(fill="x", padx=3, pady=2)

            cb = ctk.CTkCheckBox(row, text=f" {name}", variable=v,
                                  text_color=COLORS["text"],
                                  fg_color=COLORS["accent"],
                                  hover_color=COLORS["accent"],
                                  font=ctk.CTkFont(family="Courier", size=11, weight="bold"),
                                  command=self.update_code)
            cb.pack(side="left", padx=(2, 0), pady=2)

            fl = tk.Label(row, text=file, bg=COLORS["panel"],
                          fg=COLORS["text_dim"], font=("Courier", 11))
            fl.pack(side="right", padx=6)

            for w in (row, cb, fl):
                w.bind("<Enter>", lambda e, r=row, t=tip, n=name, f=file, d=desc:
                       (r.config(highlightbackground=COLORS["accent"]),
                        self.mod_info_var.set(f"◈ {n}  |  {f}\n{d}"),
                        _show_tt(e, t)))
                w.bind("<Leave>", lambda e, r=row:
                       (r.config(highlightbackground=COLORS["panel"]),
                        self.mod_info_var.set("  Hover a module to see details"),
                        _hide_tt(e)))


    def _build_code_tab(self, parent):
        toolbar = tk.Frame(parent, bg=COLORS["panel2"])
        toolbar.pack(fill="x")
        self._btn(toolbar, "📋 Copy", self.copy_code, small=True).pack(side="left", padx=4, pady=3)
        self._btn(toolbar, "💾 Save .nut", self.save_nut, small=True).pack(side="left", padx=2, pady=3)
        self.auto_update_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(toolbar, text="Auto-update", variable=self.auto_update_var,
                         text_color=COLORS["text_dim"],
                         fg_color=COLORS["accent"],
                         hover_color=COLORS["accent"],
                         font=ctk.CTkFont(family="Courier", size=11)).pack(side="right", padx=6)

        sb_y = tk.Scrollbar(parent, orient="vertical")
        sb_y.pack(side="right", fill="y")
        sb_x = tk.Scrollbar(parent, orient="horizontal")
        sb_x.pack(side="bottom", fill="x")
        self.code_text = tk.Text(parent, yscrollcommand=sb_y.set,
                                 xscrollcommand=sb_x.set,
                                 bg="#0d1117", fg="#00ff88",
                                 insertbackground="#00ff88",
                                 font=("Courier", 10), relief="flat",
                                 wrap="none", bd=0, padx=8, pady=8)
        self.code_text.pack(fill="both", expand=True)
        sb_y.config(command=self.code_text.yview)
        sb_x.config(command=self.code_text.xview)

        # Syntax highlighting tags
        self.code_text.tag_configure("comment", foreground="#446644")
        self.code_text.tag_configure("keyword", foreground="#00e5ff")
        self.code_text.tag_configure("string", foreground="#ffaa44")
        self.code_text.tag_configure("number", foreground="#ff6b35")
        self.code_text.tag_configure("func", foreground="#aa88ff")

        self.code_text.bind("<KeyRelease>", self._on_code_edit)

    # ── Actions ──────────────────────────────────────────────────────────────

    def add_element(self):
        etype = self.new_elem_type.get()
        count = sum(1 for e in self.layout["elements"] if e.type == etype)
        elem = LayoutElement(etype, f"{etype}_{count+1}")
        # Stack vertically to avoid overlap
        elem.x = 50 + (len(self.layout["elements"]) % 5) * 50
        elem.y = 50 + (len(self.layout["elements"]) % 5) * 50
        elem.zorder = len(self.layout["elements"])
        self.layout["elements"].append(elem)
        self.select_element(elem)
        self.refresh_element_list()
        self.update_code()
        self.canvas.redraw()

    def delete_element(self, elem):
        if elem and elem in self.layout["elements"]:
            self.layout["elements"].remove(elem)
            if self.selected_element is elem:
                self.selected_element = None
                self.props.clear()
            self.refresh_element_list()
            self.update_code()
            self.canvas.redraw()

    def duplicate_element(self, elem):
        if not elem:
            return
        import copy
        new_elem = copy.deepcopy(elem)
        new_elem.name = elem.name + "_copy"
        new_elem.x += 20
        new_elem.y += 20
        new_elem.zorder = len(self.layout["elements"])
        self.layout["elements"].append(new_elem)
        self.select_element(new_elem)
        self.refresh_element_list()
        self.update_code()
        self.canvas.redraw()

    def change_zorder(self, elem, delta):
        if not elem:
            return
        elem.zorder += delta
        self.update_code()
        self.refresh_element_list()
        self.canvas.redraw()

    def select_element(self, elem):
        self.selected_element = elem
        if elem:
            self.props.load_element(elem)
        else:
            self.props.clear()
        self.refresh_element_list()

    def refresh_element_list(self):
        self.elem_listbox.delete(0, tk.END)
        for elem in sorted(self.layout["elements"], key=lambda e: e.name.lower()):
            icon = {"snap": "📷", "wheel": "🎡", "boxart": "📦", "marquee": "📺",
                    "video": "▶", "text": "T", "flyer": "🗞", "fanart": "🖼",
                    "surface": "▣", "clock": "🕐", "artwork": "🎨"}.get(elem.type, "?")
            vis = "" if elem.visible else " 🚫"
            self.elem_listbox.insert(tk.END, f"  {icon} {elem.name}{vis}")
            if elem is self.selected_element:
                self.elem_listbox.selection_set(tk.END)

    def refresh_props(self):
        if self.selected_element:
            self.props.load_element(self.selected_element)

    def _on_list_select(self, event):
        sel = self.elem_listbox.curselection()
        if not sel:
            return
        # Must match the sort order used in refresh_element_list (alphabetical by name)
        sorted_elems = sorted(self.layout["elements"], key=lambda e: e.name.lower())
        idx = sel[0]
        if idx < len(sorted_elems):
            self.select_element(sorted_elems[idx])
            self.canvas.redraw()

    def _apply_resolution(self, event=None):
        try:
            w = int(self.res_w_var.get())
            h = int(self.res_h_var.get())
            if w > 0 and h > 0:
                self.layout["width"] = w
                self.layout["height"] = h
                self.update_code()
                self.canvas.redraw()
        except (ValueError, AttributeError):
            pass

    def _apply_preset(self, event=None):
        val = self.preset_var.get()
        if "x" in val:
            w, h = val.split("x")
            try:
                self.res_w_var.set(w)
                self.res_h_var.set(h)
            except ValueError:
                pass
        self.preset_var.set("— pick —")

    def _apply_zoom(self, value):
        self.canvas.scale = value
        self.canvas.redraw()

    def generate_nut(self):
        lines = []
        lw = self.layout["width"]
        lh = self.layout["height"]

        # ── File header ───────────────────────────────────────────────────────
        lines.append("//////////////////////////////////////////////////////////////")
        lines.append("//  layout.nut — generated by Attract-Mode Plus Layout Designer")
        lines.append("//////////////////////////////////////////////////////////////")
        lines.append("")

        # ── UserConfig block (hardcoded AM+ standard header) ─────────────────
        lines.append("local orderx = 0;")
        lines.append("local divider = \"----\"")
        lines.append("class UserConfig {")
        lines.append("    </ label=\"Type of wheel\", help=\"Select round wheel or vertical wheel\", options=\"Round,Straight\", order=orderx++ /> wheel_type=\"Round\"")
        lines.append("    </ label=\"Startup animation transition time\",")
        lines.append("        help=\"Startup animation transition time in milliseconds\",")
        lines.append("        options=\"500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,2000\",")
        lines.append("        order=orderx++")
        lines.append("        />ini_anim_trans_ms=\"100\";")
        lines.append("    </ label=\"Enable wheel logos mipmap\", help=\"Mipmap reduces aliasing artifacts (jagged edges) for high resolution wheel logos\", options=\"Yes,No\", order=orderx++ /> wheel_logo_mipmap=\"No\";")
        lines.append("    </ label= divider, help=\" \", options = \" \", order=orderx++ /> paramxx1 = \" \"")
        lines.append("    </ label=\"Logo Pulse\", help=\"Enable / Disable Wheel Pulse\", options=\"Yes,No\", order=2 /> pulse=\"Yes\";")
        lines.append("    </ label=\"Logo Pulse Color\", help=\"Select Wheel Pulse Color\", options=\"Red,White,Blue,Black,Green,Purple,Yellow,Rainbow\", order=3 /> color=\"Red\";")
        lines.append("}")
        lines.append("cfg <- fe.get_config()")
        lines.append("")

        # ── Layout size (user-controlled W/H) ────────────────────────────────
        lines.append("// Layout Size")
        lines.append(f"fe.layout.width={lw};")
        lines.append(f"fe.layout.height={lh};")
        lines.append("local my_config = fe.get_config();")
        lines.append("local ini_anim_time;")
        lines.append("try { ini_anim_time =  my_config[\"ini_anim_trans_ms\"].tointeger(); } catch ( e ) { }")
        lines.append("local aspect = fe.layout.width / fe.layout.height.tofloat();")
        lines.append("local flx = fe.layout.width;")
        lines.append("local fly = fe.layout.height;")
        lines.append("local flw = fe.layout.width;")
        lines.append("local flh = fe.layout.height;")
        lines.append("")

        # ── Modules ───────────────────────────────────────────────────────────
        active_mods = [name for name, v in self.module_vars.items() if v.get()]
        if active_mods:
            lines.append("// ── Modules ──────────────────────────────────────")
            for name in active_mods:
                lines.append(f'fe.load_module("{name}");')
            lines.append("")

        # ── Visual elements (from canvas) ─────────────────────────────────────
        if self.layout["elements"]:
            lines.append("// ── Layout Elements ──────────────────────────────")
            sorted_elems = sorted(self.layout["elements"], key=lambda e: e.zorder)
            for elem in sorted_elems:
                lines.append(f"\n// {elem.type.upper()} · {elem.name}")
                lines.append(elem.to_nut(indent=0, lw=lw, lh=lh))
            lines.append("")

        # ── Inserted snippets (preserved across updates) ──────────────────────
        snippets = self.layout.get("snippets", [])
        if snippets:
            lines.append("// ── Snippets ─────────────────────────────────────")
            for snip in snippets:
                lines.append("")
                lines.append(f"// snippet: {snip['name']}")
                lines.append(snip["code"])

        lines.append("")
        lines.append("// ── End of layout ────────────────────────────────")
        return "\n".join(lines)

    def update_code(self):
        if not self.auto_update_var.get() if hasattr(self, "auto_update_var") else False:
            return
        code = self.generate_nut()
        self.code_text.delete("1.0", tk.END)
        self.code_text.insert("1.0", code)
        self._highlight_code()

    def _highlight_code(self):
        import re
        text = self.code_text
        content = text.get("1.0", tk.END)
        for tag in ("comment", "keyword", "string", "number", "func"):
            text.tag_remove(tag, "1.0", tk.END)

        patterns = [
            ("comment", r"//[^\n]*"),
            ("string", r'"[^"]*"'),
            ("keyword", r'\b(local|if|else|for|while|return|true|false|null|function|class|extends|this|fe|RotateScreen|BlendMode|Align|Transition|Tween)\b'),
            ("func", r'\b(add_artwork|add_text|add_surface|load_module|add_sound|add_shader)\b'),
            ("number", r'\b\d+(\.\d+)?\b'),
        ]
        for tag, pattern in patterns:
            for m in re.finditer(pattern, content):
                start = f"1.0 + {m.start()} chars"
                end = f"1.0 + {m.end()} chars"
                text.tag_add(tag, start, end)

    def _on_code_edit(self, event=None):
        self._highlight_code()

    def copy_code(self):
        code = self.code_text.get("1.0", tk.END)
        self.clipboard_clear()
        self.clipboard_append(code)
        messagebox.showinfo("Copied", "layout.nut code copied to clipboard!")

    def save_nut(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".nut",
            filetypes=[("Squirrel Script", "*.nut"), ("All Files", "*.*")],
            title="Save layout.nut",
            initialfile="layout.nut"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.generate_nut())
            messagebox.showinfo("Saved", f"Saved to:\n{path}")

    def load_nut(self):
        path = filedialog.askopenfilename(
            filetypes=[("Squirrel Script", "*.nut"), ("All Files", "*.*")],
            title="Load layout.nut (preview only)"
        )
        if path:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.code_text.delete("1.0", tk.END)
            self.code_text.insert("1.0", content)
            self._highlight_code()
            messagebox.showinfo("Loaded", f"File loaded for viewing:\n{path}\n\n(Visual editor not populated from file import — use the code tab to edit manually.)")

    def clear_all(self):
        if messagebox.askyesno("Clear All", "Remove all elements and reset the layout?"):
            self.layout["elements"] = []
            self.layout["snippets"] = []
            self.selected_element = None
            self.props.clear()
            self.refresh_element_list()
            self.update_code()
            self.canvas.redraw()

    def _build_snippets_tab(self, parent):
        import os

        self._snip_folder   = tk.StringVar(value="")
        self._snip_files    = []
        self._snip_current  = ""

        # ── Header ────────────────────────────────────────────────────────────
        hdr = tk.Frame(parent, bg=COLORS["panel2"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="◈ CODE SNIPPETS", bg=COLORS["panel2"],
                 fg=COLORS["accent"], font=("Courier", 10, "bold")).pack(
                     side="left", padx=8, pady=5)

        # ── Folder bar ────────────────────────────────────────────────────────
        fb = tk.Frame(parent, bg=COLORS["panel"])
        fb.pack(fill="x", padx=6, pady=(4, 2))
        tk.Label(fb, text="Folder:", bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 11)).pack(side="left")
        self._snip_folder_lbl = tk.Label(fb, text="No folder loaded",
                                          bg=COLORS["panel"], fg=COLORS["text_dim"],
                                          font=("Courier", 11), anchor="w")
        self._snip_folder_lbl.pack(side="left", fill="x", expand=True, padx=4)
        self._btn(fb, "📂 Open Folder", self._snip_open_folder, small=True).pack(side="right", padx=4, pady=2)
        self._btn(fb, "🔄 Reload",       self._snip_reload,       small=True).pack(side="right", padx=2, pady=2)

        # ── Category filter tabs ──────────────────────────────────────────────
        cat_frame = tk.Frame(parent, bg=COLORS["panel"])
        cat_frame.pack(fill="x", padx=6, pady=(0, 2))
        tk.Label(cat_frame, text="Filter:", bg=COLORS["panel"],
                 fg=COLORS["text_dim"], font=("Courier", 11)).pack(side="left")
        self._snip_filter_var = tk.StringVar(value="All")
        self._snip_cat_btns = {}
        for cat in ["All", "wheel", "snap", "meta", "text", "other"]:
            b = ctk.CTkButton(cat_frame, text=cat, width=46, height=22,
                               fg_color=COLORS["panel2"], hover_color=COLORS["accent"],
                               text_color=COLORS["text_dim"],
                               font=ctk.CTkFont(family="Courier", size=11),
                               corner_radius=3,
                               command=lambda c=cat: self._snip_set_filter(c))
            b.pack(side="left", padx=2, pady=2)
            self._snip_cat_btns[cat] = b
        self._snip_set_filter("All")

        # ── Search bar ────────────────────────────────────────────────────────
        sf = tk.Frame(parent, bg=COLORS["panel2"])
        sf.pack(fill="x", padx=6, pady=(0, 4))
        tk.Label(sf, text="🔍", bg=COLORS["panel2"], fg=COLORS["text_dim"],
                 font=("Courier", 11)).pack(side="left", padx=4)
        self._snip_search_var = tk.StringVar()
        ctk.CTkEntry(sf, textvariable=self._snip_search_var,
                     fg_color=COLORS["panel2"], text_color=COLORS["text"],
                     border_color=COLORS["border"], height=24,
                     font=ctk.CTkFont(family="Courier", size=11)).pack(
                         side="left", fill="x", expand=True, pady=3)
        ctk.CTkButton(sf, text="✕", width=24, height=22,
                       fg_color=COLORS["panel2"], hover_color=COLORS["border"],
                       text_color=COLORS["text_dim"],
                       font=ctk.CTkFont(family="Courier", size=11),
                       command=lambda: self._snip_search_var.set("")).pack(side="right", padx=4)
        self._snip_search_var.trace_add("write", lambda *a: self._snip_populate())

        # ── Vertical PanedWindow: file list | preview | added list ───────────
        vpane = tk.PanedWindow(parent, orient="vertical",
                               bg=COLORS["border"], sashwidth=5,
                               sashrelief="flat", handlesize=0)
        vpane.pack(fill="both", expand=True, padx=0, pady=0)

        # ── File list pane ────────────────────────────────────────────────────
        list_pane = tk.Frame(vpane, bg=COLORS["panel"])
        vpane.add(list_pane, minsize=60, stretch="always")

        list_sb = tk.Scrollbar(list_pane, orient="vertical")
        list_sb.pack(side="right", fill="y")
        self._snip_listbox = tk.Listbox(list_pane, yscrollcommand=list_sb.set,
                                         bg=COLORS["panel2"], fg=COLORS["text"],
                                         selectbackground=COLORS["border"],
                                         selectforeground=COLORS["accent"],
                                         font=("Courier", 11), relief="flat",
                                         activestyle="none", bd=0)
        self._snip_listbox.pack(fill="both", expand=True)
        list_sb.config(command=self._snip_listbox.yview)
        self._snip_listbox.bind("<<ListboxSelect>>", self._snip_on_select)
        self._snip_listbox.bind("<Double-1>",         self._snip_insert)

        # ── Preview pane ──────────────────────────────────────────────────────
        prev_pane = tk.Frame(vpane, bg=COLORS["panel"])
        vpane.add(prev_pane, minsize=60, stretch="always")

        tk.Label(prev_pane, text="PREVIEW  (double-click list to insert)",
                 bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 11), anchor="w").pack(fill="x", padx=8, pady=(2, 0))

        prev_frame = tk.Frame(prev_pane, bg=COLORS["panel"])
        prev_frame.pack(fill="both", expand=True, padx=6, pady=(0, 2))
        psby = tk.Scrollbar(prev_frame, orient="vertical")
        psby.pack(side="right", fill="y")
        psbx = tk.Scrollbar(prev_frame, orient="horizontal")
        psbx.pack(side="bottom", fill="x")
        self._snip_preview = tk.Text(prev_frame, bg="#0d1117", fg="#00ff88",
                                      font=("Courier", 11), relief="flat",
                                      wrap="none", bd=0, padx=6, pady=4,
                                      yscrollcommand=psby.set,
                                      xscrollcommand=psbx.set, state="disabled")
        self._snip_preview.pack(fill="both", expand=True)
        psby.config(command=self._snip_preview.yview)
        psbx.config(command=self._snip_preview.xview)
        for tag, col in [("comment","#446644"),("keyword","#00e5ff"),
                         ("string","#ffaa44"),("number","#ff6b35"),("func","#aa88ff")]:
            self._snip_preview.tag_configure(tag, foreground=col)

        # ── Action buttons ────────────────────────────────────────────────────
        btn_row = tk.Frame(parent, bg=COLORS["panel"])
        btn_row.pack(fill="x", padx=6, pady=4)
        self._btn(btn_row, "⎘ Insert", self._snip_insert,    small=True).pack(side="left", padx=2)
        self._btn(btn_row, "📋 Copy",   self._snip_copy,      small=True).pack(side="left", padx=2)
        self._btn(btn_row, "📄 Open",   self._snip_open_file, small=True).pack(side="left", padx=2)

        # ── Added snippets list pane ──────────────────────────────────────────
        added_pane = tk.Frame(vpane, bg=COLORS["panel"])
        vpane.add(added_pane, minsize=50, stretch="always")

        tk.Label(added_pane, text="IN LAYOUT  (double-click to edit)",
                 bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 11), anchor="w").pack(fill="x", padx=8, pady=(4, 0))

        added_frame = tk.Frame(added_pane, bg=COLORS["panel"])
        added_frame.pack(fill="both", expand=True, padx=6, pady=(0, 2))
        added_sb = tk.Scrollbar(added_frame, orient="vertical")
        added_sb.pack(side="right", fill="y")
        self._snip_added_box = tk.Listbox(added_frame, yscrollcommand=added_sb.set,
                                           bg=COLORS["panel2"], fg=COLORS["accent"],
                                           selectbackground=COLORS["border"],
                                           selectforeground=COLORS["accent2"],
                                           font=("Courier", 11), relief="flat",
                                           activestyle="none", bd=0)
        self._snip_added_box.pack(fill="both", expand=True)
        added_sb.config(command=self._snip_added_box.yview)
        self._snip_added_box.bind("<Double-1>", lambda e: self._snip_edit())

        rem_row = tk.Frame(parent, bg=COLORS["panel"])
        rem_row.pack(fill="x", padx=6, pady=(0, 2))
        self._btn(rem_row, "✎ Edit",    self._snip_edit,       small=True).pack(side="left", padx=2)
        self._btn(rem_row, "✕ Remove",  self._snip_remove,     small=True).pack(side="left", padx=2)
        self._btn(rem_row, "✕ All",     self._snip_remove_all, small=True).pack(side="left", padx=2)

        # ── Status bar ────────────────────────────────────────────────────────
        self._snip_status_var = tk.StringVar(value="Open a folder containing .txt snippet files")
        tk.Label(parent, textvariable=self._snip_status_var,
                 bg=COLORS["panel2"], fg=COLORS["text_dim"],
                 font=("Courier", 11), anchor="w", padx=6).pack(fill="x", side="bottom")

        default_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "snippets")
        if os.path.isdir(default_folder):
            self.after(100, lambda: self._snip_load_folder(default_folder))

    # ── Snippets helpers ──────────────────────────────────────────────────────

    def _snip_set_filter(self, cat):
        self._snip_filter_var.set(cat)
        for name, btn in self._snip_cat_btns.items():
            if name == cat:
                btn.configure(fg_color=COLORS["accent"], text_color=COLORS["bg"])
            else:
                btn.configure(fg_color=COLORS["panel2"], text_color=COLORS["text_dim"])
        if hasattr(self, '_snip_listbox'):
            self._snip_populate()

    def _snip_open_folder(self):
        import os
        folder = filedialog.askdirectory(title="Select Snippets Folder")
        if folder:
            self._snip_load_folder(folder)

    def _snip_load_folder(self, folder):
        import os
        self._snip_files = []
        exts = (".txt", ".nut", ".sq")
        try:
            for fname in sorted(os.listdir(folder)):
                if fname.lower().endswith(exts):
                    full = os.path.join(folder, fname)
                    display = os.path.splitext(fname)[0]
                    self._snip_files.append((display, full))
        except Exception as e:
            messagebox.showerror("Error", f"Could not read folder:\n{e}")
            return

        short = os.path.basename(folder)
        self._snip_folder_lbl.configure(text=folder)
        self._snip_folder.set(folder)
        self._snip_populate()
        count = len(self._snip_files)
        self._snip_status_var.set(
            f"Loaded {count} snippet{'s' if count != 1 else ''}  —  {short}")

    def _snip_reload(self):
        folder = self._snip_folder.get()
        if folder:
            self._snip_load_folder(folder)
        else:
            messagebox.showinfo("Info", "Open a folder first.")

    def _snip_populate(self):
        # Guard against being called before listbox is created
        if not hasattr(self, '_snip_listbox') or not self._snip_listbox.winfo_exists():
            return
        self._snip_listbox.delete(0, tk.END)
        cat    = self._snip_filter_var.get()
        search = self._snip_search_var.get().strip().lower()
        self._snip_visible = []   # indices into self._snip_files

        for i, (display, path) in enumerate(self._snip_files):
            dl = display.lower()
            # Category filter — match if the category word appears in filename
            if cat != "All" and cat.lower() not in dl:
                continue
            # Search filter
            if search and search not in dl:
                continue
            self._snip_visible.append(i)
            # Choose icon based on filename keywords
            icon = "📄"
            if any(k in dl for k in ("wheel", "logo")):
                icon = "🎡"
            elif any(k in dl for k in ("snap", "screenshot", "video")):
                icon = "📷"
            elif any(k in dl for k in ("meta", "info", "text", "title")):
                icon = "ℹ"
            elif any(k in dl for k in ("fanart", "flyer", "boxart", "marquee")):
                icon = "🖼"
            elif any(k in dl for k in ("conveyor", "belt")):
                icon = "🔄"
            elif any(k in dl for k in ("shader", "glsl")):
                icon = "✨"
            self._snip_listbox.insert(tk.END, f"  {icon}  {display}")

        count = len(self._snip_visible)
        total = len(self._snip_files)
        if total:
            self._snip_status_var.set(
                f"Showing {count} of {total} snippets"
                + (f"  —  filter: \"{search}\"" if search else ""))
        # Re-apply tick marks for already-added snippets
        self._snip_refresh_list()

    def _snip_on_select(self, event):
        sel = self._snip_listbox.curselection()
        if not sel:
            return
        pos = sel[0]
        if not hasattr(self, "_snip_visible") or pos >= len(self._snip_visible):
            return
        file_idx = self._snip_visible[pos]
        display, path = self._snip_files[file_idx]
        try:
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            self._snip_current = code
            self._snip_show_preview(code, display)
        except Exception as e:
            self._snip_status_var.set(f"Error reading file: {e}")

    def _snip_show_preview(self, code, title):
        import re
        t = self._snip_preview
        t.config(state="normal")
        t.delete("1.0", tk.END)
        t.insert("1.0", code)
        # Syntax highlight
        for tag in ("comment", "keyword", "string", "number", "func"):
            t.tag_remove(tag, "1.0", tk.END)
        patterns = [
            ("comment", r"//[^\n]*"),
            ("string",  r'"[^"]*"'),
            ("keyword", r"\b(local|if|else|for|foreach|while|return|true|false"
                        r"|null|function|class|extends|this|fe|switch|case"
                        r"|break|continue|try|catch|throw)\b"),
            ("func",    r"\b(fe\.add_wheel|fe\.add_artwork|fe\.add_text"
                        r"|fe\.add_image|fe\.add_surface|fe\.load_module"
                        r"|fe\.add_sound|fe\.add_shader)\b"),
            ("number",  r"\b\d+(\.\d+)?\b"),
        ]
        content = t.get("1.0", tk.END)
        for tag, pattern in patterns:
            for m in re.finditer(pattern, content):
                s = "1.0 + %d chars" % m.start()
                e = "1.0 + %d chars" % m.end()
                t.tag_add(tag, s, e)
        t.config(state="disabled")
        self._snip_status_var.set(
            f"  {title}  —  {len(code.splitlines())} lines")

    def _snip_insert(self, event=None):
        if not self._snip_current:
            messagebox.showinfo("Info", "Select a snippet first.")
            return
        # Get name from selected listbox item
        sel = self._snip_listbox.curselection()
        name = "snippet"
        if sel and hasattr(self, "_snip_visible") and sel[0] < len(self._snip_visible):
            file_idx = self._snip_visible[sel[0]]
            name = self._snip_files[file_idx][0]
        # Check not already inserted
        existing = [s["name"] for s in self.layout.get("snippets", [])]
        if name in existing:
            if not messagebox.askyesno("Already Added",
                    f"'{name}' is already in your layout.\nInsert it again?"):
                return
        # Store in layout state so update_code() preserves it
        if "snippets" not in self.layout:
            self.layout["snippets"] = []
        self.layout["snippets"].append({"name": name, "code": self._snip_current})
        self.update_code()
        self._snip_status_var.set(f"Snippet '{name}' added to layout ✓")
        self._snip_refresh_list()

    def _snip_refresh_list(self):
        """Sync tick marks on file list and rebuild the added-snippets box."""
        added = [s["name"] for s in self.layout.get("snippets", [])]

        # Update file list tick marks
        self._snip_listbox.delete(0, tk.END)
        if not hasattr(self, "_snip_visible"):
            return
        for pos, file_idx in enumerate(self._snip_visible):
            display, path = self._snip_files[file_idx]
            dl = display.lower()
            icon = "📄"
            if any(k in dl for k in ("wheel","logo")):       icon = "🎡"
            elif any(k in dl for k in ("snap","screenshot","video")): icon = "📷"
            elif any(k in dl for k in ("meta","info","text","title")): icon = "ℹ"
            elif any(k in dl for k in ("fanart","flyer","boxart","marquee")): icon = "🖼"
            elif any(k in dl for k in ("conveyor","belt")):   icon = "🔄"
            elif any(k in dl for k in ("shader","glsl")):     icon = "✨"
            tick = " ✓" if display in added else ""
            self._snip_listbox.insert(tk.END, f"  {icon}  {display}{tick}")

        # Rebuild added-snippets box
        if hasattr(self, "_snip_added_box"):
            self._snip_added_box.delete(0, tk.END)
            for s in self.layout.get("snippets", []):
                self._snip_added_box.insert(tk.END, f"  📎  {s['name']}")

    def _snip_edit(self):
        """Open a full editor for the selected IN LAYOUT snippet."""
        sel = self._snip_added_box.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a snippet from the IN LAYOUT list to edit.")
            return
        idx = sel[0]
        snippets = self.layout.get("snippets", [])
        if idx >= len(snippets):
            return
        snip = snippets[idx]

        win = ctk.CTkToplevel(self)
        win.title(f"Edit Snippet  —  {snip['name']}")
        win.geometry("820x600")
        win.transient(self)

        # Header
        hdr = tk.Frame(win, bg=COLORS["panel2"])
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"◈ EDITING:  {snip['name']}",
                 bg=COLORS["panel2"], fg=COLORS["accent"],
                 font=("Courier", 10, "bold")).pack(side="left", padx=10, pady=6)

        # Name field
        nf = tk.Frame(win, bg=COLORS["bg"])
        nf.pack(fill="x", padx=10, pady=(8, 2))
        tk.Label(nf, text="Snippet Name:", bg=COLORS["bg"],
                 fg=COLORS["text_dim"], font=("Courier", 11)).pack(side="left")
        name_var = tk.StringVar(value=snip["name"])
        ctk.CTkEntry(nf, textvariable=name_var,
                      fg_color=COLORS["panel2"], text_color=COLORS["text"],
                      border_color=COLORS["border"], width=320, height=28,
                      font=ctk.CTkFont(family="Courier", size=10)).pack(side="left", padx=8)

        # Code editor label
        tk.Label(win, text="Code:", bg=COLORS["bg"],
                 fg=COLORS["text_dim"], font=("Courier", 11), anchor="w").pack(fill="x", padx=10)

        edit_frame = tk.Frame(win, bg=COLORS["bg"])
        edit_frame.pack(fill="both", expand=True, padx=10, pady=(2, 4))

        eby = tk.Scrollbar(edit_frame, orient="vertical")
        eby.pack(side="right", fill="y")
        ebx = tk.Scrollbar(edit_frame, orient="horizontal")
        ebx.pack(side="bottom", fill="x")

        editor = tk.Text(edit_frame, bg="#0d1117", fg="#00ff88",
                         font=("Courier", 10), relief="flat",
                         wrap="none", bd=0, padx=8, pady=6,
                         insertbackground="#00ff88",
                         yscrollcommand=eby.set,
                         xscrollcommand=ebx.set)
        editor.pack(fill="both", expand=True)
        eby.config(command=editor.yview)
        ebx.config(command=editor.xview)

        # Syntax tags
        editor.tag_configure("comment", foreground="#446644")
        editor.tag_configure("keyword", foreground="#00e5ff")
        editor.tag_configure("string",  foreground="#ffaa44")
        editor.tag_configure("number",  foreground="#ff6b35")
        editor.tag_configure("func",    foreground="#aa88ff")

        editor.insert("1.0", snip["code"])

        # Live syntax highlight as user types
        def _highlight_editor(event=None):
            import re
            content_e = editor.get("1.0", tk.END)
            for tag in ("comment","keyword","string","number","func"):
                editor.tag_remove(tag, "1.0", tk.END)
            patterns = [
                ("comment", r"//[^\n]*"),
                ("string",  r'"[^"]*"'),
                ("keyword", r"\b(local|if|else|for|foreach|while|return|true|false"
                            r"|null|function|class|extends|this|fe|switch|case"
                            r"|break|continue|try|catch|throw)\b"),
                ("func",    r"\b(add_wheel|add_artwork|add_text"
                            r"|add_image|add_surface|load_module"
                            r"|add_sound|add_shader)\b"),
                ("number",  r"\b\d+(\.\d+)?\b"),
            ]
            for tag, pattern in patterns:
                for m in re.finditer(pattern, content_e):
                    s = "1.0 + %d chars" % m.start()
                    e = "1.0 + %d chars" % m.end()
                    editor.tag_add(tag, s, e)

        editor.bind("<KeyRelease>", _highlight_editor)
        _highlight_editor()

        # Button row
        btn_row = tk.Frame(win, bg=COLORS["bg"])
        btn_row.pack(fill="x", padx=10, pady=(0, 10))

        def _save():
            new_name = name_var.get().strip() or snip["name"]
            new_code = editor.get("1.0", tk.END).rstrip("\n")
            snippets[idx]["name"] = new_name
            snippets[idx]["code"] = new_code
            self.update_code()
            self._snip_refresh_list()
            self._snip_status_var.set(f"Snippet '{new_name}' saved ✓")
            win.destroy()

        def _save_close():
            _save()

        def _revert():
            if messagebox.askyesno("Revert",
                    "Revert to the original file on disk?"):
                _, path = self._snip_files[
                    next((i for i, (d, p) in enumerate(self._snip_files)
                          if d == snip["name"]), 0)]
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        orig = f.read()
                    editor.delete("1.0", tk.END)
                    editor.insert("1.0", orig)
                    _highlight_editor()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        self._btn(btn_row, "💾 Save Changes", _save_close,
                  small=True).pack(side="left", padx=4)
        self._btn(btn_row, "↩ Revert to File", _revert,
                  small=True).pack(side="left", padx=4)
        self._btn(btn_row, "✕ Cancel", win.destroy,
                  small=True).pack(side="right", padx=4)

        # Line/col indicator
        pos_var = tk.StringVar(value="Ln 1, Col 1")
        tk.Label(btn_row, textvariable=pos_var, bg=COLORS["bg"],
                 fg=COLORS["text_dim"],
                 font=("Courier", 11)).pack(side="right", padx=8)

        def _update_pos(event=None):
            try:
                idx_str = editor.index(tk.INSERT)
                ln, col = idx_str.split(".")
                pos_var.set(f"Ln {ln}, Col {int(col)+1}")
            except Exception:
                pass
        editor.bind("<KeyRelease>", lambda e: (_highlight_editor(), _update_pos()))
        editor.bind("<ButtonRelease>", _update_pos)
        editor.focus_set()

    def _snip_remove(self):
        sel = self._snip_added_box.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a snippet from the IN LAYOUT list.")
            return
        idx = sel[0]
        snippets = self.layout.get("snippets", [])
        if idx < len(snippets):
            name = snippets[idx]["name"]
            del snippets[idx]
            self.update_code()
            self._snip_refresh_list()
            self._snip_status_var.set(f"Removed '{name}' from layout")

    def _snip_remove_all(self):
        if not self.layout.get("snippets"):
            return
        if messagebox.askyesno("Remove All Snippets",
                               "Remove all snippets from the layout?"):
            self.layout["snippets"] = []
            self.update_code()
            self._snip_refresh_list()
            self._snip_status_var.set("All snippets removed")

    def _snip_copy(self):
        if not self._snip_current:
            messagebox.showinfo("Info", "Select a snippet first.")
            return
        self.clipboard_clear()
        self.clipboard_append(self._snip_current)
        self._snip_status_var.set("Snippet copied to clipboard ✓")

    def _snip_open_file(self):
        """Open the selected snippet file in the system default editor."""
        import os, subprocess, sys
        sel = self._snip_listbox.curselection()
        if not sel or not hasattr(self, "_snip_visible"):
            messagebox.showinfo("Info", "Select a snippet first.")
            return
        pos = sel[0]
        if pos >= len(self._snip_visible):
            return
        _, path = self._snip_files[self._snip_visible[pos]]
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")


    def _build_cfg_tab(self, parent):
        # ── System data ───────────────────────────────────────────────────────
        MAME_SYSTEMS = [
            "Arcade","Atari 2600","Atari 5200","Atari 7800","ColecoVision",
            "Mattel Intellivision","NEC TurboGrafx-16","Nintendo Entertainment System",
            "Nintendo Gameboy","Nintendo Gameboy Color","Nintendo Gameboy Advance",
            "Super Nintendo Entertainment System","Sega Master System","Sega SG-1000",
            "Sega Genesis","Sega 32X","Sega CD","Sony Playstation","SNK Neo Geo",
        ]
        RETROARCH_SYSTEMS = [
            "Arcade","Atari 2600","Atari 5200","Atari 7800","Atari Jaguar",
            "ColecoVision","Mattel Intellivision","NEC TurboGrafx-16",
            "Nintendo Entertainment System","Super Nintendo Entertainment System",
            "Nintendo 64","Nintendo GameCube","Nintendo Wii","Sony Playstation",
            "Sony Playstation 2","SNK Neo Geo","Sega Master System","Sega SG-1000",
            "Sega Genesis","Sega 32X","Sega CD","Sega Dreamcast","Sega Saturn",
            "Sega Naomi","Sammy Atomiswave",
        ]
        OTHER_SYSTEMS = [
            "Nintendo Switch","Nintendo Wii U","PC Games","Sony Playstation 3",
        ]

        MAME_CORES = {
            "Arcade":                             "-skip_gameinfo",
            "Atari 2600":                         "a2600 -cart",
            "Atari 5200":                         "a5200 -cart",
            "Atari 7800":                         "a7800 -cart",
            "ColecoVision":                       "coleco -cart",
            "Mattel Intellivision":               "intv -cart",
            "NEC TurboGrafx-16":                  "tg16 -cart",
            "Nintendo Entertainment System":      "nes -cart",
            "Nintendo Gameboy":                   "gameboy -cart",
            "Nintendo Gameboy Color":             "gbcolor -cart",
            "Nintendo Gameboy Advance":           "gba -cart",
            "Super Nintendo Entertainment System":"snes -cart",
            "Sega Master System":                 "sms -cart",
            "Sega SG-1000":                       "sms -cart",
            "Sega Genesis":                       "genesis -cart",
            "Sega 32X":                           "32x -cart",
            "Sega CD":                            "segacd -cdrom",
            "Sony Playstation":                   "psu -cdrom",
            "SNK Neo Geo":                        "-skip_gameinfo",
        }
        RETROARCH_CORES = {
            "Arcade":                             "mame_libretro.dll",
            "Atari 2600":                         "stella_libretro.dll",
            "Atari 5200":                         "a5200_libretro.dll",
            "Atari 7800":                         "prosystem_libretro.dll",
            "Atari Jaguar":                       "virtualjaguar_libretro.dll",
            "ColecoVision":                       "gearcoleco_libretro.dll",
            "Mattel Intellivision":               "freeintv_libretro.dll",
            "NEC TurboGrafx-16":                  "mednafen_pce_fast_libretro.dll",
            "Nintendo Entertainment System":      "nestopia_libretro.dll",
            "Super Nintendo Entertainment System":"snes9x_libretro.dll",
            "Nintendo 64":                        "parallel_n64_libretro.dll",
            "Nintendo GameCube":                  "dolphin_libretro.dll",
            "Nintendo Wii":                       "dolphin_libretro.dll",
            "Sega Master System":                 "smsplus_libretro.dll",
            "Sega SG-1000":                       "gearsystem_libretro.dll",
            "Sega Genesis":                       "genesis_plus_gx_libretro.dll",
            "Sega 32X":                           "picodrive_libretro.dll",
            "Sega CD":                            "genesis_plus_gx_libretro.dll",
            "Sega Dreamcast":                     "flycast_libretro.dll",
            "Sega Naomi":                         "flycast_libretro.dll",
            "Sammy Atomiswave":                   "flycast_libretro.dll",
            "Sega Saturn":                        "kronos_libretro.dll",
            "Sony Playstation":                   "mednafen_psx_libretro.dll",
            "Sony Playstation 2":                 "pcsx2_libretro.dll",
            "SNK Neo Geo":                        "fbneo_libretro.dll",
        }
        DEFAULT_EXTS = {
            "Arcade":                             ".zip;.7z",
            "SNK Neo Geo":                        ".zip;.7z",
            "Sony Playstation":                   ".chd;.cue;.iso;.pbp",
            "Sony Playstation 2":                 ".iso;.chd;.cso",
            "Sega CD":                            ".chd;.cue;.iso",
            "Sega Dreamcast":                     ".chd;.gdi;.cdi",
            "Sega Naomi":                         ".chd;.gdi;.cdi",
            "Sammy Atomiswave":                   ".chd;.gdi;.cdi",
            "Sega Saturn":                        ".chd;.cue;.iso",
            "Nintendo GameCube":                  ".iso;.gcm;.wbfs;.rvz",
            "Nintendo Wii":                       ".iso;.gcm;.wbfs;.rvz",
            "Nintendo Wii U":                     ".wud;.wux;.rpx;.wad",
            "Nintendo Switch":                    ".xci;.nsp",
            "PC Games":                           ".exe;.lnk;.bat",
            "Sony Playstation 3":                 ".bat",
            "NEC TurboGrafx-16":                  ".pce;.zip;.7z",
            "Nintendo 64":                        ".z64;.n64;.v64;.zip;.7z",
        }
        OTHER_EXEC = {
            "Nintendo Wii U":   (r"$PROGDIR\emulators\cemu\Cemu.exe",  "-f -g"),
            "Nintendo Switch":  (r"$PROGDIR\emulators\Yuzu\yuzu.exe",  "-f -g"),
            "PC Games":         ("cmd",                                  "/c"),
            "Sony Playstation 3":(r"$PROGDIR\emulators\rpcs3\cmd.exe", "/c"),
        }

        # ── State vars ────────────────────────────────────────────────────────
        self._cfg_emu_var    = tk.StringVar(value="MAME")
        self._cfg_sys_var    = tk.StringVar(value=MAME_SYSTEMS[0])
        self._cfg_ext_var    = tk.StringVar(value=".zip;.7z")
        self._cfg_exec_var   = tk.StringVar()
        self._cfg_args_var   = tk.StringVar()
        self._cfg_preview_var= tk.StringVar()

        ARTWORK_SLOTS = ["boxart","cart","cover","disc","fanart","flyer","marquee","snap","wheel"]
        self._cfg_art_vars = {s: tk.BooleanVar(value=False) for s in ARTWORK_SLOTS}

        # ── Layout ────────────────────────────────────────────────────────────
        # Header
        hdr = tk.Frame(parent, bg=COLORS["panel2"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="◈ EMULATOR CFG GENERATOR", bg=COLORS["panel2"],
                 fg=COLORS["accent"], font=("Courier", 10, "bold")).pack(side="left", padx=8, pady=5)
        self._btn(hdr, "💾 Save .cfg", self._cfg_save, small=True).pack(side="right", padx=6, pady=4)

        # Scrollable content area
        outer = tk.Frame(parent, bg=COLORS["panel"])
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=COLORS["panel"], highlightthickness=0)
        sb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=sb.set)
        inner = tk.Frame(canvas, bg=COLORS["panel"])
        win = canvas.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        for w in (canvas, inner):
            w.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
            w.bind("<Button-4>",   lambda e: canvas.yview_scroll(-1, "units"))
            w.bind("<Button-5>",   lambda e: canvas.yview_scroll( 1, "units"))

        def _sep(text):
            f = tk.Frame(inner, bg=COLORS["border"], height=1)
            f.pack(fill="x", padx=8, pady=(10,0))
            tk.Label(inner, text=f" {text} ", bg=COLORS["panel"],
                     fg=COLORS["accent"], font=("Courier", 11, "bold")).pack(anchor="w", padx=10, pady=(0,4))

        def _row(label, widget_fn):
            f = tk.Frame(inner, bg=COLORS["panel"])
            f.pack(fill="x", padx=10, pady=3)
            tk.Label(f, text=label, bg=COLORS["panel"], fg=COLORS["text_dim"],
                     font=("Courier", 11), width=18, anchor="w").pack(side="left")
            widget_fn(f)
            return f

        # ── Emulator ─────────────────────────────────────────────────────────
        _sep("EMULATOR")
        def _make_emu(f):
            cb = ctk.CTkComboBox(f, variable=self._cfg_emu_var,
                                 values=["MAME","RetroArch","Other"],
                                 state="readonly", width=180,
                                 fg_color=COLORS["panel2"],
                                 button_color=COLORS["border"],
                                 dropdown_fg_color=COLORS["panel"],
                                 text_color=COLORS["text"],
                                 font=ctk.CTkFont(family="Courier", size=10),
                                 command=lambda v: _on_emu_change())
            cb.pack(side="left")
        _row("Emulator:", _make_emu)

        # ── System ───────────────────────────────────────────────────────────
        def _make_sys(f):
            self._cfg_sys_cb = ctk.CTkComboBox(f, variable=self._cfg_sys_var,
                                               values=MAME_SYSTEMS,
                                               state="readonly", width=240,
                                               fg_color=COLORS["panel2"],
                                               button_color=COLORS["border"],
                                               dropdown_fg_color=COLORS["panel"],
                                               text_color=COLORS["text"],
                                               font=ctk.CTkFont(family="Courier", size=10),
                                               command=lambda v: _on_sys_change())
            self._cfg_sys_cb.pack(side="left")
        _row("System:", _make_sys)

        # ── ROM Extensions ───────────────────────────────────────────────────
        def _make_ext(f):
            ctk.CTkEntry(f, textvariable=self._cfg_ext_var,
                         fg_color=COLORS["panel2"], text_color=COLORS["text"],
                         border_color=COLORS["border"], width=200, height=28,
                         font=ctk.CTkFont(family="Courier", size=10)).pack(side="left")
        _row("ROM Extensions:", _make_ext)

        # ── Other: exe + args (hidden by default) ────────────────────────────
        _sep("OTHER EMULATOR  (shown when Other is selected)")
        self._cfg_exec_frame = _row("Executable Path:", lambda f:
            ctk.CTkEntry(f, textvariable=self._cfg_exec_var,
                         fg_color=COLORS["panel2"], text_color=COLORS["text"],
                         border_color=COLORS["border"], width=230, height=28,
                         font=ctk.CTkFont(family="Courier", size=10)).pack(side="left"))
        self._cfg_args_frame = _row("Arguments:", lambda f:
            ctk.CTkEntry(f, textvariable=self._cfg_args_var,
                         fg_color=COLORS["panel2"], text_color=COLORS["text"],
                         border_color=COLORS["border"], width=230, height=28,
                         font=ctk.CTkFont(family="Courier", size=10)).pack(side="left"))

        # ── Logic callbacks ───────────────────────────────────────────────────
        def _update_preview(*_):
            if hasattr(self, "_cfg_preview"):
                self._cfg_preview.config(state="normal")
                self._cfg_preview.delete("1.0", tk.END)
                self._cfg_preview.insert("1.0", self._cfg_build())
                self._cfg_preview.config(state="disabled")

        def _on_sys_change():
            sys = self._cfg_sys_var.get()
            self._cfg_ext_var.set(DEFAULT_EXTS.get(sys, ".zip;.7z"))
            if self._cfg_emu_var.get() == "Other" and sys in OTHER_EXEC:
                exe, args = OTHER_EXEC[sys]
                self._cfg_exec_var.set(exe)
                self._cfg_args_var.set(args)
            _update_preview()

        def _on_emu_change():
            emu = self._cfg_emu_var.get()
            if emu == "MAME":
                self._cfg_sys_cb.configure(values=MAME_SYSTEMS)
                self._cfg_sys_var.set(MAME_SYSTEMS[0])
                self._cfg_exec_frame.pack_forget()
                self._cfg_args_frame.pack_forget()
            elif emu == "RetroArch":
                self._cfg_sys_cb.configure(values=RETROARCH_SYSTEMS)
                self._cfg_sys_var.set(RETROARCH_SYSTEMS[0])
                self._cfg_exec_frame.pack_forget()
                self._cfg_args_frame.pack_forget()
            else:
                self._cfg_sys_cb.configure(values=OTHER_SYSTEMS)
                self._cfg_sys_var.set(OTHER_SYSTEMS[0])
                self._cfg_exec_frame.pack(fill="x", padx=10, pady=3,
                                          before=self._cfg_args_frame)
                self._cfg_args_frame.pack(fill="x", padx=10, pady=3)
            _on_sys_change()

        # Trace ext and exec/args for live preview
        self._cfg_ext_var.trace_add("write",  lambda *a: _update_preview())
        self._cfg_exec_var.trace_add("write", lambda *a: _update_preview())
        self._cfg_args_var.trace_add("write", lambda *a: _update_preview())

        # ── Artwork checkboxes ───────────────────────────────────────────────
        _sep("ARTWORK FOLDERS")
        art_frame = tk.Frame(inner, bg=COLORS["panel"])
        art_frame.pack(fill="x", padx=10, pady=4)
        for i, slot in enumerate(ARTWORK_SLOTS):
            col = i % 3
            row = i // 3
            ctk.CTkCheckBox(art_frame, text=slot.capitalize(),
                             variable=self._cfg_art_vars[slot],
                             text_color=COLORS["text"],
                             fg_color=COLORS["accent"],
                             hover_color=COLORS["accent"],
                             font=ctk.CTkFont(family="Courier", size=11),
                             command=_update_preview).grid(
                                 row=row, column=col, sticky="w", padx=12, pady=2)

        # ── Select All / None buttons ─────────────────────────────────────────
        art_btn_row = tk.Frame(inner, bg=COLORS["panel"])
        art_btn_row.pack(anchor="w", padx=10, pady=(0, 4))
        self._btn(art_btn_row, "All",
                  lambda: [v.set(True) for v in self._cfg_art_vars.values()] or _update_preview(),
                  small=True).pack(side="left", padx=4)
        self._btn(art_btn_row, "None",
                  lambda: [v.set(False) for v in self._cfg_art_vars.values()] or _update_preview(),
                  small=True).pack(side="left", padx=2)

        # ── Preview ──────────────────────────────────────────────────────────
        _sep("PREVIEW")
        prev_sb_y = tk.Scrollbar(inner, orient="vertical")
        prev_sb_y.pack(side="right", fill="y", padx=(0, 8))
        prev_sb_x = tk.Scrollbar(inner, orient="horizontal")
        prev_sb_x.pack(side="bottom", fill="x", padx=8)
        self._cfg_preview = tk.Text(inner, bg="#0d1117", fg="#00ff88",
                                    font=("Courier", 11), relief="flat",
                                    wrap="none", bd=0, padx=8, pady=6,
                                    height=16,
                                    yscrollcommand=prev_sb_y.set,
                                    xscrollcommand=prev_sb_x.set,
                                    state="disabled")
        self._cfg_preview.pack(fill="x", padx=8, pady=(0, 8))
        prev_sb_y.config(command=self._cfg_preview.yview)
        prev_sb_x.config(command=self._cfg_preview.xview)

        # ── Status ───────────────────────────────────────────────────────────
        self._cfg_status_var = tk.StringVar(value="Ready — configure and click Save .cfg")
        tk.Label(parent, textvariable=self._cfg_status_var,
                 bg=COLORS["panel2"], fg=COLORS["text_dim"],
                 font=("Courier", 11), anchor="w", padx=6).pack(fill="x", side="bottom")

        # Initial hide of Other fields and preview render
        self._cfg_exec_frame.pack_forget()
        self._cfg_args_frame.pack_forget()
        _update_preview()

    # ── CFG helpers ───────────────────────────────────────────────────────────

    def _cfg_build(self):
        MAME_CORES = {
            "Arcade":"-skip_gameinfo","Atari 2600":"a2600 -cart","Atari 5200":"a5200 -cart",
            "Atari 7800":"a7800 -cart","ColecoVision":"coleco -cart",
            "Mattel Intellivision":"intv -cart","NEC TurboGrafx-16":"tg16 -cart",
            "Nintendo Entertainment System":"nes -cart","Nintendo Gameboy":"gameboy -cart",
            "Nintendo Gameboy Color":"gbcolor -cart","Nintendo Gameboy Advance":"gba -cart",
            "Super Nintendo Entertainment System":"snes -cart","Sega Master System":"sms -cart",
            "Sega SG-1000":"sms -cart","Sega Genesis":"genesis -cart","Sega 32X":"32x -cart",
            "Sega CD":"segacd -cdrom","Sony Playstation":"psu -cdrom","SNK Neo Geo":"-skip_gameinfo",
        }
        RETROARCH_CORES = {
            "Arcade":"mame_libretro.dll","Atari 2600":"stella_libretro.dll",
            "Atari 5200":"a5200_libretro.dll","Atari 7800":"prosystem_libretro.dll",
            "Atari Jaguar":"virtualjaguar_libretro.dll","ColecoVision":"gearcoleco_libretro.dll",
            "Mattel Intellivision":"freeintv_libretro.dll",
            "NEC TurboGrafx-16":"mednafen_pce_fast_libretro.dll",
            "Nintendo Entertainment System":"nestopia_libretro.dll",
            "Super Nintendo Entertainment System":"snes9x_libretro.dll",
            "Nintendo 64":"parallel_n64_libretro.dll","Nintendo GameCube":"dolphin_libretro.dll",
            "Nintendo Wii":"dolphin_libretro.dll","Sega Master System":"smsplus_libretro.dll",
            "Sega SG-1000":"gearsystem_libretro.dll","Sega Genesis":"genesis_plus_gx_libretro.dll",
            "Sega 32X":"picodrive_libretro.dll","Sega CD":"genesis_plus_gx_libretro.dll",
            "Sega Dreamcast":"flycast_libretro.dll","Sega Naomi":"flycast_libretro.dll",
            "Sammy Atomiswave":"flycast_libretro.dll","Sega Saturn":"kronos_libretro.dll",
            "Sony Playstation":"mednafen_psx_libretro.dll","Sony Playstation 2":"pcsx2_libretro.dll",
            "SNK Neo Geo":"fbneo_libretro.dll",
        }

        emu  = self._cfg_emu_var.get()
        sys  = self._cfg_sys_var.get()
        ext  = self._cfg_ext_var.get()
        exe  = self._cfg_exec_var.get()
        args = self._cfg_args_var.get()

        lines = []
        lines.append("# Generated by Attract-Mode Plus CFG Generator")
        lines.append("#")

        if emu == "MAME":
            core = MAME_CORES.get(sys, "")
            lines.append(r"executable           $PROGDIR\emulators\mame\mame.exe")
            lines.append(f'args                 {core} "[romfilename]"')
        elif emu == "RetroArch":
            core = RETROARCH_CORES.get(sys, "")
            lines.append(r"executable           $PROGDIR\emulators\RetroArch-Win64\retroarch.exe")
            lines.append(f'args                 -L cores\\{core} "[romfilename]"')
        else:
            lines.append(f"executable           {exe}")
            lines.append(f'args                 {args} "[romfilename]"')

        lines.append(f"rompath              $PROGDIR\\collections\\{sys}\\roms\\")
        lines.append(f"romext               {ext}")
        lines.append(f"system               {sys}")
        lines.append("info_source          thegamesdb.net")
        lines.append("exit_hotkey          Joy0 Button6+Joy0 Button7")

        art_lines = []
        for slot, var in self._cfg_art_vars.items():
            if var.get():
                art_lines.append(f"artwork    {slot:<16}collections\\{sys}\\{slot}")
        if art_lines:
            lines.append("")
            lines.extend(art_lines)

        return "\n".join(lines)

    def _cfg_save(self):
        emu = self._cfg_emu_var.get()
        sys = self._cfg_sys_var.get()
        exe = self._cfg_exec_var.get()
        args = self._cfg_args_var.get()

        if emu == "Other" and (not exe or not args):
            messagebox.showerror("Missing Fields",
                "Please fill in both Executable Path and Arguments for Other emulator.")
            return

        default_name = sys.replace(" ", "_") + ".cfg"
        path = filedialog.asksaveasfilename(
            title="Save Emulator CFG",
            defaultextension=".cfg",
            initialfile=default_name,
            filetypes=[("CFG Files", "*.cfg"), ("All Files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self._cfg_build())
            self._cfg_status_var.set(f"Saved  —  {path}")
            messagebox.showinfo("Saved", f"Config saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))


    def _build_romlist_tab(self, parent):
        self._rom_current_file = ""
        self._rom_header = []

        # ── Toolbar ──────────────────────────────────────────────────────────
        toolbar = tk.Frame(parent, bg=COLORS["panel2"])
        toolbar.pack(fill="x", padx=0, pady=0)

        tk.Label(toolbar, text="◈ ROMLIST EDITOR", bg=COLORS["panel2"],
                 fg=COLORS["accent"], font=("Courier", 10, "bold")).pack(side="left", padx=8, pady=5)

        for txt, cmd, col in [
            ("📂 Open",    self._rom_open,      None),
            ("💾 Save",    self._rom_save,      None),
            ("💾 Save As", self._rom_save_as,   None),
            ("✎ Bulk Edit",self._rom_bulk_edit, None),
            ("+ Add Row",  self._rom_add_row,   None),
            ("✕ Del Row",  self._rom_del_row,   "#4a2020"),
        ]:
            self._btn(toolbar, txt, cmd, color=col, small=True).pack(side="left", padx=3, pady=4)

        # ── File label ───────────────────────────────────────────────────────
        self._rom_file_var = tk.StringVar(value="No file loaded")
        tk.Label(parent, textvariable=self._rom_file_var,
                 bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 11), anchor="w").pack(fill="x", padx=8, pady=(4, 0))

        # ── Header display ───────────────────────────────────────────────────
        hf = tk.Frame(parent, bg=COLORS["panel"])
        hf.pack(fill="x", padx=6, pady=(2, 4))
        tk.Label(hf, text="Header:", bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier", 11)).pack(side="left")
        self._rom_header_var = tk.StringVar(value="")
        ctk.CTkEntry(hf, textvariable=self._rom_header_var, state="disabled",
                     fg_color=COLORS["panel2"], text_color=COLORS["text_dim"],
                     border_color=COLORS["border"], height=22,
                     font=ctk.CTkFont(family="Courier", size=11)).pack(
                         side="left", fill="x", expand=True, padx=4)

        # ── Search bar ───────────────────────────────────────────────────────
        sf = tk.Frame(parent, bg=COLORS["panel2"])
        sf.pack(fill="x", padx=6, pady=(0, 4))
        tk.Label(sf, text="🔍", bg=COLORS["panel2"], fg=COLORS["text_dim"],
                 font=("Courier", 11)).pack(side="left", padx=4)
        self._rom_search_var = tk.StringVar()
        ctk.CTkEntry(sf, textvariable=self._rom_search_var,
                     fg_color=COLORS["panel2"], text_color=COLORS["text"],
                     border_color=COLORS["border"], height=24,
                     font=ctk.CTkFont(family="Courier", size=11)).pack(
                         side="left", fill="x", expand=True, pady=3)
        ctk.CTkButton(sf, text="✕", width=24, height=22,
                       fg_color=COLORS["panel2"], hover_color=COLORS["border"],
                       text_color=COLORS["text_dim"],
                       font=ctk.CTkFont(family="Courier", size=11),
                       command=lambda: self._rom_search_var.set("")).pack(side="right", padx=4)
        self._rom_search_var.trace_add("write", lambda *a: self._rom_apply_search())

        # ── Treeview table (no CTK equivalent — kept as ttk) ─────────────────
        tree_frame = tk.Frame(parent, bg=COLORS["panel"])
        tree_frame.pack(fill="both", expand=True, padx=6, pady=(0, 2))

        tree_sb_y = tk.Scrollbar(tree_frame, orient="vertical")
        tree_sb_y.pack(side="right", fill="y")
        tree_sb_x = tk.Scrollbar(tree_frame, orient="horizontal")
        tree_sb_x.pack(side="bottom", fill="x")

        self._rom_tree = ttk.Treeview(tree_frame, show="headings",
                                       selectmode="browse",
                                       style="Rom.Treeview",
                                       yscrollcommand=tree_sb_y.set,
                                       xscrollcommand=tree_sb_x.set)
        self._rom_tree.pack(fill="both", expand=True)
        tree_sb_y.config(command=self._rom_tree.yview)
        tree_sb_x.config(command=self._rom_tree.xview)

        self._rom_tree.bind("<Double-1>", self._rom_on_double_click)
        self._rom_tree.bind("<Button-3>", self._rom_on_right_click)

        # ── Context menu ─────────────────────────────────────────────────────
        self._rom_ctx = tk.Menu(self, tearoff=0,
                                bg=COLORS["panel"], fg=COLORS["text"],
                                activebackground=COLORS["border"],
                                activeforeground=COLORS["accent"])
        self._rom_ctx.add_command(label="✎ Edit Cell",        command=self._rom_edit_via_ctx)
        self._rom_ctx.add_command(label="✎ Bulk Edit Column", command=self._rom_bulk_edit_col_ctx)
        self._rom_ctx.add_separator()
        self._rom_ctx.add_command(label="+ Add Row",          command=self._rom_add_row)
        self._rom_ctx.add_command(label="✕ Delete Row",       command=self._rom_del_row)

        # ── Status bar ───────────────────────────────────────────────────────
        self._rom_status_var = tk.StringVar(value="Ready  —  open a .txt or .lst romlist file")
        tk.Label(parent, textvariable=self._rom_status_var,
                 bg=COLORS["panel2"], fg=COLORS["text_dim"],
                 font=("Courier", 11), anchor="w", padx=6).pack(fill="x", side="bottom")

    # ── Romlist helpers ───────────────────────────────────────────────────────

    def _rom_open(self):
        path = filedialog.askopenfilename(
            title="Open Romlist File",
            filetypes=[("Romlist Files", "*.txt *.lst"), ("All Files", "*.*")]
        )
        if path:
            self._rom_load(path)

    def _rom_load(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if not lines:
                messagebox.showwarning("Empty File", "That file appears to be empty.")
                return

            # Clear tree
            self._rom_tree.delete(*self._rom_tree.get_children())

            # Parse header
            self._rom_header = lines[0].strip().split(";")
            self._rom_header_var.set(lines[0].strip())
            self._rom_tree["columns"] = self._rom_header
            for col in self._rom_header:
                self._rom_tree.heading(col, text=col,
                    command=lambda c=col: self._rom_sort_by(c, False))
                self._rom_tree.column(col, width=110, minwidth=50, stretch=True)

            # Load rows — store full data list for search filtering
            self._rom_all_rows = []
            for line in lines[1:]:
                line = line.strip()
                if line:
                    row = line.split(";")
                    self._rom_all_rows.append(row)
                    self._rom_tree.insert("", "end", values=row)

            self._rom_current_file = path
            self._rom_file_var.set(f"File: {path}")
            count = len(self._rom_all_rows)
            self._rom_status_var.set(f"Loaded {count} entries  —  {path}")

        except Exception as e:
            messagebox.showerror("Load Error", str(e))
            self._rom_status_var.set("Load failed")

    def _rom_save(self):
        if not self._rom_current_file:
            self._rom_save_as()
        else:
            self._rom_write(self._rom_current_file)

    def _rom_save_as(self):
        path = filedialog.asksaveasfilename(
            title="Save Romlist As",
            defaultextension=".txt",
            filetypes=[("Romlist Files", "*.txt *.lst"), ("All Files", "*.*")]
        )
        if path:
            self._rom_write(path)

    def _rom_write(self, path):
        try:
            rows = [";".join(self._rom_header)]
            for item in self._rom_tree.get_children():
                vals = self._rom_tree.item(item)["values"]
                rows.append(";".join(str(v) for v in vals))
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(rows))
            self._rom_current_file = path
            self._rom_file_var.set(f"File: {path}")
            self._rom_status_var.set(f"Saved  —  {path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def _rom_on_double_click(self, event):
        region = self._rom_tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        item = self._rom_tree.identify_row(event.y)
        col  = self._rom_tree.identify_column(event.x)
        if not item:
            return
        self._rom_edit_cell(item, col)

    def _rom_on_right_click(self, event):
        row = self._rom_tree.identify_row(event.y)
        col = self._rom_tree.identify_column(event.x)
        if row:
            self._rom_tree.selection_set(row)
        self._rom_ctx_col = col
        self._rom_ctx.tk_popup(event.x_root, event.y_root)

    def _rom_edit_via_ctx(self):
        sel = self._rom_tree.selection()
        if sel and hasattr(self, "_rom_ctx_col"):
            self._rom_edit_cell(sel[0], self._rom_ctx_col)

    def _rom_edit_cell(self, item, col):
        from tkinter import simpledialog
        col_idx = int(col.replace("#", "")) - 1
        if col_idx >= len(self._rom_header):
            return
        col_name = self._rom_header[col_idx]
        cur_val  = self._rom_tree.item(item)["values"][col_idx]

        # Inline edit popup near the cell
        bbox = self._rom_tree.bbox(item, col)
        if not bbox:
            new_val = simpledialog.askstring(
                "Edit Cell", f"{col_name}:", initialvalue=str(cur_val))
            if new_val is not None:
                vals = list(self._rom_tree.item(item)["values"])
                vals[col_idx] = new_val
                self._rom_tree.item(item, values=vals)
            return

        x, y, w, h = bbox
        # Map bbox from treeview coords to screen, accounting for the tab widget
        abs_x = self._rom_tree.winfo_rootx() + x
        abs_y = self._rom_tree.winfo_rooty() + y

        popup = ctk.CTkToplevel(self)
        popup.wm_overrideredirect(True)
        popup.geometry(f"{max(w, 180)}x{h + 4}+{abs_x}+{abs_y}")
        popup.attributes("-topmost", True)

        var = tk.StringVar(value=str(cur_val))
        entry = ctk.CTkEntry(popup, textvariable=var,
                              fg_color=COLORS["panel2"], text_color=COLORS["text"],
                              border_color=COLORS["accent"], border_width=1,
                              font=ctk.CTkFont(family="Courier", size=11))
        entry.pack(fill="both", expand=True)
        entry._entry.select_range(0, tk.END)
        entry._entry.focus_set()

        def _commit(e=None):
            vals = list(self._rom_tree.item(item)["values"])
            vals[col_idx] = var.get()
            self._rom_tree.item(item, values=vals)
            popup.destroy()
            self._rom_status_var.set(f"Updated {col_name}")

        def _cancel(e=None):
            popup.destroy()

        entry._entry.bind("<Return>",   _commit)
        entry._entry.bind("<Tab>",      _commit)
        entry._entry.bind("<Escape>",   _cancel)
        entry._entry.bind("<FocusOut>", _cancel)

    def _rom_bulk_edit(self):
        if not self._rom_header:
            messagebox.showinfo("Info", "Open a romlist file first.")
            return
        self._rom_bulk_edit_dialog(None)

    def _rom_bulk_edit_col_ctx(self):
        if hasattr(self, "_rom_ctx_col"):
            col_idx = int(self._rom_ctx_col.replace("#", "")) - 1
            if col_idx < len(self._rom_header):
                self._rom_bulk_edit_dialog(self._rom_header[col_idx])

    def _rom_bulk_edit_dialog(self, preselect_col):
        from tkinter import simpledialog
        win = ctk.CTkToplevel(self)
        win.title("Bulk Edit Column")
        win.geometry("360x160")
        win.transient(self)
        win.grab_set()

        ctk.CTkLabel(win, text="◈ BULK EDIT COLUMN",
                      text_color=COLORS["accent"],
                      font=ctk.CTkFont(family="Courier", size=10, weight="bold")).pack(
                          anchor="w", padx=12, pady=(12, 4))

        tf = tk.Frame(win, bg=COLORS["bg"])
        tf.pack(fill="x", padx=12)
        tk.Label(tf, text="Column:", bg=COLORS["bg"], fg=COLORS["text_dim"],
                 font=("Courier", 11), width=10, anchor="w").pack(side="left")
        col_var = tk.StringVar(value=preselect_col or (self._rom_header[0] if self._rom_header else ""))
        ctk.CTkComboBox(tf, variable=col_var, values=self._rom_header,
                         state="readonly", width=200,
                         fg_color=COLORS["panel2"], button_color=COLORS["border"],
                         dropdown_fg_color=COLORS["panel"], text_color=COLORS["text"],
                         font=ctk.CTkFont(family="Courier", size=11)).pack(side="left", padx=4)

        vf = tk.Frame(win, bg=COLORS["bg"])
        vf.pack(fill="x", padx=12, pady=6)
        tk.Label(vf, text="New value:", bg=COLORS["bg"], fg=COLORS["text_dim"],
                 font=("Courier", 11), width=10, anchor="w").pack(side="left")
        val_var = tk.StringVar()
        ctk.CTkEntry(vf, textvariable=val_var,
                      fg_color=COLORS["panel2"], text_color=COLORS["text"],
                      border_color=COLORS["border"], width=200, height=28,
                      font=ctk.CTkFont(family="Courier", size=11)).pack(side="left", padx=4)

        def _apply():
            col_name = col_var.get()
            new_val  = val_var.get()
            if col_name not in self._rom_header:
                return
            col_idx = self._rom_header.index(col_name)
            for item in self._rom_tree.get_children():
                vals = list(self._rom_tree.item(item)["values"])
                if col_idx < len(vals):
                    vals[col_idx] = new_val
                    self._rom_tree.item(item, values=vals)
            count = len(self._rom_tree.get_children())
            self._rom_status_var.set(f"Bulk updated '{col_name}' for {count} rows")
            win.destroy()

        bf = tk.Frame(win, bg=COLORS["bg"])
        bf.pack(pady=8)
        self._btn(bf, "✓ Apply",  _apply,      small=True).pack(side="left", padx=6)
        self._btn(bf, "✕ Cancel", win.destroy, small=True).pack(side="left", padx=6)

    def _rom_add_row(self):
        if not self._rom_header:
            messagebox.showinfo("Info", "Open a romlist file first.")
            return
        empty = [""] * len(self._rom_header)
        self._rom_tree.insert("", "end", values=empty)
        # Select and scroll to new row
        new_item = self._rom_tree.get_children()[-1]
        self._rom_tree.selection_set(new_item)
        self._rom_tree.see(new_item)
        count = len(self._rom_tree.get_children())
        self._rom_status_var.set(f"Added empty row  —  {count} total entries")

    def _rom_del_row(self):
        sel = self._rom_tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Select a row to delete.")
            return
        if messagebox.askyesno("Delete Row", "Delete the selected row?"):
            self._rom_tree.delete(sel[0])
            count = len(self._rom_tree.get_children())
            self._rom_status_var.set(f"Row deleted  —  {count} total entries")

    def _rom_apply_search(self):
        query = self._rom_search_var.get().strip().lower()
        self._rom_tree.delete(*self._rom_tree.get_children())
        if not hasattr(self, "_rom_all_rows"):
            return
        count = 0
        for row in self._rom_all_rows:
            if not query or any(query in str(v).lower() for v in row):
                self._rom_tree.insert("", "end", values=row)
                count += 1
        self._rom_status_var.set(
            f"Showing {count} of {len(self._rom_all_rows)} entries"
            + (f"  —  filter: \"{query}\"" if query else ""))

    def _rom_sort_by(self, col, reverse):
        items = [(self._rom_tree.set(k, col), k)
                 for k in self._rom_tree.get_children("")]
        try:
            items.sort(key=lambda t: t[0].lower(), reverse=reverse)
        except Exception:
            items.sort(reverse=reverse)
        for idx, (_, k) in enumerate(items):
            self._rom_tree.move(k, "", idx)
        col_idx = self._rom_header.index(col) if col in self._rom_header else 0
        self._rom_tree.heading(col, text=col + (" ▲" if not reverse else " ▼"),
            command=lambda c=col: self._rom_sort_by(c, not reverse))
        self._rom_status_var.set(f"Sorted by '{col}' {'▲' if not reverse else '▼'}")


    def _build_reference_tab(self, parent):
        REFERENCE = {
            "AM+ fe.* API": [
                ("fe.layout.width / height",
                 "Set the base layout resolution.\n\nfe.layout.width  = 1920;\nfe.layout.height = 1080;\nlocal flw = fe.layout.width;\nlocal flh = fe.layout.height;"),
                ("fe.add_artwork(name,x,y,w,h)",
                 "Add artwork image. name = art slot (snap,wheel,boxart,marquee,flyer,fanart).\n\nlocal snap = fe.add_artwork(\"snap\", 0, 0, flw/2, flh/2);\nsnap.preserve_aspect_ratio = true;"),
                ("fe.add_text(str,x,y,w,h)",
                 "Add a text label. Supports magic tokens.\n\nlocal title = fe.add_text(\"[Title]\", 0, flh*9/10, flw, flh/10);\ntitle.align = Align.Centre;\ntitle.char_size = 32;"),
                ("fe.add_image(file,x,y,w,h)",
                 "Add a static image file.\n\nlocal bg = fe.add_image(\"bg.png\", 0, 0, flw, flh);"),
                ("fe.add_surface(w,h)",
                 "Add an offscreen render surface.\n\nlocal surf = fe.add_surface(flw/2, flh/2);\nsurf.x = flw/4;\nsurf.y = flh/4;"),
                ("fe.add_sound(file)",
                 "Add a sound effect.\n\nlocal snd = fe.add_sound(\"click.ogg\");\nsnd.playing = true;"),
                ("fe.add_shader(type,...)",
                 "Add a GLSL shader.\n\nlocal sh = fe.add_shader(Shader.VertexAndFragment,\n    \"vert.glsl\", \"frag.glsl\");\nmy_art.shader = sh;"),
                ("fe.load_module(file)",
                 "Load an AM+ module (.nut file).\n\nfe.load_module(\"animate.nut\");\nfe.load_module(\"conveyor.nut\");"),
                ("fe.add_transition_callback(fn)",
                 "Register a function called on screen transitions.\n\nfe.add_transition_callback(\"on_transition\");\nfunction on_transition(ttype, var, ttime) {\n    return false;\n}"),
                ("fe.add_signal_handler(fn)",
                 "Register a function to handle user input.\n\nfe.add_signal_handler(\"on_signal\");\nfunction on_signal(sig) {\n    if (sig == \"select\") { /* do thing */ }\n    return false;\n}"),
                ("fe.game_info(id, offset)",
                 "Get info about a game in the list.\n\nlocal title = fe.game_info(Info.Title);\nlocal year  = fe.game_info(Info.Year, 1);"),
                ("fe.get_input_state(sig)",
                 "Check if an input signal is active.\n\nif (fe.get_input_state(\"up\")) { /* ... */ }"),
                ("fe.list.size / index / name",
                 "Current list properties.\n\nlocal total = fe.list.size;\nlocal cur   = fe.list.index;\nlocal name  = fe.list.name;"),
            ],
            "AM+ Object Properties": [
                ("x, y, width, height",
                 "Position and size of any fe object.\n\nobj.x = flw/4;\nobj.y = flh/4;\nobj.width  = flw/2;\nobj.height = flh/2;"),
                ("alpha (0-255)",
                 "Transparency. 0=invisible, 255=fully opaque.\n\nobj.alpha = 180;"),
                ("rotation",
                 "Rotation in degrees (clockwise).\n\nobj.rotation = 45.0;"),
                ("visible",
                 "Show or hide the object.\n\nobj.visible = false;"),
                ("blend_mode",
                 "Blend mode for rendering.\n\nobj.blend_mode = BlendMode.Alpha;\n// Options: None Alpha Premult Add Screen Multiply"),
                ("preserve_aspect_ratio",
                 "Keep artwork proportions when scaling.\n\nobj.preserve_aspect_ratio = true;"),
                ("set_rgb(r,g,b)",
                 "Set tint colour (0-255 per channel).\n\nobj.set_rgb(255, 128, 0);"),
                ("set_pos(x,y,w,h)",
                 "Shorthand to set position and size.\n\nobj.set_pos(flw/4, flh/4, flw/2, flh/2);"),
                ("char_size (text only)",
                 "Font size for text objects.\n\ntxt.char_size = 28;"),
                ("align (text only)",
                 "Text alignment.\n\ntxt.align = Align.Centre;\n// Align.Left  Align.Centre  Align.Right"),
                ("msg (text only)",
                 "Override the text string at runtime.\n\ntxt.msg = \"Now Playing\";"),
            ],
            "AM+ Enums & Constants": [
                ("Align.*",
                 "Text alignment constants.\n\nAlign.Left\nAlign.Centre\nAlign.Right"),
                ("BlendMode.*",
                 "Blend mode constants.\n\nBlendMode.None\nBlendMode.Alpha\nBlendMode.Premult\nBlendMode.Add\nBlendMode.Screen\nBlendMode.Multiply"),
                ("Transition.*",
                 "Transition trigger types.\n\nTransition.ToNewSelection\nTransition.FromOldSelection\nTransition.EndNavigation\nTransition.StartLayout\nTransition.EndLayout\nTransition.ScreenSaver"),
                ("Tween.*",
                 "Animation easing types (animate module).\n\nTween.Linear\nTween.QuadIn    Tween.QuadOut    Tween.QuadInOut\nTween.CubicIn   Tween.CubicOut   Tween.CubicInOut\nTween.SineIn    Tween.SineOut    Tween.SineInOut\nTween.Bounce    Tween.Elastic"),
                ("Info.*",
                 "Game info field constants for fe.game_info().\n\nInfo.Title        Info.Year\nInfo.Manufacturer Info.CloneOf\nInfo.Players      Info.Category\nInfo.Rating       Info.PlayedTime\nInfo.PlayedCount  Info.System\nInfo.Overview     Info.Buttons"),
                ("Shader.*",
                 "Shader type constants.\n\nShader.VertexAndFragment\nShader.Vertex\nShader.Fragment\nShader.Empty"),
            ],
            "AM+ Magic Tokens": [
                ("[Title] [Year] [Manufacturer]",
                 "Common game info tokens for text strings.\n\nlocal t = fe.add_text(\"[Title] ([Year])\", 0, 0, flw, 60);"),
                ("[Players] [Category] [Rating]",
                 "More game info tokens.\n\nlocal t = fe.add_text(\"Players: [Players]\", 0, 60, flw, 40);"),
                ("[System] [Overview]",
                 "System name and game description.\n\nlocal t = fe.add_text(\"[System]\", 0, 0, flw, 40);"),
                ("[PlayedCount] [PlayedTime]",
                 "Play statistics tokens.\n\nlocal t = fe.add_text(\"Played: [PlayedCount]x\", 0, 0, 300, 40);"),
                ("[!strftime_format]",
                 "Live clock using C strftime format.\n\nlocal clk = fe.add_text(\"[!%H:%M]\", flw-120, 10, 110, 40);\nclk.align = Align.Right;"),
                ("[ListSize] [ListEntry] [ListFilterName]",
                 "List navigation tokens.\n\nlocal t = fe.add_text(\"[ListEntry] / [ListSize]\", 0, 0, 200, 40);"),
            ],
            "Squirrel: Variables & Types": [
                ("local",
                 "Declare a local variable.\n\nlocal x = 10;\nlocal name = \"hello\";\nlocal flag = true;\nlocal nothing = null;"),
                ("Integer / Float",
                 "Numeric types.\n\nlocal i = 42;\nlocal h = 0xFF;\nlocal f = 3.14;\nlocal e = 1.0e2;"),
                ("String",
                 "String literals and verbatim strings.\n\nlocal s = \"Hello\\n\";\nlocal v = @\"verbatim no escape\";\nlocal c = \"line1\\nline2\";"),
                ("Table  { }",
                 "Key-value associative container.\n\nlocal t = { a = 1, b = \"two\" };\nt.c <- 3;\nprint(t.a);\ndelete t.b;"),
                ("Array  [ ]",
                 "Ordered list, zero-indexed.\n\nlocal a = [10, 20, 30];\nprint(a[0]);\na.push(40);\nforeach (i, v in a) print(i + \":\" + v + \"\\n\");"),
                ("typeof",
                 "Get the type of a value as a string.\n\nprint(typeof 42);       // integer\nprint(typeof \"hello\");  // string\nprint(typeof {});       // table"),
            ],
            "Squirrel: Control Flow": [
                ("if / else",
                 "Conditional branching.\n\nif (x > 0) {\n    print(\"positive\\n\");\n} else if (x < 0) {\n    print(\"negative\\n\");\n} else {\n    print(\"zero\\n\");\n}"),
                ("while",
                 "Loop while condition is true.\n\nlocal i = 0;\nwhile (i < 10) {\n    print(i + \"\\n\");\n    i++;\n}"),
                ("for",
                 "C-style for loop.\n\nfor (local i = 0; i < 10; i++) {\n    print(i + \"\\n\");\n}"),
                ("foreach",
                 "Iterate over array, table, string or generator.\n\nlocal arr = [1, 2, 3];\nforeach (idx, val in arr) {\n    print(idx + \" = \" + val + \"\\n\");\n}"),
                ("switch / case",
                 "Multi-branch switch.\n\nswitch (val) {\n    case 1:  print(\"one\\n\");   break;\n    case 2:  print(\"two\\n\");   break;\n    default: print(\"other\\n\"); break;\n}"),
                ("try / catch / throw",
                 "Exception handling.\n\ntry {\n    throw \"something went wrong\";\n} catch (e) {\n    print(\"caught: \" + e + \"\\n\");\n}"),
                ("break / continue",
                 "Loop control statements.\n\nfor (local i=0; i<10; i++) {\n    if (i == 3) continue;\n    if (i == 7) break;\n    print(i + \"\\n\");\n}"),
            ],
            "Squirrel: Functions & Classes": [
                ("function declaration",
                 "Define a named function.\n\nfunction add(a, b) {\n    return a + b;\n}\nprint(add(3, 4));"),
                ("anonymous / lambda",
                 "Inline function expressions.\n\nlocal sq = function(x) { return x * x; };\nlocal sq2 = @(x) x * x;\nprint(sq(5));\nprint(sq2(5));"),
                ("class declaration",
                 "Define a class with constructor.\n\nclass Animal {\n    name = null;\n    constructor(n) { name = n; }\n    function speak() { print(name + \"\\n\"); }\n}\nlocal a = Animal(\"Cat\");\na.speak();"),
                ("extends (inheritance)",
                 "Inherit from a base class.\n\nclass Dog extends Animal {\n    constructor(n) { base.constructor(n); }\n    function speak() { print(name + \" barks\\n\"); }\n}\nlocal d = Dog(\"Rex\");\nd.speak();"),
                ("varargs  ...",
                 "Variable argument functions.\n\nfunction sum(...) {\n    local total = 0;\n    foreach (v in vargv) total += v;\n    return total;\n}\nprint(sum(1, 2, 3, 4));"),
            ],
            "Squirrel: Built-in Functions": [
                ("print / error",
                 "Output text to stdout / stderr.\n\nprint(\"hello\\n\");\nerror(\"oops\\n\");"),
                ("string methods",
                 "Common string operations.\n\nlocal s = \"Hello World\";\nprint(s.len());           // 11\nprint(s.tolower());       // hello world\nprint(s.toupper());       // HELLO WORLD\nprint(s.slice(0, 5));     // Hello\nprint(s.find(\"World\"));   // 6\nprint(s.gsub(\"o\",\"0\"));   // Hell0 W0rld"),
                ("array methods",
                 "Common array operations.\n\nlocal a = [3, 1, 2];\na.push(4);\na.pop();\na.insert(0, 0);\na.remove(1);\na.sort();\nprint(a.len());"),
                ("math functions",
                 "Math built-ins.\n\nlocal pi = PI;\nprint(sin(1.0));\nprint(cos(0.0));\nprint(sqrt(16.0));\nprint(pow(2.0, 8.0));\nprint(abs(-5));\nprint(floor(3.7));\nprint(ceil(3.2));\nprint(rand() % 100);"),
                ("format",
                 "C-style string formatting.\n\nlocal s = format(\"%d items at $%.2f\", 3, 1.5);\nprint(s);"),
                ("clock / time",
                 "Timing functions.\n\nlocal t = clock();\nlocal ts = time();"),
            ],
        }

        # ── UI ──────────────────────────────────────────────────────────────
        ctk.CTkLabel(parent, text="◈ SQUIRREL & AM+ REFERENCE",
                      text_color=COLORS["accent"],
                      font=ctk.CTkFont(family="Courier", size=10, weight="bold")).pack(
                          anchor="w", padx=8, pady=(8, 2))

        # Search bar
        sf = tk.Frame(parent, bg=COLORS["panel2"])
        sf.pack(fill="x", padx=6, pady=(0, 4))
        tk.Label(sf, text="🔍", bg=COLORS["panel2"], fg=COLORS["text_dim"],
                 font=("Courier", 10)).pack(side="left", padx=4)
        self.ref_search_var = tk.StringVar()
        ctk.CTkEntry(sf, textvariable=self.ref_search_var,
                      fg_color=COLORS["panel2"], text_color=COLORS["text"],
                      border_color=COLORS["border"], height=26,
                      font=ctk.CTkFont(family="Courier", size=10)).pack(
                          side="left", fill="x", expand=True, pady=3)
        ctk.CTkButton(sf, text="✕", width=24, height=22,
                       fg_color=COLORS["panel2"], hover_color=COLORS["border"],
                       text_color=COLORS["text_dim"],
                       font=ctk.CTkFont(family="Courier", size=11),
                       command=lambda: self.ref_search_var.set("")).pack(side="right", padx=4)

        # Horizontal split: list | detail
        ref_pane = tk.PanedWindow(parent, orient="horizontal", bg=COLORS["border"],
                                  sashwidth=4, sashrelief="flat", handlesize=0)
        ref_pane.pack(fill="both", expand=True, padx=4, pady=2)

        lf = tk.Frame(ref_pane, bg=COLORS["panel"])
        ref_pane.add(lf, minsize=120, width=170, stretch="never")
        list_sb = tk.Scrollbar(lf)
        list_sb.pack(side="right", fill="y")
        self.ref_listbox = tk.Listbox(lf, yscrollcommand=list_sb.set,
                                      bg=COLORS["panel2"], fg=COLORS["text"],
                                      selectbackground=COLORS["border"],
                                      selectforeground=COLORS["accent"],
                                      font=("Courier", 11), relief="flat",
                                      activestyle="none", bd=0)
        self.ref_listbox.pack(fill="both", expand=True)
        list_sb.config(command=self.ref_listbox.yview)

        rf = tk.Frame(ref_pane, bg=COLORS["panel"])
        ref_pane.add(rf, minsize=140, stretch="always")

        dt = tk.Frame(rf, bg=COLORS["panel2"])
        dt.pack(fill="x")
        self.ref_title_var = tk.StringVar(value="")
        tk.Label(dt, textvariable=self.ref_title_var, bg=COLORS["panel2"],
                 fg=COLORS["accent"], font=("Courier", 11, "bold"),
                 anchor="w").pack(side="left", padx=6, fill="x", expand=True)
        self._btn(dt, "⎘ Insert", self._ref_insert_code, small=True).pack(side="right", padx=4, pady=2)
        self._btn(dt, "📋 Copy",  self._ref_copy_code,   small=True).pack(side="right", padx=2, pady=2)

        dsby = tk.Scrollbar(rf, orient="vertical")
        dsby.pack(side="right", fill="y")
        dsbx = tk.Scrollbar(rf, orient="horizontal")
        dsbx.pack(side="bottom", fill="x")
        self.ref_detail = tk.Text(rf, bg="#0d1117", fg="#00ff88",
                                  font=("Courier", 10), relief="flat",
                                  wrap="none", bd=0, padx=8, pady=6,
                                  yscrollcommand=dsby.set,
                                  xscrollcommand=dsbx.set,
                                  state="disabled")
        self.ref_detail.pack(fill="both", expand=True)
        dsby.config(command=self.ref_detail.yview)
        dsbx.config(command=self.ref_detail.xview)
        for tag, col in [("comment","#446644"),("keyword","#00e5ff"),
                          ("string","#ffaa44"),("number","#ff6b35"),("func","#aa88ff"),
                          ("desc", COLORS["text_dim"]),("divider", COLORS["border"])]:
            self.ref_detail.tag_configure(tag, foreground=col)

        self._ref_items = []
        self._ref_current_code = ""
        for cat, items in REFERENCE.items():
            for title, body in items:
                self._ref_items.append((cat, title, body))

        def _populate(ft=""):
            self.ref_listbox.delete(0, tk.END)
            f = ft.strip().lower()
            last_cat = None
            for cat, title, body in self._ref_items:
                if f and f not in title.lower() and f not in body.lower() and f not in cat.lower():
                    continue
                if cat != last_cat:
                    self.ref_listbox.insert(tk.END, "  \u2014 " + cat + " \u2014")
                    self.ref_listbox.itemconfig(tk.END, fg=COLORS["accent"],
                                                selectforeground=COLORS["accent"],
                                                bg=COLORS["panel"])
                    last_cat = cat
                self.ref_listbox.insert(tk.END, "  " + title)

        _populate()
        self._ref_populate = _populate
        self.ref_search_var.trace_add("write",
            lambda *a: _populate(self.ref_search_var.get()))

        def _on_select(event):
            sel = self.ref_listbox.curselection()
            if not sel:
                return
            raw = self.ref_listbox.get(sel[0]).strip()
            text = raw.lstrip("\u2014 ").rstrip(" \u2014")
            ft = self.ref_search_var.get().strip().lower()
            for cat, title, body in self._ref_items:
                if ft and ft not in title.lower() and ft not in body.lower() and ft not in cat.lower():
                    continue
                if title == text:
                    self.ref_title_var.set("  " + cat + "  \u203a  " + title)
                    parts = body.split("\n\n", 1)
                    desc = parts[0] if len(parts) > 1 else ""
                    code = parts[1] if len(parts) > 1 else body
                    self._ref_current_code = code
                    self.ref_detail.config(state="normal")
                    self.ref_detail.delete("1.0", tk.END)
                    if desc:
                        self.ref_detail.insert(tk.END, desc + "\n", "desc")
                        self.ref_detail.insert(tk.END, "\u2500" * 38 + "\n", "divider")
                    self.ref_detail.insert(tk.END, code)
                    self._highlight_ref_detail()
                    self.ref_detail.config(state="disabled")
                    break

        self.ref_listbox.bind("<<ListboxSelect>>", _on_select)

    def _highlight_ref_detail(self):
        import re
        text = self.ref_detail
        content = text.get("1.0", tk.END)
        for tag in ("comment", "keyword", "string", "number", "func"):
            text.tag_remove(tag, "1.0", tk.END)
        patterns = [
            ("comment", r"//[^\n]*"),
            ("string",  r'"[^"]*"'),
            ("keyword", r"\b(local|if|else|for|foreach|while|do|return|true|false|null|function|class|extends|base|this|break|continue|switch|case|default|try|catch|throw|yield|const|enum|static|typeof|instanceof|in|delete|clone|resume)\b"),
            ("func",    r"\b(fe|add_artwork|add_text|add_image|add_surface|add_sound|add_shader|load_module|add_transition_callback|add_signal_handler|game_info|get_input_state|print|error|format|sqrt|sin|cos|pow|abs|floor|ceil|rand|clock|time)\b"),
            ("number",  r"\b\d+(\.\d+)?\b"),
        ]
        for tag, pattern in patterns:
            for m in re.finditer(pattern, content):
                s = "1.0 + %d chars" % m.start()
                e = "1.0 + %d chars" % m.end()
                text.tag_add(tag, s, e)

    def _ref_copy_code(self):
        if self._ref_current_code:
            self.clipboard_clear()
            self.clipboard_append(self._ref_current_code)

    def _ref_insert_code(self):
        if self._ref_current_code:
            self.code_text.config(state="normal")
            try:
                pos = self.code_text.index(tk.INSERT)
            except Exception:
                pos = tk.END
            self.code_text.insert(pos, "\n" + self._ref_current_code + "\n")
            self._highlight_code()


    def _build_docs_tab(self, parent):
        """
        Loads Layouts.md from the same folder as this script and presents it
        as a searchable, section-browsable reference panel.
        Falls back to a helpful message if the file is not found.
        """
        import os, re

        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        MD_PATH    = os.path.join(SCRIPT_DIR, "Layouts.md")

        # ── Header ────────────────────────────────────────────────────────────
        hdr = tk.Frame(parent, bg=COLORS["panel2"])
        hdr.pack(fill="x")
        tk.Label(hdr, text="◈ AM+ LAYOUT REFERENCE  (Layouts.md)",
                 bg=COLORS["panel2"], fg=COLORS["accent"],
                 font=("Courier", 10, "bold")).pack(side="left", padx=8, pady=5)
        self._docs_path_var = tk.StringVar(value=MD_PATH)
        self._btn(hdr, "📂 Load File", self._docs_browse, small=True).pack(side="right", padx=6, pady=4)

        # ── Search bar ────────────────────────────────────────────────────────
        sf = tk.Frame(parent, bg=COLORS["panel2"])
        sf.pack(fill="x", padx=6, pady=(2, 4))
        tk.Label(sf, text="🔍", bg=COLORS["panel2"], fg=COLORS["text_dim"],
                 font=("Courier", 10)).pack(side="left", padx=4)
        self._docs_search_var = tk.StringVar()
        ctk.CTkEntry(sf, textvariable=self._docs_search_var,
                      fg_color=COLORS["panel2"], text_color=COLORS["text"],
                      border_color=COLORS["border"], height=26,
                      font=ctk.CTkFont(family="Courier", size=10)).pack(
                          side="left", fill="x", expand=True, pady=3)
        ctk.CTkButton(sf, text="✕", width=24, height=22,
                       fg_color=COLORS["panel2"], hover_color=COLORS["border"],
                       text_color=COLORS["text_dim"],
                       font=ctk.CTkFont(family="Courier", size=11),
                       command=lambda: self._docs_search_var.set("")).pack(side="right", padx=4)
        self._docs_search_var.trace_add("write", lambda *a: self._docs_apply_search())

        # ── Horizontal split: section list | content ──────────────────────────
        pane = tk.PanedWindow(parent, orient="horizontal", bg=COLORS["border"],
                              sashwidth=4, sashrelief="flat", handlesize=0)
        pane.pack(fill="both", expand=True, padx=4, pady=2)

        lf = tk.Frame(pane, bg=COLORS["panel"])
        pane.add(lf, minsize=130, width=165, stretch="never")
        lsb = tk.Scrollbar(lf)
        lsb.pack(side="right", fill="y")
        self._docs_listbox = tk.Listbox(lf, yscrollcommand=lsb.set,
                                        bg=COLORS["panel2"], fg=COLORS["text"],
                                        selectbackground=COLORS["border"],
                                        selectforeground=COLORS["accent"],
                                        font=("Courier", 11), relief="flat",
                                        activestyle="none", bd=0)
        self._docs_listbox.pack(fill="both", expand=True)
        lsb.config(command=self._docs_listbox.yview)
        self._docs_listbox.bind("<<ListboxSelect>>", self._docs_on_select)

        rf = tk.Frame(pane, bg=COLORS["panel"])
        pane.add(rf, minsize=150, stretch="always")

        ct = tk.Frame(rf, bg=COLORS["panel2"])
        ct.pack(fill="x")
        self._docs_section_var = tk.StringVar(value="")
        tk.Label(ct, textvariable=self._docs_section_var,
                 bg=COLORS["panel2"], fg=COLORS["accent"],
                 font=("Courier", 11, "bold"), anchor="w").pack(side="left", padx=6, fill="x", expand=True)
        self._btn(ct, "📋 Copy", self._docs_copy, small=True).pack(side="right", padx=4, pady=2)

        dsby = tk.Scrollbar(rf, orient="vertical")
        dsby.pack(side="right", fill="y")
        dsbx = tk.Scrollbar(rf, orient="horizontal")
        dsbx.pack(side="bottom", fill="x")
        docs_bg = COLORS["panel2"]
        self._docs_text = tk.Text(rf, bg=docs_bg, fg=COLORS["text"],
                                  font=("Courier", 10), relief="flat",
                                  wrap="word", bd=0, padx=10, pady=8,
                                  yscrollcommand=dsby.set,
                                  xscrollcommand=dsbx.set,
                                  state="disabled")
        self._docs_text.pack(fill="both", expand=True)
        dsby.config(command=self._docs_text.yview)
        dsbx.config(command=self._docs_text.xview)

        self._docs_text.tag_configure("h1",      foreground=COLORS["accent"],     font=("Courier", 13, "bold"))
        self._docs_text.tag_configure("h2",      foreground=COLORS["accent"],     font=("Courier", 11, "bold"))
        self._docs_text.tag_configure("h3",      foreground=COLORS["accent2"],    font=("Courier", 10, "bold"))
        self._docs_text.tag_configure("h4",      foreground=COLORS["accent2"],    font=("Courier", 10, "bold"))
        self._docs_text.tag_configure("code",    foreground="#00ff88",            font=("Courier", 10), background="#0d1117")
        self._docs_text.tag_configure("bullet",  foreground=COLORS["text_dim"],   lmargin1=16, lmargin2=24)
        self._docs_text.tag_configure("normal",  foreground=COLORS["text"])
        self._docs_text.tag_configure("dim",     foreground=COLORS["text_dim"])
        self._docs_text.tag_configure("divider", foreground=COLORS["border"])
        self._docs_text.tag_configure("search_hi", background=COLORS["accent"],  foreground=COLORS["bg"])

        self._docs_status_var = tk.StringVar(value="")
        tk.Label(parent, textvariable=self._docs_status_var,
                 bg=COLORS["panel2"], fg=COLORS["text_dim"],
                 font=("Courier", 11), anchor="w", padx=6).pack(fill="x", side="bottom")

        # ── Internal state ────────────────────────────────────────────────────
        self._docs_sections = []   # list of (title, raw_text)
        self._docs_all_text = ""

        # Load file
        self._docs_load(MD_PATH)

    # ── Docs helpers ──────────────────────────────────────────────────────────

    def _docs_browse(self):
        path = filedialog.askopenfilename(
            title="Open AM+ Reference Markdown",
            filetypes=[("Markdown", "*.md *.txt"), ("All Files", "*.*")]
        )
        if path:
            self._docs_load(path)

    def _docs_load(self, path):
        import os, re
        if not os.path.isfile(path):
            self._docs_sections = [("ℹ  File not found",
                f"Could not find:\n  {path}\n\n"
                "Place 'Layouts.md' in the same folder as this script,\n"
                "or click  📂 Load File  to browse for it.\n\n"
                "The file is the official Attract-Mode Plus Layout and\n"
                "Plug-in Programming Reference.")]
            self._docs_populate_list()
            self._docs_show_section(0)
            self._docs_status_var.set("Layouts.md not found — click 📂 Load File to browse")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
        except Exception as e:
            self._docs_status_var.set(f"Error loading file: {e}")
            return

        self._docs_all_text = raw
        self._docs_path_var.set(path)

        # Parse into sections by heading
        # Each section = everything from one heading to the next
        sections = []
        current_title = "Overview"
        current_lines = []

        for line in raw.splitlines():
            # Detect heading lines: #, ##, ###, ####  or underline-style ====/----
            stripped = line.strip()
            is_heading = False

            if re.match(r'^#{1,4}\s+', line):
                if current_lines or current_title:
                    sections.append((current_title, "\n".join(current_lines).strip()))
                current_title = re.sub(r'^#+\s*', '', line).strip()
                # Clean anchor/backtick noise
                current_title = re.sub(r'`', '', current_title)
                current_title = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', current_title)
                current_lines = []
                is_heading = True

            if not is_heading:
                current_lines.append(line)

        if current_lines:
            sections.append((current_title, "\n".join(current_lines).strip()))

        # Filter out empty sections and TOC noise
        self._docs_sections = [(t, b) for t, b in sections if b.strip() and len(b.strip()) > 20]

        self._docs_populate_list()
        if self._docs_sections:
            self._docs_show_section(0)
        count = len(self._docs_sections)
        import os
        self._docs_status_var.set(f"Loaded {count} sections  —  {os.path.basename(path)}")

    def _docs_populate_list(self, filter_text=""):
        self._docs_listbox.delete(0, tk.END)
        ft = filter_text.strip().lower()
        self._docs_filtered = []
        for i, (title, body) in enumerate(self._docs_sections):
            if ft and ft not in title.lower() and ft not in body.lower():
                continue
            self._docs_filtered.append(i)
            self._docs_listbox.insert(tk.END, "  " + title)

    def _docs_apply_search(self):
        ft = self._docs_search_var.get()
        self._docs_populate_list(ft)
        # If something is showing, highlight matches in content
        if ft and hasattr(self, "_docs_text"):
            self._docs_highlight_search(ft)
        count = len(self._docs_filtered) if hasattr(self, "_docs_filtered") else 0
        total = len(self._docs_sections)
        self._docs_status_var.set(
            f"Showing {count} of {total} sections"
            + (f"  —  filter: \"{ft}\"" if ft else ""))

    def _docs_on_select(self, event):
        sel = self._docs_listbox.curselection()
        if not sel:
            return
        pos = sel[0]
        if hasattr(self, "_docs_filtered") and pos < len(self._docs_filtered):
            self._docs_show_section(self._docs_filtered[pos])

    def _docs_show_section(self, idx):
        import re
        if idx >= len(self._docs_sections):
            return
        title, body = self._docs_sections[idx]
        self._docs_section_var.set(f"  {title}")

        self._docs_text.config(state="normal")
        self._docs_text.delete("1.0", tk.END)

        # Render with basic markdown-aware formatting
        in_code_block = False
        code_buf = []

        for line in body.splitlines():
            stripped = line.strip()

            # Fenced code blocks
            if stripped.startswith("```") or stripped.startswith("````"):
                if not in_code_block:
                    in_code_block = True
                    code_buf = []
                else:
                    in_code_block = False
                    code = "\n".join(code_buf)
                    self._docs_text.insert(tk.END, code + "\n", "code")
                continue

            if in_code_block:
                code_buf.append(line)
                continue

            # Inline code: wrap `...` spans in code tag
            if "`" in line:
                parts = re.split(r'(`[^`]+`)', line)
                for part in parts:
                    if part.startswith("`") and part.endswith("`"):
                        self._docs_text.insert(tk.END, part[1:-1], "code")
                    else:
                        # strip markdown links [text](url)
                        clean = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', part)
                        # strip bold/italic markers
                        clean = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', clean)
                        self._docs_text.insert(tk.END, clean, "normal")
                self._docs_text.insert(tk.END, "\n")
                continue

            # Headings
            if re.match(r'^#{4}\s', line):
                self._docs_text.insert(tk.END, line.lstrip("#").strip() + "\n", "h4")
                continue
            if re.match(r'^#{3}\s', line):
                self._docs_text.insert(tk.END, line.lstrip("#").strip() + "\n", "h3")
                continue
            if re.match(r'^#{2}\s', line):
                self._docs_text.insert(tk.END, line.lstrip("#").strip() + "\n", "h2")
                continue
            if re.match(r'^#\s', line):
                self._docs_text.insert(tk.END, line.lstrip("#").strip() + "\n", "h1")
                continue

            # Horizontal rules
            if re.match(r'^[-*_]{3,}$', stripped):
                self._docs_text.insert(tk.END, "\u2500" * 50 + "\n", "divider")
                continue

            # Bullet points
            if re.match(r'^\s{0,6}[-*+]\s', line) or re.match(r'^\s{0,6}\d+\.\s', line):
                clean = re.sub(r'^\s*[-*+\d.]+\s', '', line)
                clean = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', clean)
                clean = re.sub(r'`([^`]+)`', r'\1', clean)
                clean = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', clean)
                indent = "      " if line.startswith("  ") else "   "
                self._docs_text.insert(tk.END, indent + "• " + clean.strip() + "\n", "bullet")
                continue

            # Skip pure anchor tags and blank separator lines
            if re.match(r'^&nbsp;$', stripped) or re.match(r'^<a name=', stripped):
                self._docs_text.insert(tk.END, "\n")
                continue

            # Normal paragraph text
            clean = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', line)
            clean = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', clean)
            if clean.strip():
                self._docs_text.insert(tk.END, clean + "\n", "normal")
            else:
                self._docs_text.insert(tk.END, "\n")

        self._docs_text.config(state="disabled")
        self._docs_text.yview_moveto(0)

        # Apply search highlight if active
        ft = self._docs_search_var.get().strip()
        if ft:
            self._docs_highlight_search(ft)

    def _docs_highlight_search(self, term):
        import re
        self._docs_text.tag_remove("search_hi", "1.0", tk.END)
        if not term:
            return
        content = self._docs_text.get("1.0", tk.END)
        for m in re.finditer(re.escape(term), content, re.IGNORECASE):
            s = "1.0 + %d chars" % m.start()
            e = "1.0 + %d chars" % m.end()
            self._docs_text.tag_add("search_hi", s, e)

    def _docs_copy(self):
        sel = self._docs_listbox.curselection()
        if sel and hasattr(self, "_docs_filtered"):
            pos = sel[0]
            if pos < len(self._docs_filtered):
                _, body = self._docs_sections[self._docs_filtered[pos]]
                self.clipboard_clear()
                self.clipboard_append(body)
                self._docs_status_var.set("Section copied to clipboard")


    def show_theme_picker(self):
        win = ctk.CTkToplevel(self)
        win.title("Choose Theme")
        win.resizable(True, True)
        win.transient(self)
        win.grab_set()
        win.geometry("680x400")
        win.after(50, win.lift)  # CTkToplevel needs a moment to appear on top

        ctk.CTkLabel(win, text="◈ CHOOSE THEME",
                     text_color=COLORS["accent"],
                     font=ctk.CTkFont(family="Courier", size=12, weight="bold")).pack(
                         padx=20, pady=(14, 2))
        ctk.CTkLabel(win, text="Select a colour scheme for the interface.",
                     text_color=COLORS["text_dim"],
                     font=ctk.CTkFont(family="Courier", size=11)).pack(padx=20, pady=(0, 10))

        # ── Preset grid ──────────────────────────────────────────────────────
        grid_frame = tk.Frame(win, bg=COLORS["bg"])
        grid_frame.pack(fill="x", padx=16, pady=(0, 8))

        themes = list(THEMES.keys())
        cols = 4
        for i, name in enumerate(themes):
            t = THEMES[name]
            row_idx, col_idx = divmod(i, cols)
            is_active = (name == _ACTIVE_THEME)

            card = tk.Frame(grid_frame, bg=t["panel"], bd=0,
                            highlightthickness=2,
                            highlightbackground=t["accent"] if is_active else t["border"],
                            cursor="hand2")
            card.grid(row=row_idx, column=col_idx, padx=6, pady=4, sticky="ew")
            grid_frame.columnconfigure(col_idx, weight=1)

            # Colour swatches
            swatch_row = tk.Frame(card, bg=t["panel"])
            swatch_row.pack(fill="x", padx=6, pady=(6, 2))
            for sc in [t["bg"], t["panel2"], t["accent"], t["accent2"], t["text"]]:
                tk.Frame(swatch_row, bg=sc, width=14, height=14).pack(side="left", padx=1)

            # Name label — mark active theme
            label_text = f"✓ {name}" if is_active else name
            tk.Label(card, text=label_text, bg=t["panel"], fg=t["accent"],
                     font=("Courier", 11, "bold")).pack(anchor="w", padx=8, pady=(0, 4))

            def _hover_in(e, c=card, t=t):
                c.config(highlightbackground=t["accent"])
            def _hover_out(e, c=card, t=t, n=name):
                c.config(highlightbackground=t["accent"] if n == _ACTIVE_THEME else t["border"])
            def _pick(e=None, n=name, w=win):
                self.apply_theme(n)
                w.destroy()

            for widget in [card] + card.winfo_children() + [
                    w2 for child in card.winfo_children() for w2 in child.winfo_children()]:
                widget.bind("<Enter>",    _hover_in)
                widget.bind("<Leave>",    _hover_out)
                widget.bind("<Button-1>", _pick)

        # ── Cancel ────────────────────────────────────────────────────────────
        self._btn(win, "Cancel", win.destroy, small=True).pack(pady=(4, 14))

    def apply_theme(self, theme_name):
        if theme_name not in THEMES:
            return
        _sync_colors(theme_name)
        self._apply_style()
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()
        self.update_code()
        self.canvas.redraw()



    def show_help(self):
        help_text = """ATTRACT-MODE PLUS LAYOUT DESIGNER — HELP

CANVAS:
  • Click an element to select it
  • Drag to reposition
  • Drag the orange corner handle to resize
  • Right-click for context menu (delete, duplicate, z-order)
  • Mouse wheel: scroll canvas

ADDING ELEMENTS:
  • Pick a type on the left panel
  • Click "+ Add Element"
  • Adjust in Properties tab (right panel)

ELEMENT TYPES:
  snap       — Game screenshot/snap artwork
  wheel      — Game wheel logo artwork
  boxart     — Box/cover artwork
  marquee    — Marquee/header artwork
  flyer      — Flyer artwork
  fanart     — Fan art
  video      — Snap video (uses snap art slot)
  text       — Static or token-based text
  surface    — Offscreen render surface
  artwork    — Generic artwork (custom slot name)

TEXT TOKENS (use in text strings):
  [Title]     [Year]      [Manufacturer]
  [Players]   [Category]  [Rating]
  [PlayedCount] [PlayedTime]

MODULES:
  Toggle modules in the Modules tab.
  They will be added as fe.load_module() calls.

CODE TAB:
  • Live-updating layout.nut code
  • Syntax highlighted
  • Editable directly
  • Save with 💾 button

OUTPUT:
  Save your layout.nut and place it in:
  ~/.attract/layouts/YOUR_LAYOUT_NAME/layout.nut
  
THANKS: Claude & Deepseek Ai
        JJTheKing
        Tankman3737 Wheel Code Snippets
        PaCiFiKbAllA  - Feedback
        Version 4.2 (04/25/2026)        
"""
        win = ctk.CTkToplevel(self)
        win.title("Help")
        win.geometry("560x560")
        win.transient(self)
        t = tk.Text(win, bg=COLORS["panel"], fg=COLORS["text"],
                    font=("Courier", 10), relief="flat", padx=12, pady=12)
        t.pack(fill="both", expand=True, padx=8, pady=8)
        t.insert("1.0", help_text)
        t.config(state="disabled")


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = AttractLayoutBuilder()
    app.mainloop()
