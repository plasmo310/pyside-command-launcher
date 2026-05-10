from PySide6 import QtCore, QtWidgets

from cmdlaunch.data.item_info import CategoryItemInfo
from cmdlaunch.gui.widgets.category_item import CategoryItem


class CategoryPanel(QtWidgets.QFrame):
    """カテゴリサイドバーパネル"""

    on_select_category_signal = QtCore.Signal(CategoryItemInfo)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "CategoryPanel")
        self.setMinimumSize(QtCore.QSize(280, 1))

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(8, 24, 8, 24)
        layout.setSpacing(0)

        header_label = QtWidgets.QLabel("Categories")
        header_label.setProperty("class", "PanelHeader")
        layout.addWidget(header_label)
        layout.addSpacing(18)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setProperty("class", "CategoryScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        items_container = QtWidgets.QWidget()
        items_container.setProperty("class", "CategoryItemsContainer")

        self.__items_layout = QtWidgets.QVBoxLayout(items_container)
        self.__items_layout.setContentsMargins(0, 0, 0, 0)
        self.__items_layout.setSpacing(12)
        self.__items_layout.addStretch()

        scroll_area.setWidget(items_container)
        layout.addWidget(scroll_area, 1)

        self.__category_item_list: list[CategoryItem] = []

    def set_categories(
        self,
        category_item_info_list: list[CategoryItemInfo],
        selected_category_item_info: CategoryItemInfo | None = None,
    ):
        while self.__items_layout.count() > 1:
            child = self.__items_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.__category_item_list.clear()

        for category_item_info in category_item_info_list:
            is_selected = category_item_info is selected_category_item_info
            category_item = CategoryItem(category_item_info, selected=is_selected)
            category_item.on_click_item_signal.connect(self.__on_click_category_item)
            self.__items_layout.insertWidget(
                self.__items_layout.count() - 1, category_item
            )
            self.__category_item_list.append(category_item)

    def __on_click_category_item(self, category_item_info: CategoryItemInfo):
        for category_item in self.__category_item_list:
            category_item.set_selected(category_item.category_item_info is category_item_info)
        self.on_select_category_signal.emit(category_item_info)
