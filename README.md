<img width="1536" height="1024" alt="AMP-LD" src="https://github.com/user-attachments/assets/71ab12a0-6af4-489d-8edb-b6c0809a0256" />

# ⚡ Attract-Mode Plus — Layout Designer

A visual drag-and-drop layout builder for **Attract-Mode Plus** frontends.  
Build, preview, and export `layout.nut` files without writing Squirrel script by hand.

**Version 6.5**

---

## Requirements

```
Windows 10/11
```

Run with:
```
Attract-Mode Plus - Layout Designer-TKK.exe
```

---

## Interface Overview

The app has three zones:

```
┌─────────────────────────────────────────────────────────────────┐
│  Menu bar:  File · Edit · View · Tools · Help                   │
│  Toolbar:   Load · Save · Clear · Preview · Theme               │
│  Res bar:   W · H · Presets · Zoom                              │
├──────────────┬──────────────────────────────┬───────────────────┤
│  Left panel  │       Canvas (preview)       │   Right panel     │
│  Elements    │                              │   Properties      │
│  Modules     │                              │   layout.nut      │
│  Snippets    │                              │                   │
└──────────────┴──────────────────────────────┴───────────────────┘
```

---

## Menu Bar

### File
| Item | Shortcut | Action |
|---|---|---|
| New Layout | `Ctrl+N` | Clear all elements and reset |
| Load .nut… | `Ctrl+O` | Load an existing layout.nut file |
| Save .nut | `Ctrl+S` | Save the current layout code |
| Layout Info… | | Set name, author, version, date, notes for the file header |
| ▶ Preview in AM+ | | Launch Attract-Mode Plus with the current layout |
| Exit | | Close the application |

### Edit
| Item | Shortcut | Action |
|---|---|---|
| Duplicate Element | `Ctrl+D` | Clone the selected element |
| Delete Element | `Del` | Remove the selected element |
| Bring Forward | | Increase z-order by 1 |
| Send Backward | | Decrease z-order by 1 |
| Clear All Elements | | Remove everything from the canvas |

### View
| Item | Action |
|---|---|
| Choose Theme… | Open the theme picker |
| Load BG Image… | Load a PNG/JPG as a canvas reference image |
| Clear BG Image | Remove the background reference image |

### Tools  *(advanced features — hidden from novices)*
| Item | Action |
|---|---|
| Romlist Editor… | Full romlist editor in its own window |
| CFG Generator… | Emulator config generator |
| Reference… | Squirrel + AM+ API reference |
| AM+ Docs… | Renders Layouts.md from your AM+ install |
| Snippet Manager… | Browse and insert reusable code snippets |

### Help
| Item | Action |
|---|---|
| Help & Reference | Built-in help popup |
| Check for Updates / Website | Opens the project website |
| About | Version, credits, website link |

---

## Toolbar

Five core buttons always visible at the top:

| Button | Shortcut | Action |
|---|---|---|
| 📂 Load .nut | `Ctrl+O` | Load a layout file |
| 💾 Save .nut | `Ctrl+S` | Save the layout code |
| 🗑 Clear | | Remove all elements |
| ▶ Preview | | Launch AM+ with the current layout |
| 🎨 Theme | | Choose a colour theme |

> All buttons have **tooltips** — hover to see what each one does.

---

## Resolution Bar

Set the layout canvas size:

- **W / H** — type width and height directly
- **Presets** — dropdown: 640×480 up to 3840×2160
- **Canvas Zoom** — slider to scale the preview (0.1–1.0)

---

## Canvas

The centre panel is a live **scaled preview** of your layout.

| Action | Result |
|---|---|
| Click an element | Select it |
| Drag an element | Reposition it |
| Drag the orange corner handle | Resize it |
| Right-click an element | Context menu — delete, duplicate, z-order |

### Background Reference Image

Drop a PNG/JPG screenshot of your cabinet onto the canvas as a visual guide.  
It does **not** affect the generated `.nut` code.

| Control | Action |
|---|---|
| 📂 Load BG Image | File dialog — pick any PNG/JPG |
| View > Load BG Image… | Same via menu |
| Show BG checkbox | Toggle visibility |
| Opacity slider | 0–100%, default 40% |
| 🗑 Clear BG | Remove the image |
| Drag file onto canvas | Loads as BG *(if no image element selected)* |

> **Tip:** Drag a file onto the canvas while an **image** element is selected to assign the PNG to that element instead.

---

## Left Panel

### Elements Tab

Click a type to select it, then click **+ Add Element** — or just click the type row to add immediately.  
Hover any row to see a description tooltip. The selected type stays highlighted.

