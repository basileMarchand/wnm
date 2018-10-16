
from .qtImport import *


class NewNoteForm(QWidget):
    def __init__(self, parent, category_list):
        super().__init__()
        self._parent = parent
        self._category = category_list
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout( layout )

        label = QLabel("In catergory ")        
        layout.addWidget( label, 1, 1 )
        self._list = QComboBox()
        layout.addWidget( self._list, 1, 2)

        for x in self._category:
            self._list.addItem( x )
            
        self._newCategory = QCheckBox("Create a new category")
        layout.addWidget( self._newCategory , 2,1)
        self._newCategoryName = QLineEdit()
        layout.addWidget( self._newCategoryName, 2, 2)
        
        name = QLabel("The name of the new note  ")        
        layout.addWidget( name, 3, 1 )        
        self._inp_name = QLineEdit()

        layout.addWidget( self._inp_name, 3, 2)
        button = QPushButton("Create")
        button.clicked.connect( self._parent.create )
        layout.addWidget( button, 4, 1, 1,2)
        
    def getInputs(self):
        data = {}
        data["category"] = self._list.currentIndex()
        data["new_category"] = self._newCategory.isChecked()
        data["new_category_name"] = self._newCategoryName.text()
        data["note_name"] = self._inp_name.text()
        return data
        
        
class NewNoteWindow(QMainWindow):
    def __init__(self, parent):
        super(NewNoteWindow, self).__init__(parent)
        self._form = None      
        self._parent = parent
        

    def setCategory(self, available ):
        self._category = available

    def initUI(self):
        self.setWindowTitle("Create a new notes")
        _widget = QWidget()
        windowLayout = QVBoxLayout(_widget)        
        self._form = NewNoteForm( self, self._category )
        windowLayout.addWidget( self._form )
        self.setCentralWidget( _widget )

    def create( self ):
        data = self._form.getInputs()
        self._parent.actionNewNote( data )        
        self.close()




class DeleteNoteForm(QWidget):
    def __init__(self, parent, notes_tree):
        super().__init__()
        self._parent = parent
        self._notes_tree = notes_tree
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout( layout )

        label = QLabel("Select the note or category you want to delete\n Becarefull it's a definitiv deletion")        
        layout.addWidget( label, 1, 1, 2, 2 )
        self._tree = QTreeWidget()
        headerItem  = QTreeWidgetItem()
        item    = QTreeWidgetItem()

        layout.addWidget( self._tree, 1, 2)

        for category, notes in self._notes_tree.items():
            parent = QTreeWidgetItem(self._tree)
            parent.setText(0, category)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            for note in notes:
                child = QTreeWidgetItem(self._tree)
                child.setText(0, note)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setCheckState(0, Qt.Unchecked)


        button = QPushButton("Delete selection")
        button.clicked.connect( self._parent.delete )
        layout.addWidget( button, 4, 1, 1,2)
        
    def getInputs(self):
        iterator = QTreeWidgetItemIterator(self._tree, QTreeWidgetItemIterator.Checked)
        while iterator.value():
            item = iterator.value()
            print (item.text(0))    
            iterator += 1

        data = {}
        return data

class DeleteNoteWindow(QMainWindow):
    def __init__(self, parent):
        super(DeleteNoteWindow, self).__init__(parent)
        self._form = None      
        self._parent = parent
        
    def setNotesTree(self, available ):
        self._category = available

    def initUI(self):
        self.setWindowTitle("Delete a note or a category")
        _widget = QWidget()
        windowLayout = QVBoxLayout(_widget)        
        self._form = DeleteNoteForm( self, self._category )
        windowLayout.addWidget( self._form )
        self.setCentralWidget( _widget )

    def delete( self ):
        data = self._form.getInputs()
        self._parent.actionDeleteNote( data )        
        self.close()
