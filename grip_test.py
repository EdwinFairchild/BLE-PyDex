from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Draggable Separator Example")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.layout = QVBoxLayout()

        self.frame_top = QFrame()
        self.frame_top.setStyleSheet("background-color: red;")
        self.frame_top.setFixedHeight(100)
        self.layout.addWidget(self.frame_top)

        self.frame_separator = QFrame()
        self.frame_separator.setStyleSheet("background-color: green;")
        self.frame_separator.setFixedHeight(10)
        self.frame_separator.setCursor(Qt.SizeVerCursor)
        self.layout.addWidget(self.frame_separator)

        self.frame_bottom = QFrame()
        self.frame_bottom.setStyleSheet("background-color: blue;")
        self.frame_bottom.setFixedHeight(100)
        self.layout.addWidget(self.frame_bottom)

        main_widget.setLayout(self.layout)

        # For tracking mouse position
        self.oldPos = None

    def mousePressEvent(self, event):
        if self.frame_separator.geometry().contains(event.position().toPoint()):
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
            new_top_height = self.frame_top.height() + delta.y()
            new_bottom_height = self.frame_bottom.height() - delta.y()

            # Enforce minimum sizes
            new_top_height = max(50, new_top_height)
            new_bottom_height = max(50, new_bottom_height)

            self.frame_top.setFixedHeight(new_top_height)
            self.frame_bottom.setFixedHeight(new_bottom_height)
            self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.oldPos = None

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
