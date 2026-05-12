import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QProgressBar,
    QTextEdit,
    QMessageBox,
)
from PySide6.QtCore import QThread, Signal
import script_gui


class OutputCapturer:
    def __init__(self, callback):
        self.callback = callback

    def write(self, msg):
        if msg.strip():
            self.callback(msg.strip())

    def flush(self):
        pass


class Worker(QThread):
    log = Signal(str)
    done = Signal(bool, str)

    def __init__(self, url, st_id, nat_id):
        super().__init__()
        self.url = url
        self.st_id = st_id
        self.nat_id = nat_id

    def run(self):
        old_stdout = sys.stdout
        sys.stdout = OutputCapturer(self.log.emit)

        try:
            script_gui.main(url=self.url, st_id=self.st_id, nat_id=self.nat_id)
            self.done.emit(True, "Done.")
        except Exception as e:
            self.done.emit(False, str(e))
        finally:
            sys.stdout = old_stdout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adobe Meeting Downloader")
        self.setFixedSize(500, 450)

        layout = QVBoxLayout()
        layout.setSpacing(8)

        # URL
        layout.addWidget(QLabel("Class URL:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://lms1.sku.ac.ir/...")
        layout.addWidget(self.url_input)

        # Student ID
        layout.addWidget(QLabel("Student ID (number only):"))
        self.st_id_input = QLineEdit()
        self.st_id_input.setPlaceholderText("4041406xxx")
        layout.addWidget(self.st_id_input)

        # National Code
        layout.addWidget(QLabel("National Code:"))
        self.nat_id_input = QLineEdit()
        self.nat_id_input.setEchoMode(QLineEdit.Password)
        self.nat_id_input.setPlaceholderText("**********")
        layout.addWidget(self.nat_id_input)

        # Button
        self.btn = QPushButton("Start Download")
        self.btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.btn.clicked.connect(self.start)
        layout.addWidget(self.btn)

        # Progress
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # Log
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet(
            "QTextEdit { background-color: #1e1e1e; color: #d4d4d4; font-family: monospace; }"
        )
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def start(self):
        url = self.url_input.text().strip()
        st_id = self.st_id_input.text().strip()
        nat_id = self.nat_id_input.text().strip()

        if not url or not st_id or not nat_id:
            QMessageBox.warning(self, "Error", "All fields are required.")
            return

        if not nat_id.isdigit():
            QMessageBox.warning(self, "Error", "National code must be digits only.")
            return

        self.btn.setEnabled(False)
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)
        self.log_output.clear()

        self.worker = Worker(url.rstrip("/"), st_id, nat_id)
        self.worker.log.connect(self.log_output.append)
        self.worker.done.connect(self.finish)
        self.worker.start()

    def finish(self, success, msg):
        self.progress.setMaximum(100)
        self.progress.setValue(100 if success else 0)
        self.log_output.append(f"\n{msg}")
        self.btn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
