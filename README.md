<img width="1536" height="1024" alt="AMP-LD" src="https://github.com/user-attachments/assets/71ab12a0-6af4-489d-8edb-b6c0809a0256" />

# ⚡ Attract-Mode Plus — Layout Designer

A visual drag-and-drop layout builder for **Attract-Mode Plus** frontends.  
Build, preview, and export `layout.nut` files without writing Squirrel script by hand.

---

## Requirements

```
Windows 10/11
```

| Package | Purpose |
|---|---|
| `customtkinter` | Modern CTK UI widgets |
| `pillow` | Background reference images + image element rendering |
| `tkinterdnd2` | Drag-and-drop PNG/JPG files onto the canvas *(optional — button fallback included)* |

Run with:
```
Attract-Mode Plus - Layout Designer-TKK.exe
```

---

## Top Toolbar

| Button | Action |
|---|---|
| 💾 Save .nut | Save the current layout.nut code |
| 📂 Load .nut | Load an existing layout.nut file |
| 🗑 Clear All | Remove all elements and reset the layout |
| 🎨 Theme | Choose a colour theme |
| 📋 Romlist | Open the Romlist Editor in its own window |
| ❓ Help | Open the built-in help reference |

---

## Canvas

The centre panel is a live **scaled preview** of your layout.

| Action | Result |
|---|---|
| Click an element | Select it |
| Drag an element | Reposition it |
| Drag the orange corner handle | Resize it |
| Right-click an element | Context menu — delete, duplicate, z-order |
| Mouse wheel | Scroll the canvas |
| **Zoom slider** *(resolution bar)* | Scale the canvas preview |
| **W / H fields** | Set layout resolution |
| **Preset dropdown** | Pick a standard resolution (640×480 → 3840×2160) |

### Background Reference Image

Drop a PNG/JPG screenshot of your cabinet or monitor onto the canvas to use as a visual guide — it does **not** affect the generated `.nut` code.

| Control | Action |
|---|---|
| 📂 Load BG Image | File dialog to pick a PNG/JPG |
| Show BG checkbox | Toggle visibility |
| Opacity slider | 0–100 %, defaults to 40 % |
| 🗑 Clear BG | Remove the image |
| Drag a file onto the canvas | Loads as background *(if no image element selected)* |

> **Tip:** If an **image** element is selected when you drag a file onto the canvas, the file is assigned to that element instead of the background.

---

## Left Panel

### Elements Tab

Select an element type and click **+ Add Element** to place it on the canvas.

Hover any type name to see a tooltip description.

| Type | Description |
|---|---|
| `snap` | Current game screenshot |
| `wheel` | Game logo / wheel art |
| `boxart` | Box / cover artwork |
| `marquee` | Arcade cabinet marquee strip |
| `flyer` | Promotional flyer artwork |
| `fanart` | Fan-made background art |
| `video` | Video preview clip |
| `text` | Meta token or custom string |
| `image` | **Static PNG/JPG** — frames, overlays, bezels, logos |
| `surface` | Layered offscreen render surface |
| `artwork` | Generic artwork (custom slot name) |
| `shader_layer` | GLSL shader effect overlay |

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
Hover a module name to see its description and file name in a tooltip.

Included modules cover: `animate`, `blur`, `config`, `conveyor`, `fade`, `file`, `flow`, `gtc`, `inertia`, `mask`, `math`, `objects`, `perspective`, `pan_and_scan`, `surface`, `wheel`, and more.

---

### CFG Gen Tab

Generate an `emulator.cfg` emulator entry.

**Fields:**

| Field | Notes |
|---|---|
| Emulator | MAME, RetroArch, or Other |
| System | Pre-filled list per emulator |
| ROM Extensions | e.g. `.zip .7z` |
| Executable Path | For Other emulator type |
| Arguments | For Other emulator type |
| Artwork Folders | Checkboxes — All / None shortcuts |
| `nb_mode_wait` | e.g. `10` |
| `import_extras` | e.g. `$PROGDIR\extras\extras.txt` |

The **PREVIEW** pane shows live-updating config text. You can **edit it directly** before saving — your changes are preserved. Click **↺ Regenerate** to rebuild from the fields above.

