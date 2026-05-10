from PySide6 import QtWidgets


class IconButton(QtWidgets.QToolButton):
    """正方形アイコンボタン"""

    def __init__(self, icon_text: str, danger: bool = False, parent=None):
        super().__init__(parent)
        self.setText(icon_text)
        self.setFixedSize(36, 36)
        self.setProperty("class", "IconButtonDanger" if danger else "IconButton")