| Type | Description |
|---|---|
| `artwork` | Generic artwork slot (custom path name) |
| `boxart` | Box / cover artwork |
| `fanart` | Fan-made background art |
| `flyer` | Promotional flyer artwork |
| `image` | **Static PNG/JPG** — frames, overlays, bezels, logos |
| `marquee` | Arcade cabinet marquee strip |
| `shader_layer` | GLSL shader effect overlay |
| `snap` | Current game screenshot |
| `surface` | Layered offscreen render surface |
| `text` | Meta token or custom string |
| `video` | Video preview clip |
| `wheel` | Game logo / wheel art |

**Element List** buttons:

| Button | Action |
|---|---|
| ↑ / ↓ | Change z-order |
| ⊕ Dupe | Duplicate selected element |
| ✕ Del | Delete selected element |

> The panel is split by a draggable sash — resize the type picker vs the element list.

---

### Modules Tab

Check any module to include `fe.load_module("name")` in the output.  
Hover a module name to see its description in a tooltip.  
The selected module row stays highlighted until you uncheck it.

---

### Snippets Tab

Browse and insert reusable `.txt` code snippets into the layout.nut editor.

| Control | Action |
|---|---|
| 📂 Open Folder | Load a folder of `.txt` snippet files |
| 🔄 Reload | Refresh the file list |
| Category buttons | Filter: All / wheel / snap / meta / text / other |
| 🔍 Search | Filter by filename |
| Single-click | Preview the snippet with syntax highlighting |
| Double-click | Insert into layout.nut |
| ⎘ Insert | Insert selected snippet |
| 📋 Copy | Copy to clipboard |
| 📄 Open | Open file in default editor |

The **IN LAYOUT** section tracks snippets added. Double-click to edit, ✕ to remove.

> A `snippets/` folder next to the script is auto-loaded on startup if it exists.  
> All three panes (list / preview / added) have draggable sashes.

---

## Right Panel

### Properties Tab

All fields update the `layout.nut` code live.

#### Position & Size
`Name` · `X` · `Y` · `Width` · `Height` · `Rotation` · `Z-Order`

> Z-Order is written to the `.nut` file. Changing it updates the draw order.

#### Image File *(image type only)*
- File path entry + **Browse** button
- Or drag a PNG/JPG onto the canvas while an image element is selected

#### Snap / Video Transforms *(snap and video only)*
| Field | Description |
|---|---|
| Pinch X | Pinch corners horizontally e.g. `0.3` |
| Pinch Y | Pinch corners vertically e.g. `0.3` |
| Skew X | Skew horizontally e.g. `0.2` |
| Skew Y | Skew vertically e.g. `0.1` |

#### RGB Tint *(snap, video, image)*
`Red` · `Green` · `Blue` — 0–255.  
Default `255,255,255` = no tint (omitted from `.nut`).

#### Appearance
`Alpha (0–255)` · `Blend Mode` · `Visible` · `Preserve Aspect Ratio` · `No Audio`

#### Text *(text type only)*
**Meta Token** dropdown — all AM+ magic tokens:

| Category | Tokens |
|---|---|
| Game info | `[Title]` `[TitleFull]` `[Year]` `[Manufacturer]` `[Category]` `[Players]` `[Rating]` `[Series]` `[RomName]` `[CloneOf]` `[AltTitle]` `[Language]` `[Region]` `[Status]` `[Control]` `[PlayedCount]` `[PlayedTime]` `[EmulatorName]` `[SystemName]` |
| Navigation | `[ListSize]` `[ListEntry]` `[FilterName]` |
| Clock | `[!%H:%M]` `[!%H:%M:%S]` `[!%d/%m/%Y]` `[!%A, %d %B %Y]` |
| Screen | `[ScreenWidth]` `[ScreenHeight]` |
| Custom | `-- custom --` *(reveals a free-text entry)* |

**Font** — dropdown of 35 fonts (also editable for custom names):
- Sans-serif: Arial, Verdana, Tahoma, Calibri, Trebuchet MS, Century Gothic, Franklin Gothic
- Serif: Times New Roman, Georgia, Palatino, Garamond
- Monospace: Courier New, Consolas, Lucida Console
- Arcade/Display: Impact, Agency FB, Bebas Neue, Oswald, Righteous
- Pixel/Retro: Press Start 2P, VT323, 04b\_03

**Font Size** — dropdown (12–128), also editable.  
**Align** · **Font Color** picker

#### Animation
`Enable Animation` · `Trigger` · `Duration (ms)`

---

### layout.nut Tab

Live-updating Squirrel code with syntax highlighting.

| Button | Action |
|---|---|
| 📋 Copy | Copy all code to clipboard |
| 💾 Save .nut | Save to a file |
| ▶ Preview | Launch AM+ with the current layout |
| ↺ Regenerate | Rebuild code from visual elements *(discards manual edits)* |
| 🏷 Layout Info | Set name, author, version, date, notes for the file header |
| Auto-update | Toggle live regeneration when properties change |

