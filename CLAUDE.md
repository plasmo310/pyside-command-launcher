# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**Command Launcher** is a PySide6 desktop app that manages and executes local scripts (`.bat`, `.sh`, `.ps1`, `.command`) organized into categories. Primary target users are DCC/game-dev pipelines (Maya, Houdini, Unreal Engine, etc.).

## Setup and running

**First time (Windows):**
```
scripts\win\Setup.bat
```
Downloads Python 3.13.13 via NuGet into `bin/`, creates `.venv`, installs `requirements.txt`.

**First time (macOS/Linux):**
```
bash scripts/mac/Setup.sh
```
Uses system Python 3.13.13, creates `.venv`, installs requirements.

**Run the app:**
```
# Windows
scripts\win\LaunchApp.bat

# macOS/Linux
bash scripts/mac/LaunchApp.sh
```

Both scripts set `PYTHONPATH=<repo root>/python` and run `python -m cmdlaunch.main <json_path>`. The default JSON is `resources/data/ItemData_Sample.json`.

**Run manually (with venv activated):**
```
PYTHONPATH=python python -m cmdlaunch.main resources/data/ItemData_Sample.json   # macOS/Linux
$env:PYTHONPATH="python"; python -m cmdlaunch.main resources/data/ItemData_Sample.json  # PowerShell
```

## Linting

Ruff is configured in `pyproject.toml` for isort (first-party: `cmdlaunch`). Run with:
```
ruff check python/
ruff format python/
```

## Architecture

The source lives entirely under `python/cmdlaunch/` with `PYTHONPATH` pointing at `python/`.

```
python/cmdlaunch/
├── main.py              # QApplication setup, stylesheet loading, entry point
├── tool_config.py       # Static config: app title, resource paths
└── gui/
    ├── main_model.py    # Data layer: ScriptItem, Category dataclasses + MainModel
    ├── main_view.py     # MainView (QMainWindow): composes the three panels
    ├── main_controller.py  # Wires model ↔ view via Qt signals/slots
    └── widgets/
        ├── category_panel.py  # Left sidebar: list of categories (emits category_selected)
        ├── category_item.py   # Single row in category sidebar
        ├── menu_panel.py      # Center panel: scrollable list of script items
        ├── menu_item.py       # Single script row (run/open/delete buttons)
        ├── detail_panel.py    # Right panel: path + code editor + edit/save actions
        └── icon_button.py     # 42×42 QToolButton with normal/danger variants
```

**MVC pattern:** `MainController` owns `MainModel` and `MainView`. It calls model methods and routes view signals to handlers. Views emit typed Qt signals; widgets never call model methods directly.

**Styling:** All visual styling is in `resources/ui/stylesheet.qss`. Widgets are styled by `objectName` (e.g., `#CategoryPanel`, `#ButtonBlue`). Dynamic state (selected/unselected) uses Qt properties (`isSelected`) — after changing a property call `style().unpolish(w); style().polish(w)` to force a repaint.

**Data:** `MainModel` loads data from a JSON file passed as a startup argument. The JSON schema has a `categories` array, each with `name`, `icon_color`, and `items` (array of `name`, `description`, `script_path`, `file_type`).

## Testing

When running Python tests, always set `PYTHONDONTWRITEBYTECODE=1` to prevent `__pycache__` creation:

```
# PowerShell
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest python/

# macOS/Linux
PYTHONDONTWRITEBYTECODE=1 python -m pytest python/
```

## Rules

- **Never leave `__pycache__` behind.** Always run every `python` command with `PYTHONDONTWRITEBYTECODE=1`, regardless of whether it is a smoke-test, unit test, or general execution. If any `__pycache__` directory is found under `python/` after a run, delete it immediately.

### Coding conventions

**Naming:**
- Never abbreviate variable or function names; names must be self-explanatory.
- Variables and fields of type `list` must have a `_list` suffix.
- Variables and fields of type `dict` must have a `_dict` suffix.
- Variables that hold a class instance must include the class name.
  - e.g. `list[CategoryItemInfo]` → `category_item_info_list`
  - e.g. a JSON element treated as `dict` → `category_item_info_dict`

**Access modifiers:**
- Private methods of a class must be prefixed with `__` (double underscore).
- Private fields of a class must also be prefixed with `__`.
- Module-level private functions and variables use a single `_` prefix.

**UI event handlers:**
- Functions bound to UI events must follow the pattern `__on_<verb>_<ui_name>`.
  - e.g. `__on_click_new_button`, `__on_select_category`, `__on_run_menu_item`

**Signal naming:**
- Signal variables must follow the pattern `on_<verb>_<action>_signal`.
  - e.g. `on_click_run_signal`, `on_select_category_signal`, `on_run_item_signal`

**Styling:**
- Never use `setObjectName()`.
- Apply QSS styles via `setProperty("class", "<value>")` in Python, and select with `[class="<value>"]` in QSS.
  - e.g. Python: `widget.setProperty("class", "ButtonBlue")` / QSS: `QPushButton[class="ButtonBlue"] { ... }`

## Key implementation notes

- `PYTHONDONTWRITEBYTECODE=1` is set by the launch scripts — no `__pycache__` is written during normal use.
- The category icon color is applied as an inline stylesheet on each `CategoryItem` because it is data-driven; it cannot come from the `.qss` file.
- `DetailPanel.__load_script_content` currently returns mock content and needs to be replaced with real file reading when the persistence layer is added.
- Script execution handlers in `MainController` (`__handle_run_item`, `__handle_run_selected`, etc.) are stubs that only `print()`; actual subprocess execution is not yet implemented.
