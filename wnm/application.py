import os 
from .engine import NotesManager
from .forms import NewNoteWindow, DeleteNoteWindow
from .qtImport import *

class WNMApplication(QMainWindow):
    def __init__(self, engine=None):
        super(WNMApplication, self).__init__()

        self._zfactor = 1.
        self.view = None
        self._keys = []
        
        if engine == None:
            self._engine = NotesManager()
        else:
            self._engine = engine
            self._conf = self._engine.get_config()

    def defineShortCut(self):
        key = PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence( self._conf.shortcut.create ),self )
        key.activated.connect( self.newNote )
        self._keys.append( key )
        key = PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence( self._conf.shortcut.edit ), self )
        key.activated.connect( self.editNote )
        self._keys.append( key )
        key = PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence( self._conf.shortcut.compile ), self)
        key.activated.connect( self.compileNotes )
        self._keys.append( key )

        key = PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence( self._conf.shortcut.delete ), self)
        key.activated.connect( self.deleteNotes )
        self._keys.append( key )

        key = PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence( self._conf.shortcut.zoomin ), self)
        key.activated.connect( self.zoom )
        self._keys.append( key )

        key = PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence( self._conf.shortcut.zoomout ), self)
        key.activated.connect( self.unzoom )
        self._keys.append( key )


        key = PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence( self._conf.shortcut.pdf ), self)
        key.activated.connect( self.exportPDF )
        self._keys.append( key )


    def initUI(self):

        url_base = os.path.abspath(os.path.join( self._engine.get_build_dir(), "index.html" ))
        url = QUrl( "file:" + os.path.sep + os.path.sep + url_base )
        self.view = QWebView(self)
        self.view.load( url )
        self.setCentralWidget(self.view)
        self.defineShortCut()

        self._newNote = NewNoteWindow(self)
        self._deleteNote = DeleteNoteWindow(self)

    def zoom(self):
        self._zfactor += 0.05
        self.view.setZoomFactor(self._zfactor)

    def unzoom(self):
        self._zfactor -= 0.05
        self.view.setZoomFactor(self._zfactor)

    def newNote(self):
        _data = self._engine.listCategory()
        self._newNote.setCategory( _data )
        self._newNote.initUI()
        self._newNote.setWindowModality(QtCore.Qt.ApplicationModal)
        self._newNote.show()    

    def deleteNotes(self):
        _data = self._engine.listNotes()
        self._deleteNote.setNotesTree( _data )
        self._deleteNote.initUI()
        self._deleteNote.setWindowModality(QtCore.Qt.ApplicationModal)
        self._deleteNote.show()

    def actionNewNote(self, data):
        category = None
        if data["new_category"] is True:
            category = data["new_category_name"]
            ret = self._engine.createCategory( data["new_category_name"] )
        else:
            all_category = self._engine.listCategory()
            category = all_category[data["category"]]

        self._engine.createNote( category, data["note_name"])

    def actionDeleteNote(self, data):
        return NotImplementedError


    def editNote(self):
        """
        Edit the rst file associted to the current viewed html page
        """ 
        url = self.view.url().path()
        tmp = url.split("/")
        try:
            category = tmp[-2].split("_")[1]
        except:
            category = None
        note = tmp[-1][:-5]
        self._engine.editNote( category, note)

    def compileNotes(self):
        """ 
        Function which compile sphinx documentation backend
        and update the html view
        """
        self._engine.compileHtml()
        self.view.reload()
        
    def exportPDF(self):
        name = QFileDialog.getSaveFileName(self, "Export to pdf", filter="PDF (*.pdf)")[0]

        printer = QPrinter()
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(name)
        
        self.view.print_( printer )
