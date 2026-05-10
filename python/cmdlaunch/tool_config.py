import os
import sys

from cmdlaunch.definitions import PlatformType


class ToolConfig:
    """ツール設定クラス"""

    # ツールタイトル
    TOOL_TITLE = "Command Launcher"

    # コマンドラインからの強制指定用
    __force_json_path = None

    @staticmethod
    def __get_app_root_dir() -> str:
        # PyInstallerで作成した場合、exeと同階層（_internalの親）を返す
        # 参考: https://pyinstaller.org/en/stable/runtime-information.html
        if hasattr(sys, "_MEIPASS"):
            return os.path.dirname(sys._MEIPASS)
        return os.path.join(os.path.dirname(__file__), "../../")

    @staticmethod
    def __get_resources_dir() -> str:
        # PyInstallerで作成した場合、_internal/resources/ を返す
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, "resources")
        return os.path.join(os.path.dirname(__file__), "../../resources")

    @staticmethod
    def set_json_file_path(json_path: str) -> None:
        """JSONファイルパスを設定する"""
        ToolConfig.__force_json_path = json_path

    @staticmethod
    def get_json_file_path() -> str:
        """JSONファイル格納ディレクトリ"""
        # コマンドライン引数が設定されている場合
        if ToolConfig.__force_json_path:
            return ToolConfig.__force_json_path

        app_root_dir = ToolConfig.__get_app_root_dir()
        platform_type = PlatformType.current()
        if platform_type == PlatformType.MAC:
            platform_dir = "mac"

        elif platform_type == PlatformType.WINDOWS:
            platform_dir = "win"

        else:
            raise RuntimeError(f"Unsupported platform: {platform_type}")

        return os.path.abspath(
            os.path.join(app_root_dir, "data", platform_dir, "ItemData.json")
        )

    @staticmethod
    def get_stylesheet_dir() -> str:
        """stylesheet格納ディレクトリ"""
        resources_dir = ToolConfig.__get_resources_dir()
        return os.path.abspath(os.path.join(resources_dir, "ui"))

    @staticmethod
    def get_tool_icon_path() -> str:
        """ツールアイコンパス（プラットフォーム別）"""
        platform_type = PlatformType.current()
        if platform_type == PlatformType.WINDOWS:
            icon_file_name = "tool_icon_rect.ico"

        elif platform_type == PlatformType.MAC:
            icon_file_name = "tool_icon_round.icns"

        else:
            raise RuntimeError(f"Unsupported platform: {platform_type}")

        resources_dir = ToolConfig.__get_resources_dir()
        return os.path.abspath(os.path.join(resources_dir, "icon", icon_file_name))

    @staticmethod
    def get_tool_icon_svg_path() -> str:
        """ツールアイコンSVGパス"""
        resources_dir = ToolConfig.__get_resources_dir()
        return os.path.abspath(os.path.join(resources_dir, "icon", "tool_icon.svg"))

    @staticmethod
    def resolve_script_path(script_path: str) -> str:
        """{APP_ROOT_DIR} プレースホルダをアプリルートパスに置換する"""
        app_root_dir = ToolConfig.__get_app_root_dir()
        return os.path.abspath(script_path.replace("{APP_ROOT_DIR}", app_root_dir))
