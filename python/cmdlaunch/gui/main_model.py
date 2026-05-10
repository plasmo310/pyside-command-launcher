import os
import shlex
import subprocess
from typing import List

from cmdlaunch.data.item_info import (
    CategoryItemInfo,
    CommandItemInfo,
    load_category_item_info_list_from_dict,
)
from cmdlaunch.definitions import CommandType, PlatformType
from cmdlaunch.logger import get_tool_logger
from cmdlaunch.tool_config import ToolConfig
from cmdlaunch.utilities.json_utility import JsonUtility

__logger = get_tool_logger()


class MainModel:
    """メイン画面 Modelクラス

    Attributes:
        __category_item_info_list (List[CategoryItemInfo]): カテゴリアイテム情報リスト
    """

    def __init__(self, json_path: str):
        self.__category_item_info_list: List[CategoryItemInfo] = self.__load_from_json(
            json_path
        )

    @staticmethod
    def __load_from_json(json_path: str) -> List[CategoryItemInfo]:
        """カテゴリアイテム情報JSONファイルの読込

        Args:
            json_path (str): JSONファイルパス

        Returns:
            List[CategoryItemInfo]: カテゴリアイテム情報リスト
        """
        json_data_dict = JsonUtility.load_json(json_path)
        category_item_info_list = load_category_item_info_list_from_dict(json_data_dict)
        for category_item_info in category_item_info_list:
            if category_item_info.icon_path:
                category_item_info.icon_path = ToolConfig.resolve_script_path(
                    category_item_info.icon_path
                )
            for command_item_info in category_item_info.command_item_info_list:
                command_item_info.script_path = ToolConfig.resolve_script_path(
                    command_item_info.script_path
                )
                if command_item_info.icon_path:
                    command_item_info.icon_path = ToolConfig.resolve_script_path(
                        command_item_info.icon_path
                    )
        return category_item_info_list

    @property
    def category_item_info_list(self) -> List[CategoryItemInfo]:
        """カテゴリアイテム情報リスト"""
        return self.__category_item_info_list

    @property
    def first_category_item_info(self) -> CategoryItemInfo | None:
        """最初のカテゴリアイテム情報"""
        return (
            self.__category_item_info_list[0]
            if self.__category_item_info_list
            else None
        )

    def get_script_content(self, script_path: str) -> str | None:
        """スクリプト内容の読込

        Args:
            script_path (str): スクリプトファイルパス

        Returns:
            str: ファイル内容 / None: 非対応形式 / "": ファイルなし
        """
        extention = os.path.splitext(script_path)[1].lower()
        file_type = CommandType.from_extension(extention)
        if file_type not in CommandType.viewable_types():
            return None

        if not os.path.isfile(script_path):
            return ""

        with open(script_path, encoding="utf-8", errors="replace") as f:
            return f.read()

    def run_command(self, command_item_info: CommandItemInfo) -> None:
        """コマンド実行処理

        Args:
            command_item_info (CommandItemInfo): コマンドアイテム情報
        """
        script_path = os.path.normpath(command_item_info.script_path)
        extention = os.path.splitext(script_path)[1].lower()
        command_type = CommandType.from_extension(extention)

        # .app はディレクトリ形式のバンドルなので isdir で存在確認する
        if command_type == CommandType.APP:
            if not os.path.isdir(script_path):
                return
        elif not os.path.isfile(script_path):
            return
        args_list = (
            shlex.split(command_item_info.args)
            if command_item_info.args.strip()
            else []
        )

        # プラットフォーム別に実行処理を行う
        platform_type = PlatformType.current()

        # Windows
        if platform_type == PlatformType.WINDOWS:
            if command_type == CommandType.PS1:
                cmd = [
                    "powershell",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    script_path,
                    *args_list,
                ]
                subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

            elif command_type == CommandType.EXE:
                subprocess.Popen([script_path, *args_list])

            elif command_type == CommandType.BAT:
                subprocess.Popen(
                    ["cmd", "/c", script_path, *args_list],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                )

            else:
                __logger.warning("Unsupported command type on Windows: %s", script_path)

        # Mac
        elif platform_type == PlatformType.MAC:
            if command_type == CommandType.SHELL or command_type == CommandType.COMMAND:
                # ターミナルにログを出すためosascriptで実行
                # subprocess.Popen(["bash", script_path, *args_list])
                bash_cmd = (
                    shlex.join(["bash", script_path, *args_list])
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                )
                subprocess.Popen(
                    [
                        "osascript",
                        "-e",
                        f'tell application "Terminal"\ndo script "{bash_cmd}"\nactivate\nend tell',
                    ]
                )

            elif command_type == CommandType.APP:
                if args_list:
                    subprocess.Popen(["open", script_path, "--args", *args_list])
                else:
                    subprocess.Popen(["open", script_path])

            else:
                __logger.warning(
                    "Unsupported command type on %s: %s",
                    platform_type.name,
                    script_path,
                )
        else:
            __logger.warning("Unsupported platform: %s", platform_type.name)

    def reveal_in_file_manager(self, script_path: str) -> None:
        """ファイルマネージャーでスクリプトファイルを選択表示

        Args:
            script_path (str): スクリプトファイルパス
        """
        if not script_path:
            return
        normalized_path = os.path.normpath(script_path)
        platform_type = PlatformType.current()
        if platform_type == PlatformType.WINDOWS:
            subprocess.Popen(["explorer", f"/select,{normalized_path}"])

        elif platform_type == PlatformType.MAC:
            subprocess.Popen(["open", "-R", normalized_path])

        else:
            __logger.warning("Unsupported platform: %s", platform_type.name)
