import os

from PySide6 import QtCore, QtGui, QtWidgets

from cmdlaunch.data.item_info import CategoryItemInfo


class CategoryItem(QtWidgets.QFrame):
    """カテゴリサイドバー行ウィジェット"""

    on_click_item_signal = QtCore.Signal(CategoryItemInfo)

    def __init__(
        self, category_item_info: CategoryItemInfo, selected: bool = False, parent=None
    ):
        super().__init__(parent)
        self.__category_item_info = category_item_info

        self.setProperty("class", "CategoryItem")
        self.setFixedHeight(64)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.setProperty("isSelected", selected)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(16, 15, 16, 15)
        layout.setSpacing(18)

        icon_label = QtWidgets.QLabel()
        icon_label.setProperty("class", "CategoryItemIcon")
        icon_label.setFixedSize(34, 34)
        icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        if category_item_info.icon_path and os.path.isfile(
            category_item_info.icon_path
        ):
            pixmap = QtGui.QPixmap(category_item_info.icon_path).scaled(
                34,
                34,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            icon_label.setPixmap(pixmap)
        else:
            icon_label.setText(category_item_info.name[0].upper())
            # icon_color はカテゴリごとに異なるためインラインスタイルで設定
            icon_label.setStyleSheet(f"""
                background-color: {category_item_info.icon_color};
                color: #090a0d;
                border: none;
                border-radius: 4px;
                font-size: 18px;
                font-weight: bold;
            """)
        layout.addWidget(icon_label)

        name_label = QtWidgets.QLabel(category_item_info.name)
        name_label.setProperty("class", "CategoryItemName")
        layout.addWidget(name_label, 1)

        badge_label = QtWidgets.QLabel(str(category_item_info.item_count()))
        badge_label.setProperty("class", "CategoryItemBadge")
        badge_label.setFixedSize(30, 30)
        badge_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(badge_label)

    @property
    def category_item_info(self) -> CategoryItemInfo:
        return self.__category_item_info

    def set_selected(self, selected: bool):
        self.setProperty("isSelected", selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.on_click_item_signal.emit(self.__category_item_info)
        super().mousePressEvent(event)
