from PySide6 import QtCore, QtWidgets

from cmdlaunch.data.item_info import CommandItemInfo
from cmdlaunch.gui.widgets.menu_item import MenuItem


class MenuPanel(QtWidgets.QFrame):
    """メニューリストパネル"""

    on_click_run_selected_signal = QtCore.Signal(list)
    on_select_item_signal = QtCore.Signal(CommandItemInfo)
    on_run_item_signal = QtCore.Signal(CommandItemInfo)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "MenuPanel")
        self.setMinimumSize(QtCore.QSize(400, 1))

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 12)
        layout.setSpacing(0)

        header_label = QtWidgets.QLabel("Menu")
        header_label.setProperty("class", "PanelHeader")
        layout.addWidget(header_label)
        layout.addSpacing(12)

        layout.addWidget(self.__build_bulk_bar())
        layout.addSpacing(10)
        layout.addWidget(self.__build_scroll_area(), 1)
        layout.addSpacing(8)
        layout.addWidget(self.__build_footer())

        self.__menu_item_list: list[MenuItem] = []
        self.__command_item_info_list: list[CommandItemInfo] = []
        self.__selected_command_item_info_list: list[CommandItemInfo] = []
        self.__anchor_index: int = 0

    def __build_bulk_bar(self) -> QtWidgets.QWidget:
        bar = QtWidgets.QWidget()
        bar.setProperty("class", "BulkActionBar")
        bar.setFixedHeight(44)

        layout = QtWidgets.QHBoxLayout(bar)
        layout.setContentsMargins(8, 2, 12, 2)
        layout.setSpacing(8)

        self.selected_count_label = QtWidgets.QLabel("")
        self.selected_count_label.setProperty("class", "SelectedCountLabel")
        layout.addWidget(self.selected_count_label)
        layout.addStretch()

        self.run_selected_button = QtWidgets.QPushButton("▶ Run Selected")
        self.run_selected_button.setProperty("class", "ButtonBlue")
        self.run_selected_button.setFixedSize(120, 36)
        self.run_selected_button.clicked.connect(
            lambda: self.on_click_run_selected_signal.emit(
                list(self.__selected_command_item_info_list)
            )
        )
        layout.addWidget(self.run_selected_button)

        return bar

    def __build_scroll_area(self) -> QtWidgets.QScrollArea:
        self.__items_container = QtWidgets.QWidget()
        self.__items_container.setProperty("class", "MenuItemsContainer")

        self.__items_layout = QtWidgets.QVBoxLayout(self.__items_container)
        self.__items_layout.setContentsMargins(0, 0, 4, 0)
        self.__items_layout.setSpacing(8)
        self.__items_layout.addStretch()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setProperty("class", "MenuScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll_area.setWidget(self.__items_container)
        scroll_area.viewport().setProperty("class", "MenuScrollViewport")
        return scroll_area

    def __build_footer(self) -> QtWidgets.QWidget:
        footer = QtWidgets.QWidget()
        footer.setProperty("class", "MenuFooter")
        footer.setFixedHeight(36)

        layout = QtWidgets.QHBoxLayout(footer)
        layout.setContentsMargins(8, 0, 8, 0)

        self.item_count_label = QtWidgets.QLabel("0 items")
        self.item_count_label.setProperty("class", "MenuFooterLabel")
        layout.addWidget(self.item_count_label)
        layout.addStretch()

        self.footer_selected_label = QtWidgets.QLabel("")
        self.footer_selected_label.setProperty("class", "MenuFooterLabel")
        layout.addWidget(self.footer_selected_label)

        return footer

    def set_items(self, command_item_info_list: list[CommandItemInfo]):
        for menu_item in self.__menu_item_list:
            menu_item.deleteLater()
        self.__menu_item_list.clear()
        self.__command_item_info_list = list(command_item_info_list)
        self.__selected_command_item_info_list.clear()
        self.__anchor_index = 0

        while self.__items_layout.count() > 1:
            child = self.__items_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for command_item_info in command_item_info_list:
            menu_item = MenuItem(command_item_info)
            menu_item.on_click_item_signal.connect(
                lambda _ci, is_shift, is_ctrl_cmd, ci=command_item_info, mi=menu_item: (
                    self.__on_toggle_menu_item(ci, mi, is_shift, is_ctrl_cmd)
                )
            )
            menu_item.on_click_run_signal.connect(self.on_run_item_signal)
            self.__items_layout.insertWidget(self.__items_layout.count() - 1, menu_item)
            self.__menu_item_list.append(menu_item)

        if command_item_info_list:
            self.__selected_command_item_info_list.append(command_item_info_list[0])
            self.__menu_item_list[0].set_selected(True)

        self.item_count_label.setText(f"{len(command_item_info_list)} items")
        self.__refresh_selected_display()
        if self.__selected_command_item_info_list:
            self.on_select_item_signal.emit(self.__selected_command_item_info_list[0])

    def __on_toggle_menu_item(
        self,
        command_item_info: CommandItemInfo,
        menu_item: MenuItem,
        is_shift: bool,
        is_ctrl_cmd: bool,
    ):
        clicked_index = self.__menu_item_list.index(menu_item)

        if is_shift:
            # アンカーからクリック位置までの範囲を選択
            start = min(self.__anchor_index, clicked_index)
            end = max(self.__anchor_index, clicked_index)
            self.__selected_command_item_info_list.clear()
            for i, item in enumerate(self.__menu_item_list):
                in_range = start <= i <= end
                item.set_selected(in_range)
                if in_range:
                    self.__selected_command_item_info_list.append(
                        self.__command_item_info_list[i]
                    )

        elif is_ctrl_cmd:
            # 個別トグル（最後の1つは外さない）
            if command_item_info in self.__selected_command_item_info_list:
                if len(self.__selected_command_item_info_list) > 1:
                    self.__selected_command_item_info_list.remove(command_item_info)
                    menu_item.set_selected(False)
            else:
                self.__selected_command_item_info_list.append(command_item_info)
                menu_item.set_selected(True)
            self.__anchor_index = clicked_index

        else:
            # シングル選択
            for item in self.__menu_item_list:
                item.set_selected(False)
            self.__selected_command_item_info_list.clear()
            self.__selected_command_item_info_list.append(command_item_info)
            menu_item.set_selected(True)
            self.__anchor_index = clicked_index

        self.on_select_item_signal.emit(self.__selected_command_item_info_list[0])
        self.__refresh_selected_display()

    def __refresh_selected_display(self):
        count = len(self.__selected_command_item_info_list)
        if count > 0:
            self.selected_count_label.setText(f"{count} selected")
            self.footer_selected_label.setText(f"{count} selected")
        else:
            self.selected_count_label.setText("")
            self.footer_selected_label.setText("")
