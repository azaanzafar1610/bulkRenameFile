import os
import re

#importing item models and item which reflect each 'listview' in the GUI 
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5 import uic

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi('bulkgui.ui', self) #loading the gui file into the 'self' object
        self.show()

        self.directory = "."
        #initializing a model where we will store 'data'
        self.listModel = QStandardItemModel()
        self.selectModel = QStandardItemModel()

        #setting the model for the view
        self.selectView.setModel(self.selectModel)
        self.selected = []     #keeping track of everythign that has been selected in a list/arr

        #connecting each button from the GUI to their respective functions when the button is triggered/clicked
        #eg. .filgerButton, .selectButton are the names for the buttons which are in the GUI
        self.actionOpen.triggered.connect(self.load_directory)
        self.filterButton.clicked.connect(self.filter_list)
        self.selectButton.clicked.connect(self.choose_selection)
        self.removeButton.clicked.connect(self.remove_selection)
        self.applyButton.clicked.connect(self.rename_files)

    def load_directory(self):
        #this will store the directory the user opens
        self.directory = QFileDialog.getExistingDirectory(self, "Select Directory")

        #we are going through each file in the directory 
        for file in os.listdir(self.directory):
            #.isfile allows us to ONLY get the files and not any folders in the directory. we just want to focus on files.
            if os.path.isfile(os.path.join(self.directory, file)):
                #for each file name a 'QStandardItem' is created with the param as a file and then added to the QstandardItemModel 
                #named 'listModel' using appendRow
                self.listModel.appendRow(QStandardItem(file))
        #this will present the data in listView (in our gui) from the listModel 
        self.listView.setModel(self.listModel)

 
    def rename_files(self):
        counter = 1
        for filename in self.selected:
            #checking if a radio is selected
            if self.addPrefixRadio.isChecked():
                #adding a prefix to start of file name
                os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, self.nameEdit.text() + filename))
            #removing file(s) from the directory
            elif self.deleteRadioButton.isChecked():
                os.remove(os.path.join(self.directory, filename))
            #removing a prefix from start of file name
            elif self.removePrefixRadio.isChecked():
                if filename.startswith(self.nameEdit.text()):
                    os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, self.filename[len(self.nameEdit.text()):]))
            #adding suffix at the end of file name
            elif self.addSuffixRadio.isChecked():
                filetype = filename.split('.')[-1]
                os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, filename[:-(len(filetype) + 1)] + self.nameEdit.text() + "."+ filetype))
            #removing suffix at the end of file name
            elif self.removeSuffixRadio.isChecked():
                filetype = filename.split('.')[-1]
                if filename.endswith(self.nameEdit.text() + "." + filetype):
                    os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, filename[:-len(self.nameEdit.text() + '.' + filetype)] + "."+ filetype))
            #renaming file
            elif self.newNameRadio.isChecked():
                #splits the filename --> access the last value in the array which is basically the filetyp
                #eg filename = abcdy.pdf
                # .split(".") result --> ['abcdy', '.pdf']
                #[-1] accesses the last val in array, result--> filetype= pdf
                filetype = filename.split('.')[-1]
                #here we rename the file and increment the counter by 1
                #this is so that if there are multiple files with the same name, itll automatically disinguish them by the counter 
                #eg file1, file2...
                os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, self.nameEdit.text()+ str(counter) +  "." + filetype))
                counter+=1
            else:
                print("Select a radio button")
            
            self.selected = []
            self.selectModel.clear()
            self.listModel.clear()
            
            for file in os.listdir(self.directory):
                if os.path.isfile(os.path.join(self.directory, file)):
                    self.listModel.appendRow(QStandardItem(file))
                self.listView.setModel(self.listModel)
    def choose_selection(self):
        #if not empty
        if len(self.listView.selectedIndexes()) !=0:
            for index in self.listView.selectedIndexes():
                if index.data() not in self.selected:
                    self.selected.append(index.data())
                    self.selectModel.appendRow(QStandardItem(index.data()))

    def remove_selection(self):
        try:
            if len(self.selectView.selectedIndexes()) != 0:
                #we reverse the positions of the file so that it mathces the original positions
                #if we dont reverse, it will then try remove something which doesnt 'exist' and give an error
                for index in reversed(sorted(self.selectView.selectedIndexes())):
                    self.selected.remove(index.data())
                    self.selectModel.removeRow(index.row())
        except Exception as e:
            print(e)

    def filter_list(self):
        self.selectModel.clear()
        self.selected = []
        for index in range(self.listModel.rowCount()):
            item = self.listModel.item(index)
            if re.match(self.filterEdit.text(), item.text()):
                self.selectModel.appendRow(QStandardItem(item.text()))
                self.selected.append(item.text())

app = QApplication([])
window = MyGUI()
#starts the event loop / app starts running 
app.exec_() 