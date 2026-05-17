from typing import List

from cmdlaunch.data.item_info import CategoryItemInfo, CommandItemInfo

from .main_model import MainModel
from .main_view import MainView


class MainController:
    """メイン画面 Controllerクラス"""

    def __init__(self, json_path: str):
        self.__json_path = json_path
        self.__model = MainModel(json_path=json_path)
        self.__view = MainView()
        self.__setup_connections()
        self.__init_data()

    def launch(self):
        """ツール起動"""
        self.__view.show()

    def __init_data(self):
        """初期データの設定"""

        # 最初のアイテムを選択状態にして表示する
        first_category_item_info = self.__model.first_category_item_info

        self.__view.category_panel.set_categories(
            self.__model.category_item_info_list,
            selected_category_item_info=first_category_item_info,
        )

        if first_category_item_info:
            self.__view.menu_panel.set_items(
                first_category_item_info.command_item_info_list
            )

    def __setup_connections(self):
        """Viewとの接続"""
        self.__view.category_panel.on_select_category_signal.connect(
            self.__on_select_category_item
        )
        self.__view.menu_panel.on_select_item_signal.connect(
            self.__on_select_command_item
        )
        self.__view.menu_panel.on_click_run_selected_signal.connect(
            self.__on_click_run_selected_button
        )
        self.__view.menu_panel.on_run_item_signal.connect(self.__on_run_menu_item)
        self.__view.detail_panel.on_click_open_signal.connect(
            self.__on_click_open_button
        )
        self.__view.on_click_open_settings_signal.connect(
            self.__on_click_open_settings_button
        )
        self.__view.on_click_reflesh_signal.connect(self.__on_click_reflesh_button)

    def __on_select_category_item(self, category_item_info: CategoryItemInfo):
        """カテゴリアイテム選択処理"""
        self.__view.menu_panel.set_items(category_item_info.command_item_info_list)
        if not category_item_info.command_item_info_list:
            self.__view.detail_panel.show_item(None, "")

    def __on_select_command_item(self, command_item_info: CommandItemInfo):
        """コマンドメニューアイテム選択処理"""
        script_content = self.__model.get_script_content(command_item_info.script_path)
        self.__view.detail_panel.show_item(command_item_info, script_content)

    def __on_click_run_selected_button(
        self, command_item_info_list: List[CommandItemInfo]
    ):
        """アイテム複数実行ボタン押下時処理

        Args:
            command_item_info_list (List[CommandItemInfo]): 選択しているコマンドアイテム情報リスト
        """
        for command_item_info in command_item_info_list:
            self.__model.run_command(command_item_info)

    def __on_run_menu_item(self, command_item_info: CommandItemInfo):
        """アイテム単体実行ボタン押下時処理

        Args:
            command_item_info (CommandItemInfo): コマンドアイテム情報
        """
        self.__model.run_command(command_item_info)

    def __on_click_open_button(self, script_path: str):
        """Openボタン押下時処理

        Args:
            script_path (str): スクリプトパス
        """
        self.__model.reveal_in_file_manager(script_path)

    def __on_click_open_settings_button(self):
        """Open Settingsボタン押下時処理"""
        self.__model.reveal_in_file_manager(self.__json_path)

    def __on_click_reflesh_button(self):
        """Refleshボタン押下時処理"""
        self.__model.reload()
        self.__view.detail_panel.show_item(None, "")
        self.__init_data()