**Emulator Website Links** — 12 buttons open official download pages in your browser:  
MAME · RetroArch · PCSX2 · RPCS3 · Dolphin · Cemu · Ryujinx · Duckstation · PPSSPP · FBNeo · ScummVM · DOSBox

---

### Snippets Tab

Browse and insert reusable `.txt` code snippets.

| Control | Action |
|---|---|
| 📂 Open Folder | Load a folder of `.txt` snippet files |
| 🔄 Reload | Refresh the file list |
| Filter buttons | Filter by category: All / wheel / snap / meta / text / other |
| 🔍 Search | Filter by name |
| Single-click | Preview the snippet |
| Double-click | Insert into layout.nut |
| ⎘ Insert | Insert selected snippet |
| 📋 Copy | Copy to clipboard |
| 📄 Open | Open file in default editor |

The **IN LAYOUT** list tracks snippets added to the current session. Double-click to edit, ✕ Remove / ✕ All to remove.

> All three panes (file list, preview, added list) are split by draggable sashes.

> A `snippets/` folder next to the script is auto-loaded on startup if it exists.

---

## Right Panel

### Properties Tab

All fields update the `layout.nut` code live as you edit.

#### Position & Size
`Name` · `X` · `Y` · `Width` · `Height` · `Rotation` · `Z-Order`

> Z-Order is written to the `.nut` file and controls draw order.

#### Image File *(image type only)*
- **File Path** entry + **Browse** button
- Or drag a PNG/JPG onto the canvas while the element is selected

#### Snap / Video Transforms *(snap and video only)*
| Field | Description |
|---|---|
| Pinch X | Pinch the corners horizontally e.g. `0.3` |
| Pinch Y | Pinch the corners vertically e.g. `0.3` |
| Skew X | Skew horizontally e.g. `0.2` |
| Skew Y | Skew vertically e.g. `0.1` |

#### RGB Tint *(snap, video, image)*
`Red` · `Green` · `Blue` — 0–255 each.  
Default `255, 255, 255` = no tint (not written to `.nut`).

#### Appearance
`Alpha (0–255)` · `Blend Mode` · `Visible` · `Preserve Aspect Ratio` · `No Audio`

#### Text *(text type only)*
**Meta Token** dropdown — pick from all AM+ magic tokens:

| Category | Tokens |
|---|---|
| Game info | `[Title]` `[TitleFull]` `[Year]` `[Manufacturer]` `[Category]` `[Players]` `[Rating]` `[Series]` `[RomName]` `[CloneOf]` `[AltTitle]` `[Language]` `[Region]` `[Status]` `[Control]` `[PlayedCount]` `[PlayedTime]` `[EmulatorName]` `[SystemName]` |
| Navigation | `[ListSize]` `[ListEntry]` `[FilterName]` |
| Clock | `[!%H:%M]` `[!%H:%M:%S]` `[!%d/%m/%Y]` `[!%A, %d %B %Y]` |
| Screen | `[ScreenWidth]` `[ScreenHeight]` |
| Custom | `-- custom --` *(reveals a free-text field)* |

**Font** — dropdown of 35 fonts across 5 categories (also editable for custom font names):
- Sans-serif: Arial, Verdana, Tahoma, Calibri, Trebuchet MS, Century Gothic, Franklin Gothic
- Serif: Times New Roman, Georgia, Palatino, Garamond
- Monospace: Courier New, Consolas, Lucida Console
- Arcade/Display: Impact, Agency FB, Bebas Neue, Oswald, Righteous
- Pixel/Retro: Press Start 2P, VT323, 04b\_03

**Font Size** — dropdown (12–128) also editable for any value.

**Align** · **Font Color** picker

#### Animation
`Enable Animation` · `Trigger` · `Duration (ms)`

---

### layout.nut Tab

Live-updating Squirrel code with syntax highlighting.

