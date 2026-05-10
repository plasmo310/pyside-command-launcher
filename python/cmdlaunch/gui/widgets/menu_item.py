import os

from PySide6 import QtCore, QtGui, QtWidgets

from cmdlaunch.data.item_info import CommandItemInfo
from cmdlaunch.gui.widgets.icon_button import IconButton


class MenuItem(QtWidgets.QFrame):
    """メニューリスト行ウィジェット"""

    on_click_run_signal = QtCore.Signal(CommandItemInfo)
    on_click_item_signal = QtCore.Signal(CommandItemInfo, bool, bool)

    def __init__(
        self, command_item_info: CommandItemInfo, selected: bool = False, parent=None
    ):
        super().__init__(parent)
        self.__command_item_info = command_item_info

        self.setProperty("class", "MenuItem")
        self.setFixedHeight(72)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setProperty("isSelected", selected)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 8, 12)
        layout.setSpacing(0)

        icon_label = QtWidgets.QLabel()
        icon_label.setProperty("class", "MenuItemIcon")
        icon_label.setFixedSize(38, 38)
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if command_item_info.icon_path and os.path.isfile(command_item_info.icon_path):
            pixmap = QtGui.QPixmap(command_item_info.icon_path).scaled(
                38,
                38,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            icon_label.setPixmap(pixmap)
        else:
            icon_label.setText(command_item_info.name[0].upper())
            if command_item_info.icon_color:
                icon_label.setStyleSheet(f"""
                    background-color: {command_item_info.icon_color};
                    color: #090a0d;
                    border: none;
                    border-radius: 4px;
                    font-size: 18px;
                    font-weight: bold;
                """)
        layout.addWidget(icon_label)
        layout.addSpacing(12)

        text_block = QtWidgets.QWidget()
        text_block.setProperty("class", "TextBlock")
        text_block.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        text_layout = QtWidgets.QVBoxLayout(text_block)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(4)
        text_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)

        name_label = QtWidgets.QLabel(command_item_info.name)
        name_label.setProperty("class", "MenuItemName")
        text_layout.addWidget(name_label)

        description_label = QtWidgets.QLabel(command_item_info.description)
        description_label.setProperty("class", "MenuItemDescription")
        text_layout.addWidget(description_label)

        layout.addWidget(text_block, 1)
        layout.addSpacing(8)

        run_button = IconButton("▶")
        run_button.clicked.connect(
            lambda: self.on_click_run_signal.emit(self.__command_item_info)
        )
        layout.addWidget(run_button)

    def set_selected(self, selected: bool):
        self.setProperty("isSelected", selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            modifiers = event.modifiers()
            is_shift = bool(modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier)
            is_ctrl_cmd = bool(
                modifiers
                & (
                    QtCore.Qt.KeyboardModifier.ControlModifier
                    | QtCore.Qt.KeyboardModifier.MetaModifier
                )
            )
            self.on_click_item_signal.emit(
                self.__command_item_info, is_shift, is_ctrl_cmd
            )
        super().mousePressEvent(event)
