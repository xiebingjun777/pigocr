import sys,os,threading
from multiprocessing import freeze_support
# from PySide6 import QtWidgets
# from PySide2 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QTimer, Qt, QCoreApplication
from PyQt5 import uic, QtWebEngineWidgets
from PyQt5.QtGui import QIcon
from qt_material import apply_stylesheet, QtStyleTools, density
from paddleocr import PaddleOCR,draw_ocr
# Extra stylesheets
extra = {
    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',
    # Font
    'font_family': 'Roboto',
    # Density
    'density_scale': '0',
    # Button Shape
    'button_shape': 'default',
}
RUN_PATH = os.path.split(os.path.realpath(__file__))[0]
########################################################################
class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super().__init__()
        self.setFixedSize(800,500);
        self.main = uic.loadUi('main_window.ui', self)
        wt = '🐖'
        

        try:
            self.main.setWindowTitle(f'{self.main.windowTitle()} - {wt}')
        except:
            self.main.window_title = f'{self.main.window_title} - {wt}'

        self.set_extra(extra)
        logo = QIcon("lulu.jpeg")
        logo_frame = QIcon("qt_material:/logo/logo_frame.svg")
        try:
            self.main.setWindowIcon(logo)
        except:
            self.main.window_icon = logo
           
        if hasattr(QFileDialog, 'getExistingDirectory'):
            self.main.pushButton_file_dialog.clicked.connect(
                self.load_img
            )
            # self.main.pushButton_folder_dialog.clicked.connect(
            #     lambda: QFileDialog.getExistingDirectory(self.main)
            # )
        else:
            self.main.pushButton_file_dialog.clicked.connect(
                self.load_img
            )
            # self.main.pushButton_folder_dialog.clicked.connect(
            #     lambda: QFileDialog.get_existing_directory(self.main)
            # )

        self.main.pushButton_2.clicked.connect(self.rec_word)
        self.initOCR()
        # ocr_thread = threading.Thread(target=self.initOCR)		# 定义一个线程，target定义要运行的函数
        # ocr_thread.start()		# 开始线程

    def initOCR(self):
        self.OCR = PaddleOCR(use_angle_cls=True, lang='ch',
                cls_model_dir=os.path.join(RUN_PATH, 'paddle_model', 'cls').decode("utf-8").encode("gbk"), 
                rec_model_dir=os.path.join(RUN_PATH, 'paddle_model', 'rec-ch').decode("utf-8").encode("gbk"), 
                det_model_dir=os.path.join(RUN_PATH, 'paddle_model', 'det').decode("utf-8").encode("gbk"), 
                show_log=False)

    def rec_word(self):
        rec_text = ""
        result = self.OCR.ocr(self.main.lineEdit_1.text(), cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                print(line)
                rec_text = rec_text + line[1][0] + "\n"
        self.main.textEdit.setText(rec_text)

    def load_img(self):
        file_path = QFileDialog.getOpenFileName(self.main)
        self.main.lineEdit_1.setText(file_path[0])
    # ----------------------------------------------------------------------
    def custom_styles(self):
        """"""
        for i in range(self.main.toolBar_vertical.layout().count()):

            try:
                tool_button = (
                    self.main.toolBar_vertical.layout().itemAt(i).widget()
                )
                tool_button.setMaximumWidth(150)
                tool_button.setMinimumWidth(150)
            except:
                tool_button = (
                    self.main.toolBar_vertical.layout().item_at(i).widget()
                )
                tool_button.maximum_width = 150
                tool_button.minimum_width = 150
        try:
            for r in range(self.main.tableWidget.rowCount()):
                self.main.tableWidget.setRowHeight(r, 36)

            for r in range(self.main.tableWidget_2.rowCount()):
                self.main.tableWidget_2.setRowHeight(r, 36)

        except:
            for r in range(self.main.tableWidget.row_count):
                self.main.tableWidget.set_row_height(r, 36)

            for r in range(self.main.tableWidget_2.row_count):
                self.main.tableWidget_2.set_row_height(r, 36)


if __name__ == "__main__":
    # create the application and the main window
    app = QApplication([])
    freeze_support()
    try:
        app.processEvents()
        app.setQuitOnLastWindowClosed(False)
        app.lastWindowClosed.connect(app.quit)
    except:
        app.process_events()
        app.quit_on_last_window_closed = False
        app.lastWindowClosed.connect(app.quit)

    if len(sys.argv) > 2:
        theme = sys.argv[2]
    else:
        theme = 'light_red.xml'

    # setup stylesheet
    apply_stylesheet(app, theme=theme,
        invert_secondary=('light' in theme and 'dark' not in theme),
        extra=extra)

    # # run
    # window.show()
    # app.exec_()

    frame = RuntimeStylesheets()
    try:
        frame.main.showMaximized()
    except:
        frame.main.show_maximized()

    if hasattr(app, 'exec'):
        app.exec()
    else:
        app.exec_()
