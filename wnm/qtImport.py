
from PyQt5.QtCore import Qt, QUrl
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QListWidget, QComboBox, QGridLayout, QGroupBox, QVBoxLayout, QLineEdit, QCheckBox, QPushButton, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QFileDialog
from PyQt5.QtPrintSupport import QPrinter
import PyQt5.QtGui
import PyQt5.QtWidgets


try:
    from PyQt5.QtWebKitWidgets import QWebView
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
