<a href="/README.ja.md">日本語版ドキュメントはこちら</a>

# Command Launcher

A general-purpose launcher tool for registering and executing scripts such as batch files and shell scripts.  
Supports category organization and argument configuration, making it ideal for switching between multiple DCC tool environments.

<img src="doc/ReadMeContents/01_command_launcher.png" width="800">

## Requirements

Available on Windows and macOS.

- Verified OS versions
  - Windows 11
  - macOS 15.3.2

## Supported Script Formats

| Extension  | Windows | macOS |
| ---------- | ------- | ----- |
| `.bat`     | ✓       | —     |
| `.ps1`     | ✓       | —     |
| `.exe`     | ✓       | —     |
| `.sh`      | —       | ✓     |
| `.command` | —       | ✓     |
| `.app`     | —       | ✓     |

---

## Setup

This tool does not provide pre-built packages.</br>
Please run it directly from source or build it yourself using the steps below.

### 1. Clone the Repository

```
git clone <repository_url>
cd pyside-command-launcher
```

### 2. Set Up the Environment

Creates a virtual environment and installs the required packages.

```bat
# Windows
scripts\win\Setup.bat

# macOS
bash scripts/mac/Setup.sh
```

The setup script automatically performs the following:

- **Windows:** Downloads Python to `bin/` via NuGet and creates `.venv`
- **macOS:** Uses the system Python to create `.venv`

### 3. Launch the Tool

```bat
# Windows
scripts\win\LaunchApp.bat

# macOS
bash scripts/mac/LaunchApp.sh
```

By default, `data/<os>/ItemData.json` is loaded. To use a different JSON file, pass the path via the `--json-path` argument.

```
python -m cmdlaunch.main --json-path path/to/ItemData.json
```

The `LaunchApp_Dev` script loads `ItemData_Dev.json` instead — intended for development and testing.

---

## Usage

### Basic Operations

**1. Select a category in the left sidebar, then select a command from the center panel.**

- You can also multi-select using Shift or Ctrl.</br>When selected, the right panel displays detailed script information.

  <img src="doc/ReadMeContents/02_manual_select.png" width="400">

  | Action                  | Behavior               |
  | ----------------------- | ---------------------- |
  | Left click              | Single select          |
  | Shift + left click      | Range select           |
  | Ctrl (Cmd) + left click | Toggle individual item |

**2. Run commands using the buttons.**

- In addition to the per-row button, the top button allows batch execution of multiple commands.

  <img src="doc/ReadMeContents/03_manual_run.png" width="400">

  | Action                | Behavior                            |
  | --------------------- | ----------------------------------- |
  | ▶ button on a row     | Immediately run that command        |
  | ▶ Run Selected button | Run all currently selected commands |

**3. (Optional) Click the Open button in the right panel to reveal the script file in the file manager.**

<img src="doc/ReadMeContents/04_manual_open.png" width="400">

---

## Configuration File

Categories and commands can be freely customized by editing the JSON file.  
It is loaded at startup and defines the categories and commands displayed in the launcher.

- Windows: `data/win/ItemData.json`
- macOS: `data/mac/ItemData.json`

### JSON Schema

```json
{
  "Categories": [
    {
      "Name": "Category Name",
      "IconColor": "#ff6108",
      "IconPath": "",
      "Items": [
        {
          "Name": "Command Name",
          "IconColor": "",
          "IconPath": "",
          "Description": "Description",
          "ScriptPath": "{APP_ROOT_DIR}/data/win/scripts/sample.bat",
          "Args": "arg1 arg2"
        }
      ]
    }
  ]
}
```

**Categories**

| Field       | Description                 |
| ----------- | --------------------------- |
| `Name`      | Category name               |
| `IconColor` | Icon color (hex color code) |
| `IconPath`  | Path to the icon image      |
| `Items`     | Array of command entries    |

**Items**

| Field         | Description                      |
| ------------- | -------------------------------- |
| `Name`        | Command name                     |
| `Description` | Description text for the command |
| `ScriptPath`  | Path to the script to execute    |
| `Args`        | Arguments passed to the script   |
| `IconColor`   | Icon color (hex color code)      |
| `IconPath`    | Path to the icon image           |

### Path Placeholders

The following placeholders can be used in `ScriptPath` and `IconPath`:

| Placeholder      | Resolves to                |
| ---------------- | -------------------------- |
| `{APP_ROOT_DIR}` | Application root directory |

---

## Build (Standalone Executable)

A standalone executable (`.exe` / `.app`) can be generated using PyInstaller.  
The build environment is isolated under `build_env/` and uses a separate virtual environment from the development environment.

### Build Environment Setup (first time only)

```bat
# Windows
build_env\scripts\win\Setup.bat

# macOS
bash build_env/scripts/mac/Setup.sh
```

### Run the Build

```bat
# Windows
build_env\scripts\win\BuildApp.bat

# macOS
bash build_env/scripts/mac/BuildApp.sh
```

Build output is placed in `build_env/scripts/<os>/dist/CommandLauncher/`.

---

## Architecture Overview

Follows the MVC pattern. `MainController` mediates between `MainModel` and `MainView`.  
Widgets do not reference the model directly; they communicate via Qt signals.

```
python/cmdlaunch/
├── main.py                 # QApplication initialization and entry point
├── tool_config.py          # App settings and resource path constants
├── definitions.py          # CommandType / PlatformType enums
├── logger.py               # Logger configuration
├── data/
│   ├── item_info.py        # CategoryItemInfo / CommandItemInfo dataclasses
│   └── interface.py        # Interface for data classes
└── gui/
    ├── main_model.py        # Data layer: JSON loading and command execution
    ├── main_view.py         # MainView (QMainWindow): 3-panel layout
    ├── main_controller.py   # Connects Model and View via Qt signals/slots
    └── widgets/
        ├── category_panel.py  # Left sidebar: category list
        ├── category_item.py   # Single row in the category sidebar
        ├── menu_panel.py      # Center panel: command list
        ├── menu_item.py       # Single row in the command list (run/show buttons)
        ├── detail_panel.py    # Right panel: script preview
        └── icon_button.py     # 42×42 icon button (normal and danger variants)
```
