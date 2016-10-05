import sys
import os
import re
from Qt.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit, QAction
from Qt.QtWidgets import QFileDialog
from Qt.QtGui import QFont, QFontMetrics
from highlighter import Highlighter, DEFAULT_RULES, DEFAULT_STYLE

test = "øæååøæøæåøæ안녕 하세요 Jakob씨" # (and some garbage)

class Editor(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.current_dir = os.getcwd()
        self.current_file = None
        
        self.init_ui()
    
    def init_ui(self):
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        
        font = QFont("Menlo", 12)
        # TODO: Create a layout and change the line spacing
        #spacing = QFontMetrics(font).lineSpacing()
        self.text_edit.setFont(font)
        self.highlighter = Highlighter(self.text_edit.document(), DEFAULT_RULES, DEFAULT_STYLE)
        #print("Highlighter doc: {}".format(self.text_edit.document()))
        
        menu_bar = self.menuBar()
        m_file = menu_bar.addMenu("File")
        
        i_open = QAction("Open", self)
        i_open.setShortcut('Ctrl+O')
        i_open.triggered.connect(self.on_open)
        
        m_file.addAction(i_open)
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle("tea")
    
    def on_open(self):
        file_path, other = QFileDialog.getOpenFileName(self, "Open File", self.current_dir)
        #print([a for a in dir(QFileDialog) if not a.startswith("_")])
        print("File name: {}, Other: {}".format(file_path, other))
        if file_path:
            dirname = os.path.basename(os.path.dirname(file_path))
            filename = os.path.basename(file_path)
            self.setWindowTitle("{} - {}".format(filename, dirname))
            with open(file_path) as f:
                text = f.read()
                #formatted = markup_python(text)
                #formatted = "<font color=red size=24>{}</font>".format(text)
                self.text_edit.setText(text)
                #print("Updated doc: {}".format(self.text_edit.document()))

def main():
    """Entry point"""
    # Just starting the app returns in a sigsegv on close :/
    app = QApplication(sys.argv)
    #label = QLabel("<font color=red size=40>Hello World</font>")
    #label.show()
    editor = Editor()
    editor.show()
    res = app.exec_()
    #sys.exit(res)

if __name__ == '__main__':
    main()