| Button | Action |
|---|---|
| 📋 Copy | Copy all code to clipboard |
| 💾 Save .nut | Save the code to a file |
| ▶ Preview | Launch Attract-Mode Plus with the current layout |
| ↺ Regenerate | Rebuild code from visual elements *(discards manual edits)* |
| 🏷 Layout Info | Set name, author, version, date, notes for the file header |
| Auto-update | Toggle live regeneration from properties panel changes |

> Once you type directly in the code editor, auto-update stops overwriting your edits.  
> Click **↺ Regenerate** to go back to auto-generated code at any time.

#### 🏷 Layout Info
Fields written into the header comment of `layout.nut`:

```
//////////////////////////////////////////////////////////////
//  My Arcade Layout
//  Author  : Your Name Here
//  Version : 1.0
//  Date    : 2025-04-30
//  Notes   : 16:9 widescreen layout
//  Generated by Attract-Mode Plus Layout Designer
//////////////////////////////////////////////////////////////
```

- **Today** button fills the date automatically
- Live preview of the header updates as you type

---

### Reference Tab

Searchable Squirrel + AM+ API reference. Click an entry to see full details with syntax-highlighted examples. **⎘ Insert** puts the code snippet into the layout.nut editor.

---

### AM+ Docs Tab

Loads and renders `Layouts.md` from your AM+ installation. Searchable, section-navigable, copyable.

---

## ▶ Preview

Launches **Attract-Mode Plus** with your current layout — no need to save manually first.

### Setup

**Option A** — drop `RunMe.exe` into the `preview/` folder next to the script. Auto-detected, no configuration needed.

**Option B** — click ▶ Preview and use the Browse dialog to locate `RunMe.exe` anywhere on your machine. Path is saved to `preview/attract_exe.cfg` for future sessions.

### Folder structure

```
preview/
  attractplus.exe          ← AM+ binary
  layouts/
    test/                  ← created automatically
      layout.nut           ← written fresh on every preview
  romlists/                ← your test romlists (optional)
```

> The layout folder name is taken from where you last saved your `.nut` file, falling back to `test`.

---

## 🎨 Themes

8 built-in colour schemes. The active theme is marked with **✓**.

| Theme | Style |
|---|---|
| Arctic Light | Light blue-grey — default |
| Slate Pro | Dark blue-grey |
| Cyan Night | Dark with cyan accents |
| Amber Dark | Dark with amber/orange |
| Green Matrix | Dark with green terminal style |
| Purple Haze | Dark with purple/pink |
| Red Alert | Dark with red accents |
| Warm Mocha | Dark warm brown/tan |

Each theme automatically switches CTK between light and dark appearance mode.

---

## 📋 Romlist Editor

Opens in its own full-size resizable window. Also accessible from the left panel Romlist tab.

| Feature | Details |
|---|---|
| 📂 Open | Load a `.romlist` file |
| 💾 Save / Save As | Write changes back to disk |
| ✎ Bulk Edit | Set an entire column to one value |
| + Add Row | Append a blank row |
| ✕ Del Row | Remove selected row |
| 🔍 Search | Filter rows live |
| Double-click cell | Edit inline |
| Right-click | Context menu — bulk edit column |

---

## Output

Save your `layout.nut` and place it in:

```
~/.attract/layouts/YOUR_LAYOUT_NAME/layout.nut
```

Or on Windows:
```
%USERPROFILE%\AppData\Roaming\attract\layouts\YOUR_LAYOUT_NAME\layout.nut
```

---

## Credits

Built with ❤️ by **JJTheKing**  
AI assistance: Claude & DeepSeek  
Wheel code snippets: **Tankman3737**
Feedback: **Oomek**
Feedback: **PaCiFiKbAllA**
Version: 5.9


Color Changer
<img width="332" height="474" alt="image" src="https://github.com/user-attachments/assets/7c577d0c-ac21-43a7-afc1-3d72094d1354" />

Romlist Editor (With Bulk Edit)
<img width="1919" height="1011" alt="image" src="https://github.com/user-attachments/assets/8ddb866c-9fd2-4dee-b630-32d404045a2f" />

Emulator cfg Generator
<img width="1919" height="935" alt="image" src="https://github.com/user-attachments/assets/ebbe6b29-8274-4f0c-8934-57089cc6a5b5" />