> Once you type in the code editor, auto-update stops overwriting your edits.  
> Click **↺ Regenerate** to go back to auto-generated code.

#### Layout Info Header

Fields written into the top of `layout.nut`:

```squirrel
//////////////////////////////////////////////////////////////
//  My Arcade Layout
//  Author  : Your Name Here
//  Version : 1.0
//  Date    : 05-26-2026
//  Notes   : 16:9 widescreen layout
//  Generated by Attract-Mode Plus Layout Designer
//////////////////////////////////////////////////////////////
```

- **Today** button fills the date automatically
- Live preview updates as you type

---

## Tools Menu Windows

Each tool opens in its own full-size resizable window.

### Romlist Editor
| Feature | Details |
|---|---|
| 📂 Open | Load a `.romlist` file |
| 💾 Save / Save As | Write changes to disk |
| ✎ Bulk Edit | Set an entire column to one value |
| + Add Row / ✕ Del Row | Add or remove rows |
| 🔍 Search | Filter rows live |
| Double-click cell | Edit inline |
| Right-click | Bulk edit column shortcut |

### CFG Generator

Generate an `attract.cfg` emulator entry.

| Field | Notes |
|---|---|
| Emulator | MAME, RetroArch, or Other |
| System | Pre-filled list per emulator |
| ROM Extensions | e.g. `.zip .7z` |
| Executable / Args | For Other emulator type |
| Artwork Folders | Checkboxes with All/None shortcuts |
| `nb_mode_wait` | e.g. `10` |
| `import_extras` | e.g. `$PROGDIR\extras\extras.txt` |

The preview is **editable** before saving. Click **↺ Regenerate** to rebuild from fields.  
Emulator website links open official download pages (MAME, RetroArch, PCSX2, RPCS3, Dolphin, Cemu, Ryujinx, Duckstation, PPSSPP, FBNeo, ScummVM, DOSBox).

### Reference
Searchable Squirrel + AM+ API reference with syntax-highlighted examples.  
**⎘ Insert** puts a snippet into the layout.nut editor.

### AM+ Docs
Loads and renders `Layouts.md`. Searchable by section, copyable.

### Snippet Manager
Same as the Snippets tab in the left panel — available here as a full-size popup.

---

## ▶ Preview

Launches **Attract-Mode Plus** with the current layout — no manual save needed first.

### Setup

**Option A** — drop `attractplus.exe` into the `preview/` folder next to the script. Auto-detected.

**Option B** — click ▶ Preview, use the Browse dialog to locate `RunMe.exe`. Saved to `preview/attract_exe.cfg` for future sessions.

### Folder structure

```
preview/
  attractplus.exe        ← AM+ binary
  layouts/
    test/                ← created automatically
      layout.nut         ← written fresh on every preview
  romlists/              ← optional test romlists
```

> The layout folder name is taken from where you last saved your `.nut`, defaulting to `test`.

---

## 🎨 Themes

8 built-in colour schemes — **View > Choose Theme** or the toolbar button.  
The active theme is marked with **✓**.

| Theme | Style |
|---|---|
| Arctic Light | Light blue-grey — default |
| Slate Pro | Dark blue-grey |
| Cyan Night | Dark with cyan accents |
| Amber Dark | Dark with amber/orange |
| Green Matrix | Dark green terminal style |
| Purple Haze | Dark with purple/pink |
| Red Alert | Dark with red accents |
| Warm Mocha | Dark warm brown/tan |

Each theme switches CTK between light and dark appearance mode automatically.

---

## Output

Save your `layout.nut` and place it in:

**Linux / Mac:**
```
~/.attract/layouts/YOUR_LAYOUT_NAME/layout.nut
```

**Windows:**
```
%USERPROFILE%\AppData\Roaming\attract\layouts\YOUR_LAYOUT_NAME\layout.nut
```


Clicking **Help > Check for Updates / Website** opens this URL in the browser.

---

## Credits

Built with ❤️ by **JJTheKing**  
AI assistance: Claude & DeepSeek  
Wheel code snippets: **Tankman3737**
Feedback: **Oomek , Chadnaut , PaCiFiKbAllA**



Color Changer
<img width="332" height="474" alt="image" src="https://github.com/user-attachments/assets/7c577d0c-ac21-43a7-afc1-3d72094d1354" />

Romlist Editor (With Bulk Edit)
<img width="1919" height="1011" alt="image" src="https://github.com/user-attachments/assets/8ddb866c-9fd2-4dee-b630-32d404045a2f" />

Emulator cfg Generator
<img width="1919" height="935" alt="image" src="https://github.com/user-attachments/assets/ebbe6b29-8274-4f0c-8934-57089cc6a5b5" />



