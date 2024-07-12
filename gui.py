import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox, QCheckBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from email_sage import main as email_sage_main
from PyQt5.QtGui import QFont
from pyfiglet import figlet_format

class EmailFinderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Email Sage - Email Finder')
        self.setGeometry(100, 100, 800, 700)  # Increased window size

        layout = QVBoxLayout()

        # Create a banner label with ASCII art
        # banner_text = figlet_format('Email Sage')
        # banner_label = QLabel(banner_text, self)
        # banner_label.setFont(QFont("Courier", 16))  # Set a monospaced font for better display
        # banner_label.setAlignment(Qt.AlignCenter)  # Center align the banner
        # layout.addWidget(banner_label)  # Add the banner to the layout


        font = QFont()
        font.setPointSize(18)  # Increased font size for better readability

        self.domain_label = QLabel('Domain:')
        self.domain_label.setFont(font)
        self.domain_input = QLineEdit(self)
        self.domain_input.setFont(font)

        self.limit_label = QLabel('Limit:')
        self.limit_label.setFont(font)
        self.limit_input = QLineEdit(self)
        self.limit_input.setText("10")
        self.limit_input.setFont(font)

        self.output_label = QLabel('Output File:')
        self.output_label.setFont(font)
        self.output_input = QLineEdit(self)
        self.output_input.setFont(font)
        self.output_button = QPushButton('Browse')
        self.output_button.setFont(font)
        self.output_button.clicked.connect(self.browse_output_file)

        self.validate_checkbox = QCheckBox('Validate Emails')
        self.validate_checkbox.setFont(font)
        self.dns_checkbox = QCheckBox('Perform DNS Lookup')
        self.dns_checkbox.setFont(font)

        self.run_button = QPushButton('Run')
        self.run_button.setFont(font)
        self.run_button.clicked.connect(self.run_email_sage)
        self.run_button.setStyleSheet(
            "border-radius: 10px; border: 2px solid #0073cf; background-color: #0073cf; color: white;"
        )

        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.result_text.setFont(font)

        layout.addWidget(self.domain_label)
        layout.addWidget(self.domain_input)
        layout.addWidget(self.limit_label)
        layout.addWidget(self.limit_input)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_input)
        layout.addWidget(self.output_button)
        layout.addWidget(self.validate_checkbox)
        layout.addWidget(self.dns_checkbox)
        layout.addWidget(self.run_button)
        layout.addWidget(self.result_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def browse_output_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt);;CSV Files (*.csv);;JSON Files (*.json);;PDF Files (*.pdf)", options=options)
        if file:
            self.output_input.setText(file)

    def run_email_sage(self):
        domain = self.domain_input.text()
        limit = self.limit_input.text()
        output_file = self.output_input.text()
        validate = self.validate_checkbox.isChecked()
        dns_lookup = self.dns_checkbox.isChecked()

        args = ['-d', domain, '-l', limit]
        if output_file:
            args.extend(['-o', output_file])
        if validate:
            args.append('-v')
        if dns_lookup:
            args.append('--dns-lookup')

        self.result_text.clear()
        self.result_text.append("Running Email Sage with the following arguments: " + ' '.join(args))

        self.thread = EmailSageThread(args)
        self.thread.result.connect(self.display_result)
        self.thread.start()

    def display_result(self, result):
        self.result_text.append(result)

class EmailSageThread(QThread):
    result = pyqtSignal(str)

    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self):
        old_stdout = sys.stdout
        sys.stdout = self
        try:
            email_sage_main(self.args)
        except Exception as e:
            self.result.emit(f"Error: {e}")
        finally:
            sys.stdout = old_stdout

    def write(self, text):
        self.result.emit(text)

    def flush(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmailFinderApp()
    ex.show()
    sys.exit(app.exec_())
