import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QFileDialog
import modified_rc4 as mrc4

# Screens
class main_screen(QDialog):
    def __init__(self):
        super(main_screen, self).__init__()
        loadUi("UI/main.ui", self)
        self.pushButton.clicked.connect(self.to_encrypt_screen)
        self.pushButton_2.clicked.connect(self.to_decrypt_screen)

    def to_encrypt_screen(self):
        screen = encrypt_screen()
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def to_decrypt_screen(self):
        screen = decrypt_screen()
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class encrypt_screen(QDialog):
    def __init__(self):
        super(encrypt_screen, self).__init__()
        loadUi("UI/encrypt.ui", self)
        self.mode = "encrypt"
        self.message = ""
        self.output_path = ""
        self.key = ""

        self.inputButton_1.toggled.connect(self.toggle_button1)
        self.inputButton_2.toggled.connect(self.toggle_button2)
        self.inputFileButton.clicked.connect(self.browse_input)
        self.goButton.clicked.connect(self.encode)
        self.backButton.clicked.connect(back)

    def browse_input(self):
        file = QFileDialog.getOpenFileName(self, "Open file", "~/Desktop")
        self.inputFileField.setText(file[0])
    
    def toggle_button1(self):
        self.button_state(self.inputButton_1)
    
    def toggle_button2(self):
        self.button_state(self.inputButton_2)
    
    def button_state(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")
    
    def get_message(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            self.message = mrc4.read_file(path)
        else:
            self.message = self.inputKeyboardField.text()
    
    def get_output_path(self):
        self.output_path = "output_encrypt/" + self.outputFileField.text() + "." + self.outputFormatField.text()
    
    def encode(self):
        self.get_message()
        self.get_output_path()
        self.key = self.keyField.text()
        mrc4.get_key(self.key)
        result = mrc4.encrypt(self.message)
        mrc4.write_file(self.output_path, result)

        self.outputField.setText(result)
        self.label_3.setText("Lihat File Hasil pada Folder Output!")

class decrypt_screen(QDialog):
    def __init__(self):
        super(decrypt_screen, self).__init__()
        loadUi("UI/decrypt.ui", self)
        self.mode = "decrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""

        self.inputButton_1.toggled.connect(self.toggle_button1)
        self.inputButton_2.toggled.connect(self.toggle_button2)
        self.inputFileButton.clicked.connect(self.browse_input)
        self.goButton.clicked.connect(self.decode)
        self.backButton.clicked.connect(back)

    def browse_input(self):
        file = QFileDialog.getOpenFileName(self, "Open file", "~/Desktop")
        self.inputFileField.setText(file[0])
    
    def toggle_button1(self):
        self.button_state(self.inputButton_1)
    
    def toggle_button2(self):
        self.button_state(self.inputButton_2)
    
    def button_state(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")
    
    def get_message(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            self.message = mrc4.read_file(path)
        else:
            self.message = self.inputKeyboardField.text()
    
    def get_output_path(self):
        self.output_path = "output_decrypt/" + self.outputFileField.text() + "." + self.outputFormatField.text()
    
    def decode(self):
        self.get_message()
        self.get_output_path()
        self.key = self.keyField.text()
        mrc4.get_key(self.key)
        result = mrc4.decrypt(self.message)
        mrc4.write_file(self.output_path, result)

        self.outputField.setText(result)
        self.label_3.setText("Lihat File Hasil pada Folder Output!")

def back():
    widget.removeWidget(widget.currentWidget())

# Main
app = QApplication(sys.argv)
widget = QStackedWidget()
main = main_screen()
widget.addWidget(main)
widget.setFixedWidth(640)
widget.setFixedHeight(640)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")







