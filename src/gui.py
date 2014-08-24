from PySide import QtGui
from PySide import QtCore
from collections import OrderedDict
import sys
import eo
from ref import kind_list

from PySide.QtCore import *
from PySide.QtGui import *

BLUE = QtGui.QBrush()
BLUE.setColor(QtGui.QColor(0,0,255))

BLACK = QtGui.QBrush()
BLACK.setColor(QtGui.QColor(0,0,0))



class Batch(QtGui.QWidget):
    
    def __init__(self):
        super(Batch, self).__init__()
        
        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        self.b = eo.Building()
        self.b.load('input/Kendrick.inp')

        # which kinds in which tab
        self.kind_map = {
            'Floor' : ['FLOOR'],
            'Wall' : ['INTERIOR-WALL', 'EXTERIOR-WALL', 'UNDERGROUND-WALL'],
            'Window' : ['WINDOW', 'DOOR'] ,
            'Space' : ['SPACE'] ,
            'Polygon' : ['POLYGON'] ,
            }

        existing = []
        for value in self.kind_map.values():
            existing += value

        self.kind_map['Other'] = [k for k in kind_list if not k in existing]
        
        self.selected = []
        
        self.setLayout(grid) 
        tabWidget = QtGui.QTabWidget()
        spaceTab = QtGui.QWidget()
        tabWidget.addTab(Main_Tab(self.b, self), 'Main')
        tabWidget.addTab(Floor_Tab(self.b, self), 'Floor')
        tabWidget.addTab(Space_Tab(self.b, self), 'Space')
        tabWidget.addTab(Wall_Tab(self.b, self), 'Wall')
        tabWidget.addTab(Window_Tab(self.b, self), 'Window')
        tabWidget.addTab(Polygon_Tab(self.b, self), 'Polygon')
        tabWidget.addTab(Other_Tab(self.b, self), 'Other')
        grid.addWidget(tabWidget, 2, 1)
        self.setGeometry(300, 300, 550, 700)
        self.show()



class Main_Tab(QtGui.QWidget):

    def __init__(self, parent, b):
        self.parent = parent
        self.b = b

        QtGui.QWidget.__init__(self)
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

class Filter_Tab(QtGui.QWidget):

    def __init__(self, b, parent, kind=None):
        self.b = b
        self.parent = parent
        self.kind = kind

        QtGui.QWidget.__init__(self)
        
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(10)

        self.search = QtGui.QLineEdit()
        self.search.textChanged.connect(self.filter)

        self.list = QtGui.QListWidget(self)
        self.list.itemClicked.connect(self.set_selection)
        self.list.setMaximumWidth(200)
        
        self.set_checkboxes()
        self.set_advanced_filters()

        self.filter()
        self.setLayout(self.grid) 
        
        self.grid.addWidget(self.search, 2, 1)

    def set_advanced_filters(self):
        if self.adv:
            self.adv.setVisible(False)
            self.moreless = QtGui.QPushButton('More Filters')
            self.moreless.setFlat(True)
            self.moreless.setMaximumWidth(100)
            self.moreless.clicked.connect(self.toggle_moreless)
            self.grid.addWidget(self.moreless, 3, 1)
            self.grid.addWidget(self.adv, 4, 1)
        self.grid.addWidget(self.list, 5, 1)




    def set_checkboxes(self):
        self.checkboxes = {}
        if len(self.parent.kind_map[self.kind]) > 1 and not self.kind=='Other':
            
            hbox = QtGui.QHBoxLayout()
            for kind in self.parent.kind_map[self.kind]:
                self.checkboxes[kind] = QtGui.QCheckBox(kind)
                self.checkboxes[kind].toggle()
                hbox.addWidget(self.checkboxes[kind])
                self.checkboxes[kind].stateChanged.connect(self.filter)
            self.grid.addLayout(hbox, 1, 1)

    def toggle_moreless(self):
    
        if self.adv.isVisible():
            self.adv.setVisible(False)
            self.moreless.setText('More Filters')
        else:
            self.adv.setVisible(True)
            self.moreless.setText('Less Filters')
            
    
    def set_selection(self, item):
        self.b.toggle(item.text())
        if item.text() in self.b.selected:
            item.setForeground(BLUE)
        else:
            item.setForeground(BLACK)
            

    def filter(self):
        self.list.clear()

        unchecked = [name for name, checkbox in self.checkboxes.items() if not checkbox.isChecked()]
       
        for name, object in self.b.objects.items():
            if object.kind in self.parent.kind_map[self.kind]:
                if not object.kind in unchecked:
                    if str(name) in self.b.selected:
                        item = QtGui.QListWidgetItem(name)
                        self.list.addItem(item)
                        item.setForeground(BLUE)
                    elif self.search.text() in str(name):
                        item = QtGui.QListWidgetItem(name)
                        self.list.addItem(item)        


class Floor_Tab(Filter_Tab):

    def __init__(self, b, parent):
        
        self.b = b

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(QtGui.QLabel('test'),1 ,1)

        self.adv = QtGui.QWidget()
        self.adv.setLayout(grid)

        Filter_Tab.__init__(self, b, parent, 'Floor')

        
class Space_Tab(Filter_Tab):

    def __init__(self, b, parent):
        
        self.b = b
        self.adv = None
        Filter_Tab.__init__(self, b, parent, 'Space')

class Wall_Tab(Filter_Tab):

    def __init__(self, b, parent):
        
        self.b = b
        self.adv = None
        Filter_Tab.__init__(self, b, parent, 'Wall')

class Window_Tab(Filter_Tab):

    def __init__(self, b, parent):
        
        self.b = b
        self.adv = None
        Filter_Tab.__init__(self, b, parent, 'Window')

class Polygon_Tab(Filter_Tab):

    def __init__(self, b, parent):
        
        self.b = b
        self.adv = None
        Filter_Tab.__init__(self, b, parent, 'Polygon')

class Other_Tab(Filter_Tab):

    def __init__(self, b, parent):
        
        self.b = b
        self.adv = None
        Filter_Tab.__init__(self, b, parent, 'Other')
    

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Batch()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()