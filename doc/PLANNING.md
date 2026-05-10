# Command Launcher — Feature Specification

## Overview

Command Launcher is a desktop launcher that manages and executes local scripts (`.bat`, `.sh`, `.ps1`, `.command`, `.app`, etc.) organized into categories.

Primary targets are DCC and game-dev pipelines such as Maya, Houdini, and Unreal Engine.

---

## Features

### 1. Category Management

Scripts are grouped into categories displayed in a left sidebar.

Each category has:

- Name
- Icon color (hex color code)
- Icon image path (optional)

---

### 2. Menu Item List

Items belonging to the selected category are shown in a scrollable center panel.

Each item displays:

- Icon (image or colored initial letter)
- Name
- Description

Each item has the following actions:

- **▶ Run** — executes the script immediately
- **Open** — reveals the script file in the system file manager

---

### 3. Single Execution

Clicking **▶** on a menu item runs that script.

Supported file types and their execution methods:

| File type | Windows | macOS |
|-----------|---------|-------|
| `.bat` | `cmd /c` | — |
| `.ps1` | `powershell -ExecutionPolicy Bypass -File` | — |
| `.exe` | direct | — |
| `.sh` | — | `bash` |
| `.command` | — | `bash` |
| `.app` | — | `open` |

---

### 4. Multi-Selection

Items can be selected with modifier keys:

- **Click** — select only the clicked item (clears previous selection)
- **Cmd / Ctrl + Click** — toggle the clicked item individually
- **Shift + Click** — select the range from the anchor to the clicked item

At least one item is always selected.

The anchor is updated on plain click or Cmd/Ctrl+Click. Shift+Click does not move the anchor.

---

### 5. Bulk Execution

The **▶ Run Selected** button in the bulk action bar runs all selected items sequentially.

The selected count is shown in both the bulk action bar and the footer.

---

### 6. Open in File Manager

The **Open** button in each menu item reveals the script file in the system file manager.

- Windows: `explorer /select,<path>`
- macOS: `open -R <path>`

---

### 7. Detail Panel

Selecting an item shows its details in the right panel.

Displayed information:

- Name
- Script path (read-only)
- Args (read-only)
- Script content (read-only code editor with line numbers)

When multiple items are selected, the first selected item is shown in the detail panel.

For file types that cannot be previewed (e.g., `.exe`, `.app`), the editor shows a notice message instead of file content.

---

## Data Format

Registration data is stored in a JSON file passed as a startup argument.

```json
{
  "Categories": [
    {
      "Name": "Maya",
      "IconColor": "#14adc7",
      "IconPath": "",
      "Items": [
        {
          "Name": "Maya 2026",
          "IconColor": "",
          "IconPath": "",
          "Description": "Launch Maya 2026",
          "ScriptPath": "/path/to/launch_maya.sh",
          "Args": ""
        }
      ]
    }
  ]
}
```

### Field reference

| Field | Required | Description |
|-------|----------|-------------|
| `Name` | Yes | Display name |
| `IconColor` | No | Hex color for the initial-letter icon (e.g. `#ff6108`) |
| `IconPath` | No | Path to an icon image file |
| `Description` | Yes | Short description shown under the name |
| `ScriptPath` | Yes | Absolute or `{APP_ROOT_DIR}`-relative path to the script |
| `Args` | No | Arguments passed to the script at execution |

`{APP_ROOT_DIR}` is resolved to the repository root at runtime.

---

## Planned Features

- New script creation from within the app
- Single and bulk delete (registration only; actual files are not deleted by default)
- In-app script editing and saving
