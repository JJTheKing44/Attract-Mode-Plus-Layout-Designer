<img width="1536" height="1024" alt="AMP-LD" src="https://github.com/user-attachments/assets/71ab12a0-6af4-489d-8edb-b6c0809a0256" />

An all-in-one GUI toolkit for **Attract-Mode Plus** frontend development.  
Build `layout.nut` files visually, edit romlists, generate emulator CFG files, and look up Squirrel/AM+ code references — all in one app, no extra dependencies required.

---

## Requirements

**Windows


## Interface Overview

The window is split into three resizable panels. Drag the dividers between panels to resize them.

```
┌──────────────────────┬──────────────────────────┬──────────────────────┐
│  Elements            │                          │  Properties          │
│  Modules             │    Layout Canvas         │  layout.nut (code)   │
│  Romlist Editor      │    (center)              │  Reference           │
│  CFG Generator       │                          │  (right)             │
│  (left)              │                          │                      │
└──────────────────────┴──────────────────────────┴──────────────────────┘
```

---

## Left Panel

### Elements Tab

**Add Element** — Select an element type from the alphabetically sorted radio list, then click **+ Add Element** to place it on the canvas.

| Element Type | What it does |
|---|---|
| `artwork` | Generic artwork with a custom slot name |
| `boxart` | Box / cover art |
| `fanart` | Fan art image |
| `flyer` | Flyer / poster art |
| `marquee` | Marquee / header artwork |
| `shader_layer` | Layer for GLSL shader effects |
| `snap` | Game screenshot |
| `surface` | Offscreen render surface |
| `text` | Static or magic-token text label |
| `video` | Snap video (uses the snap art slot) |
| `wheel` | Wheel logo artwork |

**Element List** — All added elements shown in alphabetical order by name. Click to select. Buttons at the bottom:

| Button | Action |
|---|---|
| ↑ / ↓ | Change Z-order (draw order) |
| ⊕ Dupe | Duplicate the selected element |
| ✕ Del | Delete the selected element |

---

### Modules Tab

Checkboxes for all supported Attract-Mode Plus modules. Check any module to include it as a `fe.load_module()` call at the top of your generated code.

**Hover** over any module row to see a floating tooltip and an info bar description at the bottom of the list. The module list is **scrollable** — use the scrollbar or mouse wheel to reach all modules.

| Module | Purpose |
|---|---|
| `animate` | Property animation (fade, move, scale, spin) |
| `config` | User-configurable layout settings |
| `conveyor` | Scrolling artwork conveyor belt |
| `conveyor_helper` | Helper utilities for conveyor layouts |
| `fade` | Screen transition fade effects |
| `file` | File I/O from within layouts |
| `file_format` | Parse / format structured data (CSV etc.) |
| `file_layout` | Load and manage multiple layout files |
| `gtc` | Game & system tag/category filtering |
| `gtc_kb` | Keyboard input support for gtc |
| `inertia` | Momentum-based smooth scrolling |
| `mask` | Alpha mask and clipping regions |
| `math` | Extended math (lerp, clamp, easing) |
| `pan_and_scan` | Pan and scan artwork zoom/pan effect |
| `wheel` | Wheel artwork list navigation |

---

### Romlist Tab

A full-featured editor for Attract-Mode Plus romlist files (`.txt` / `.lst`).

**Toolbar buttons:**

| Button | Action |
|---|---|
| 📂 Open | Open a romlist file |
| 💾 Save | Save changes to the current file |
| 💾 Save As | Save to a new file |
| ✎ Bulk Edit | Set the same value for an entire column across all rows |
| + Add Row | Append a new empty row |
| ✕ Del Row | Delete the selected row |

**Features:**
- **Double-click any cell** to edit it inline — a popup appears right on the cell, press Enter to confirm or Escape to cancel
- **Click any column header** to sort the list A→Z or Z→A (toggles with ▲▼ indicator)
- **🔍 Search bar** — filters rows live as you type, shows matching count vs total
- **Right-click context menu** on any row — Edit Cell, Bulk Edit Column, Add Row, Delete Row
- **Header bar** shows the raw semicolon-delimited header of the loaded file
- **Status bar** shows entry count, current filter, and last action

