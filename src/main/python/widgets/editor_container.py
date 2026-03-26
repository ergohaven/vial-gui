from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, QEvent


class EditorContainer(QWidget):

    clicked = pyqtSignal()

    def __init__(self, editor):
        super().__init__()

        self.editor = editor

        self.setLayout(editor)
        self.clicked.connect(editor.on_container_clicked)

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            if hasattr(self.editor, 'retranslateUi'):
                self.editor.retranslateUi()
        super().changeEvent(event)
