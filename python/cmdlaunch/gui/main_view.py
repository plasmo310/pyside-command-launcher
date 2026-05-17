from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Signal

from cmdlaunch.tool_config import ToolConfig

from .widgets.category_panel import CategoryPanel
from .widgets.detail_panel import DetailPanel
from .widgets.menu_panel import MenuPanel


class MainView(QtWidgets.QMainWindow):
    """メイン画面 Viewクラス"""

    on_click_open_settings_signal = Signal()
    on_click_reflesh_signal = Signal()
    on_click_toggle_detail_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(ToolConfig.TOOL_TITLE)
        self.setWindowIcon(QtGui.QIcon(ToolConfig.get_tool_icon_path()))
        self.resize(1280, 800)
        self.setMinimumSize(QtCore.QSize(0, 0))

        rect = self.frameGeometry()
        rect.moveCenter(
            QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        )
        self.move(rect.topLeft())

        self.__build_ui()

    def __build_ui(self):
        root_widget = QtWidgets.QWidget()
        root_widget.setProperty("class", "RootWidget")
        self.setCentralWidget(root_widget)

        main_layout = QtWidgets.QVBoxLayout(root_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

        main_layout.addWidget(self.__build_header())
        main_layout.addWidget(self.__build_content(), 1)

    def __build_header(self) -> QtWidgets.QWidget:
        header_bar = QtWidgets.QWidget()
        header_bar.setProperty("class", "HeaderBar")
        header_bar.setFixedHeight(80)

        layout = QtWidgets.QHBoxLayout(header_bar)
        layout.setContentsMargins(26, 0, 16, 0)
        layout.setSpacing(0)

        app_icon_label = QtWidgets.QLabel()
        app_icon_pixmap = QtGui.QPixmap(ToolConfig.get_tool_icon_svg_path()).scaled(
            36,
            36,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )
        app_icon_label.setPixmap(app_icon_pixmap)
        layout.addWidget(app_icon_label)
        layout.addSpacing(6)

        window_title_label = QtWidgets.QLabel(ToolConfig.TOOL_TITLE)
        window_title_label.setProperty("class", "WindowTitle")
        layout.addWidget(window_title_label)
        layout.addStretch()

        open_settings_button = QtWidgets.QPushButton("Open Settings")
        open_settings_button.setFixedHeight(36)
        open_settings_button.setProperty("class", "ButtonSmall")
        open_settings_button.setStyleSheet("padding: 0 11px;")
        open_settings_button.clicked.connect(self.on_click_open_settings_signal)
        layout.addWidget(open_settings_button)
        layout.addSpacing(8)

        reflesh_button = QtWidgets.QPushButton("Reflesh")
        reflesh_button.setFixedHeight(36)
        reflesh_button.setProperty("class", "ButtonSmall")
        reflesh_button.setStyleSheet("padding: 0 11px;")
        reflesh_button.clicked.connect(self.on_click_reflesh_signal)
        layout.addWidget(reflesh_button)
        layout.addSpacing(8)

        self.__toggle_detail_button = QtWidgets.QPushButton("◧")
        self.__toggle_detail_button.setFixedHeight(36)
        self.__toggle_detail_button.setProperty("class", "ButtonSmall")
        self.__toggle_detail_button.setStyleSheet(
            "padding: 0 11px 4px 11px; font-size: 16px;"
        )
        self.__toggle_detail_button.clicked.connect(self.on_click_toggle_detail_signal)
        layout.addWidget(self.__toggle_detail_button)

        return header_bar

    def __build_content(self) -> QtWidgets.QWidget:
        content_area = QtWidgets.QWidget()
        content_area.setProperty("class", "ContentArea")

        outer_layout = QtWidgets.QVBoxLayout(content_area)
        outer_layout.setContentsMargins(16, 0, 16, 16)
        outer_layout.setSpacing(0)
        outer_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)

        self.__splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        self.__splitter.setProperty("class", "MainSplitter")
        self.__splitter.setChildrenCollapsible(True)
        self.__splitter.setHandleWidth(8)
        self.__splitter.setMinimumHeight(0)

        self.category_panel = CategoryPanel()
        self.menu_panel = MenuPanel()
        self.detail_panel = DetailPanel()

        self.__splitter.addWidget(self.category_panel)
        self.__splitter.addWidget(self.menu_panel)
        self.__splitter.addWidget(self.detail_panel)
        self.__splitter.setSizes([280, 400, 536])

        self.__detail_panel_saved_width = 536

        outer_layout.addWidget(self.__splitter)

        return content_area

    def toggle_detail_panel(self):
        """DetailPanelの開閉"""
        sizes = self.__splitter.sizes()
        detail_width = sizes[2]
        if detail_width > 0:
            self.__detail_panel_saved_width = detail_width
            self.resize(self.width() - detail_width, self.height())
            self.__splitter.setSizes([sizes[0], sizes[1], 0])
            self.__toggle_detail_button.setText("◨")
        else:
            restored = self.__detail_panel_saved_width
            self.resize(self.width() + restored, self.height())
            self.__splitter.setSizes([sizes[0], sizes[1], restored])
            self.__toggle_detail_button.setText("◧")
