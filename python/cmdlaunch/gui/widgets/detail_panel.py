from PySide6 import QtCore, QtGui, QtWidgets

from cmdlaunch.data.item_info import CommandItemInfo

_GUTTER_WIDTH = 34


class _LineNumberGutter(QtWidgets.QFrame):
    """CodeEditorの内部の行番号ガターウィジェット"""

    def __init__(self, editor: "QtWidgets.QTextEdit"):
        super().__init__(editor)
        self.__editor = editor
        self.setProperty("class", "LineNumberGutter")

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(_GUTTER_WIDTH, 0)

    def paintEvent(self, event: QtGui.QPaintEvent):
        option = QtWidgets.QStyleOption()
        option.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(
            QtWidgets.QStyle.PrimitiveElement.PE_Widget, option, painter, self
        )

        scroll_y = self.__editor.verticalScrollBar().value()
        doc = self.__editor.document()
        doc_layout = doc.documentLayout()
        font_height = self.__editor.fontMetrics().height()

        painter.setPen(QtGui.QColor("#6b7280"))
        block = doc.begin()
        block_number = 0
        while block.isValid():
            rect = doc_layout.blockBoundingRect(block)
            top = round(rect.top()) - scroll_y
            bottom = round(rect.bottom()) - scroll_y

            if top > event.rect().bottom():
                break

            if bottom >= event.rect().top():
                painter.drawText(
                    0,
                    top,
                    _GUTTER_WIDTH - 4,
                    font_height,
                    QtCore.Qt.AlignmentFlag.AlignRight
                    | QtCore.Qt.AlignmentFlag.AlignVCenter,
                    str(block_number + 1),
                )

            block = block.next()
            block_number += 1


class _CodeEditor(QtWidgets.QTextEdit):
    """コードエディタ"""

    _LINE_BOTTOM_MARGIN = 4.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptRichText(False)
        self.__gutter = _LineNumberGutter(self)
        self.document().blockCountChanged.connect(self.__update_viewport_margins)
        self.document().contentsChanged.connect(lambda: self.__gutter.update())
        self.verticalScrollBar().valueChanged.connect(lambda _: self.__gutter.update())
        self.__update_viewport_margins()

    def setPlainText(self, text: str):
        super().setPlainText(text)
        self.__apply_line_spacing()

    def __apply_line_spacing(self):
        block_format = QtGui.QTextBlockFormat()
        block_format.setBottomMargin(self._LINE_BOTTOM_MARGIN)
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.SelectionType.Document)
        cursor.setBlockFormat(block_format)
        cursor.clearSelection()
        self.setTextCursor(cursor)

    def __update_viewport_margins(self):
        self.setViewportMargins(_GUTTER_WIDTH, 0, 0, 0)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.__gutter.setGeometry(
            QtCore.QRect(cr.left(), cr.top(), _GUTTER_WIDTH, cr.height())
        )


class DetailPanel(QtWidgets.QFrame):
    """詳細パネル"""

    on_click_open_signal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "DetailPanel")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 16)
        layout.setSpacing(0)
        layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.setMinimumSize(QtCore.QSize(1, 1))

        self.title_label = QtWidgets.QLabel("")
        self.title_label.setProperty("class", "DetailTitle")
        layout.addWidget(self.title_label)
        layout.addSpacing(24)

        layout.addWidget(self.__build_path_row())
        layout.addSpacing(8)
        layout.addWidget(self.__build_args_row())
        layout.addSpacing(8)
        layout.addWidget(self.__build_script_editor(), 1)

    def __build_path_row(self) -> QtWidgets.QWidget:
        path_row = QtWidgets.QWidget()
        path_row.setProperty("class", "PathRow")
        path_row.setFixedHeight(30)

        layout = QtWidgets.QHBoxLayout(path_row)
        layout.setContentsMargins(8, 0, 0, 0)
        layout.setSpacing(8)

        path_label = QtWidgets.QLabel("Path")
        path_label.setProperty("class", "PathLabel")
        path_label.setFixedWidth(36)
        layout.addWidget(path_label)

        self.path_edit = QtWidgets.QLineEdit()
        self.path_edit.setProperty("class", "PathField")
        self.path_edit.setReadOnly(True)
        self.path_edit.setFixedHeight(30)
        layout.addWidget(self.path_edit, 1)

        open_button = QtWidgets.QPushButton("Open")
        open_button.setProperty("class", "ButtonSmall")
        open_button.setFixedSize(48, 30)
        open_button.clicked.connect(
            lambda: self.on_click_open_signal.emit(self.path_edit.text())
        )
        layout.addWidget(open_button)

        return path_row

    def __build_args_row(self) -> QtWidgets.QWidget:
        args_row = QtWidgets.QWidget()
        args_row.setProperty("class", "PathRow")
        args_row.setFixedHeight(30)

        layout = QtWidgets.QHBoxLayout(args_row)
        layout.setContentsMargins(8, 0, 0, 0)
        layout.setSpacing(6)

        args_label = QtWidgets.QLabel("Args")
        args_label.setProperty("class", "PathLabel")
        args_label.setFixedWidth(36)
        layout.addWidget(args_label)

        self.args_edit = QtWidgets.QLineEdit()
        self.args_edit.setProperty("class", "PathField")
        self.args_edit.setReadOnly(True)
        self.args_edit.setFixedHeight(30)
        layout.addWidget(self.args_edit, 1)

        return args_row

    def __build_script_editor(self) -> QtWidgets.QFrame:
        editor_frame = QtWidgets.QFrame()
        editor_frame.setProperty("class", "ScriptEditorFrame")

        layout = QtWidgets.QHBoxLayout(editor_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        editor_frame.setMinimumHeight(0)

        self.code_editor = _CodeEditor()
        self.code_editor.setProperty("class", "CodeEditor")
        self.code_editor.setReadOnly(True)
        layout.addWidget(self.code_editor, 1)

        return editor_frame

    def show_item(
        self, command_item_info: CommandItemInfo | None, script_content: str | None = ""
    ):
        if command_item_info is None:
            self.title_label.setText("")
            self.path_edit.clear()
            self.args_edit.clear()
            self.code_editor.clear()
            return

        self.title_label.setText(command_item_info.name)
        self.path_edit.setText(command_item_info.script_path)
        self.args_edit.setText(command_item_info.args)
        if script_content is None:
            self.code_editor.setPlainText("# This file type is not supported for preview.")
        elif script_content:
            self.code_editor.setPlainText(script_content)
        else:
            self.code_editor.clear()