**File format:** Attract-Mode romlists are semicolon-delimited text files. The first line is the header row defining column names (e.g. `Name;Title;Emulator;CloneOf;Year;...`). Each subsequent line is one game entry.

---

### CFG Gen Tab

Generates complete emulator `.cfg` files for Attract-Mode Plus with a point-and-click interface. No AHK required.

**Supported emulators:**
- **MAME** — pre-configured cores and arguments for all supported systems
- **RetroArch** — pre-configured libretro core filenames for all supported systems
- **Other** — custom executable path and arguments for any other emulator

**How to use:**
1. Select an **Emulator** from the dropdown — the system list updates automatically
2. Select a **Game System** — ROM extensions auto-fill for the selected system
3. Adjust **ROM Extensions** if needed (semicolon-separated, e.g. `.zip;.7z`)
4. For **Other** emulator: fill in the Executable Path and Arguments fields (auto-filled for known systems like Yuzu, Cemu, RPCS3)
5. Check any **Artwork Folders** to include — use **All** / **None** for quick selection
6. Watch the **Preview pane** update live as you make changes
7. Click **💾 Save .cfg** — the filename is pre-filled as `System_Name.cfg`

**Supported systems by emulator:**

*MAME:* Arcade, Atari 2600/5200/7800, ColecoVision, Mattel Intellivision, NEC TurboGrafx-16, NES, Gameboy/Color/Advance, SNES, Sega Master System/SG-1000/Genesis/32X/CD, Sony Playstation, SNK Neo Geo

*RetroArch:* All MAME systems plus Atari Jaguar, Nintendo 64/GameCube/Wii, Sega Dreamcast/Saturn/Naomi, Sammy Atomiswave, Sony Playstation 2

*Other:* Nintendo Switch (Yuzu), Nintendo Wii U (Cemu), PC Games, Sony Playstation 3 (RPCS3)

**Artwork folder options:** boxart, cart, cover, disc, fanart, flyer, marquee, snap, wheel

**Example output:**
```
# Generated by Attract-Mode Plus CFG Generator
#
executable           $PROGDIR\emulators\RetroArch-Win64\retroarch.exe
args                 -L cores\snes9x_libretro.dll "[romfilename]"
rompath              $PROGDIR\collections\Super Nintendo Entertainment System\roms\
romext               .zip;.7z
system               Super Nintendo Entertainment System
info_source          thegamesdb.net

artwork    snap            collections\Super Nintendo Entertainment System\snap
artwork    wheel           collections\Super Nintendo Entertainment System\wheel
artwork    boxart          collections\Super Nintendo Entertainment System\boxart
```

---

## Center Panel — Canvas

A live preview of your layout at the configured resolution.

| Action | How |
|---|---|
| Select element | Left-click |
| Move element | Click and drag |
| Resize element | Drag the **orange corner handle** (bottom-right) |
| Deselect | Click empty canvas area |
| Context menu | Right-click any element |

**Context menu options:** Delete, Duplicate, Bring Forward, Send Backward.

When an element is selected, its current **position** `(x, y)` and **size** `width × height` are shown next to it on the canvas.

**Canvas Zoom** — Use the zoom slider in the toolbar to scale the preview. Useful for large resolutions like 4K.

---

## Right Panel

### Properties Tab

Edit all properties of the currently selected element:

**Position & Size**
- Name, X, Y, Width, Height, Rotation, Z-Order

**Appearance**
- Alpha (0–255), Blend Mode, Visible toggle, Preserve Aspect Ratio

**Text** *(text elements only)*
- String content (supports magic tokens like `[Title]`, `[Year]`)
- Font name, Font size, Font colour (colour picker), Alignment

**Animation**
- Enable/disable, Trigger event, Duration (ms)

---

### layout.nut Tab

A live, syntax-highlighted view of the Squirrel code generated from your layout.

- Scrolls both **vertically and horizontally**
- **Auto-update** checkbox — uncheck to pause live updates while you manually edit
- **📋 Copy** — copy all code to clipboard
- **💾 Save .nut** — save directly to a file

The generated code uses **dynamic resolution variables** so your layout scales to any screen automatically:

