import argparse
import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .gui.main_controller import MainController
from .tool_config import ToolConfig


def parse_args() -> argparse.Namespace:
    """起動時引数取得"""
    parser = argparse.ArgumentParser(description="Command Launcher")
    parser.add_argument(
        "--json-path",
        type=str,
        required=False,
        help="Path to the item data JSON file",
    )
    return parser.parse_args()


def load_stylesheet() -> str:
    """スタイルシート読込"""
    stylesheet_path = os.path.join(ToolConfig.get_stylesheet_dir(), "stylesheet.qss")
    if os.path.exists(stylesheet_path):
        try:
            with open(stylesheet_path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            with open(stylesheet_path, "r", encoding="utf-8-sig") as file:
                return file.read()
    return ""


def main():
    """メイン処理"""
    # パラメータ読込
    args = parse_args()
    json_file_path = args.json_path

    # 指定されていたら上書き
    if json_file_path:
        if not os.path.isfile(json_file_path):
            raise FileNotFoundError(f"JSON file not found: {json_file_path}")
        ToolConfig.set_json_file_path(json_file_path)

    # Application作成
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ToolConfig.get_tool_icon_path()))
    app.setStyle("Fusion")
    stylesheet = load_stylesheet()
    if stylesheet:
        app.setStyleSheet(stylesheet)

    # ツール起動
    controller = MainController(json_path=ToolConfig.get_json_file_path())
    controller.launch()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