```squirrel
fe.layout.width  = 1920;
fe.layout.height = 1080;

local flw = fe.layout.width;
local flh = fe.layout.height;

// Elements use expressions like:
local snap_1 = fe.add_artwork("snap", 0, 0, flw/2, flh/2);
local title_1 = fe.add_text("[Title]", 0, flh*9/10, flw, flh/10);
```

Clean fractions are used wherever possible (`flw/2`, `flw*3/4`, `flh/4`, etc.). Non-standard values fall back to a decimal multiplier (`flw*0.234`).

---

### Reference Tab

A built-in searchable reference covering **Squirrel** language syntax and the **AM+ fe.* API** — no need to leave the app to look things up.

**Categories:**
- AM+ fe.* API
- AM+ Object Properties
- AM+ Enums & Constants
- AM+ Magic Tokens
- Squirrel: Variables & Types
- Squirrel: Control Flow
- Squirrel: Functions & Classes
- Squirrel: Built-in Functions

**Using the reference:**
1. Type in the **search bar** to filter across all categories instantly
2. Click any entry in the list to see a description and syntax-highlighted code example in the detail pane
3. **📋 Copy** — copy the code snippet to clipboard
4. **⎘ Insert** — paste the snippet directly into the layout.nut editor at the cursor position

---

## Toolbar

### Resolution

| Control | Purpose |
|---|---|
| **W:** / **H:** | Type any custom width and height — updates the canvas and generated code instantly |
| **Presets** | Quick-fill from common resolutions (1920×1080, 1280×720, 4K, etc.) |
| **Canvas Zoom** | Slider to scale the canvas preview (0.10 – 1.00) |

### Top Buttons

| Button | Action |
|---|---|
| 💾 Save .nut | Save the generated layout.nut to disk |
| 📂 Load .nut | Load an existing .nut file for viewing / manual editing |
| 🗑 Clear All | Remove all elements and reset the layout |
| ❓ Help | Show the in-app help window |

---

## Magic Tokens

Use these inside **text element** strings to display live game data:

| Token | Output |
|---|---|
| `[Title]` | Game title |
| `[Year]` | Release year |
| `[Manufacturer]` | Manufacturer / developer |
| `[Players]` | Number of players |
| `[Category]` | Game category |
| `[Rating]` | Content rating |
| `[System]` | System / emulator name |
| `[Overview]` | Game description |
| `[PlayedCount]` | Number of times played |
| `[PlayedTime]` | Total time played |
| `[ListEntry]` | Current list position |
| `[ListSize]` | Total number of games in list |
| `[ListFilterName]` | Active filter name |
| `[!%H:%M]` | Live clock (C strftime format) |

---

## Output File Locations

| File | Where to put it |
|---|---|
| `layout.nut` | `~/.attract/layouts/YOUR_LAYOUT_NAME/layout.nut` |
| `System_Name.cfg` | Your emulator folder (e.g. `$PROGDIR/emulators/retroarch/`) |
| Romlist `.txt` | `~/.attract/romlists/System_Name.txt` |

Any images, sounds, or shader files referenced in your layout should go in the same folder as `layout.nut`.

---

## Tips

- **Z-order** controls which elements draw on top. Higher = in front. Change it with ↑/↓ in the element list or via right-click on the canvas.
- **Duplicate** an element to quickly create matching pairs (e.g. a snap and a decorative frame behind it).
- The **Reference tab** has ready-to-use code snippets for every `fe.*` function and Squirrel language feature — use **⎘ Insert** to drop them straight into your code.
- **Auto-update** in the code tab can be turned off while you hand-edit the code, then turned back on to sync.
- All three panels are **resizable** — drag the dividers to give more space to the canvas or the code editor as needed.
- The canvas **right-click menu** is the fastest way to delete or duplicate elements.
- In the **Romlist tab**, clicking a column header sorts the entire list by that column — click again to reverse the sort order.
- In the **CFG Gen tab**, the preview pane updates live so you can see exactly what will be saved before clicking Save.
- The **Modules tab** is scrollable — use the mouse wheel to reach all 15 modules.

---

## License

Free to use and modify. Built with Python and tkinter — no external dependencies required.

Color Changer
<img width="332" height="474" alt="image" src="https://github.com/user-attachments/assets/7c577d0c-ac21-43a7-afc1-3d72094d1354" />

