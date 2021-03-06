#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:39:40 2017

@author: eli
"""

import sys
import os
import shelve
import random
import VerbsFromDB as DB
from fuzzywuzzy import fuzz
from playsound import playsound
from ShelveVerbs import verb
from PyQt4 import QtGui
from PyQt4 import QtCore


class QtDisplay(QtGui.QLineEdit): #custom version of QLineEdit class that
                                    # disables editing by default
    def __init__(self):
        QtGui.QLineEdit.__init__(self)
        QtGui.QLineEdit.setReadOnly(self,True)
class QtDisplayLong(QtGui.QLabel): #custom version of QLabel class that wraps
                                    #by default (for display of meaning)
    def __init__(self):
        QtGui.QLabel.__init__(self)
        self.setWordWrap(True)



class QtSectionLabel(QtGui.QLabel): #custom version of QLabel class that center
                    #aligns, bolds, and sets vertical policy to fixed by default
    def __init__(self, text):
        QtGui.QLabel.__init__(self, text='')
        QboldFont = QtGui.QFont()
        QboldFont.setBold(True)
        self.setFont(QboldFont)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)

class QtVFixedLabel(QtGui.QLabel): #custom version of the QLabel class that
                                    #sets vertical policy to fixed by default
    def __init__(self,text=''):
        QtGui.QLabel.__init__(self, text='')
        self.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        self.setText(text)

class QtFixedTextBox(QtGui.QTextEdit): #custom version of QTextEdit that
                                        #sets read only by default
    def __init__(self, text=''):
        QtGui.QTextEdit.__init__(self, text)
        QtGui.QTextEdit.setReadOnly(self,True)

class mainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.QverbBrowser = QtGui.QWidget()
        self.user = self.changeUserMsgBox(self.QverbBrowser, DB.get_userList()) #creates a dialog box for choosing a user
        if not DB.userExists(self.user):
            DB.add_user(self.user)
        self.setGeometry(100,100,800,800)
        self.QmainMenu = self.menuBar()
        self.QfileMenu = self.QmainMenu.addMenu("File")
        self.QfileMenuAbout = QtGui.QAction("About", self.QmainMenu)
        self.QfileMenu.addAction(self.QfileMenuAbout)
        self.QfileMenuAbout.triggered.connect(self.aboutAction)
        self.QfileMenuManageUsers = QtGui.QAction("Manage Users", self.QmainMenu)
        self.QfileMenu.addAction(self.QfileMenuManageUsers)
        self.QfileMenuManageUsers.triggered.connect(self.manageUsers)
        self.QfileMenuQuit = QtGui.QAction("Quit", self.QmainMenu)
        self.QfileMenu.addAction(self.QfileMenuQuit)
        self.QfileMenuQuit.setShortcut("Ctrl+Q")
        self.QfileMenuQuit.triggered.connect(self.closeApp)
        #--------------------------------------------
        # GRID LAYOUT
        #--------------------------------------------
        # The grid layout consists of three subgrids inside of 5 main grid as follows. Some of these sub grids are further subdivided
        #    ___________
        #   | np   | p&i|     NP - non-past indicative forms
        #   |______|____|     P&I - past and imperative forms
        #   |___ex______|     ex - dynamically allocated space for example sentences
        #   |vb | btn|q |     VB - verb browser (shows available verbs)
        #   |___|____|__|     btn - buttons to add verbs to quiz
        #                     q - list of verbs selected for quiz
        self.QverbBrowserGrid = QtGui.QGridLayout() #main layout
        # ---------------------------------------------
        # NON PAST FORMS AREA
        #----------------------------------------------
        #    ___________
        #   |*NP***|    |     NP - non-past indicative forms - QNPISubGrid
        #   |______|____|
        #   |   |    |  |
        #   |___|____|__|
        #
        self.QNPISubGrid = QtGui.QGridLayout()
        self.QverbBrowserGrid.addLayout(self.QNPISubGrid, 0, 0, 1, 2)
        #   this area is further subdivided as follows
        # __________________________
        # |                        |
        # |                        |
        # |      QinfoSubGrid      |
        # |________________________|
        # |                        |
        # | QNPIFormsSubGrid       |
        # |________________________|
        #
        self.QinfoSubGrid = QtGui.QGridLayout()
        self.QNPIFormsSubGrid = QtGui.QGridLayout()
        self.QNPISubGrid.addLayout(self.QinfoSubGrid,0,0,2,1)
        self.QNPISubGrid.addLayout(self.QNPIFormsSubGrid,3,0,1,1)
        #----------------------------------------------
        # NON PAST INDICATIVE AREA LABEL:
        #----------------------------------------------
        self.QnonPastPaneLabel = QtSectionLabel("Non-Past Indicative Forms")
        self.QinfoSubGrid.addWidget(self.QnonPastPaneLabel,0,0,1,4)
        # ----------------------------------------------
        # PLAY AUDIO BUTTON:
        #-----------------------------------------------
        self.QplayAudioButton = QtGui.QPushButton("Play Audio")
        self.QinfoSubGrid.addWidget(self.QplayAudioButton,1,2,1,2)
        #-----------------------------------------------
        # INFINITIVE LABEL AND BOX
        #-----------------------------------------------
        self.QinfinitiveLabel = QtVFixedLabel("Infinitive:")
        self.QinfinitiveBox = QtDisplay()
        self.QinfoSubGrid.addWidget(self.QinfinitiveLabel,1,0,1,1)
        self.QinfoSubGrid.addWidget(self.QinfinitiveBox,1,1,1,1)
        #-----------------------------------------------
        # MEANING LABEL AND BOX
        #-----------------------------------------------
        self.QmeaningLabel = QtVFixedLabel("Meaning:")
        self.QmeaningBox = QtDisplayLong()
        self.QinfoSubGrid.addWidget(self.QmeaningLabel,2,0,1,1)
        self.QinfoSubGrid.addWidget(self.QmeaningBox,2,1,1,3)

        #-----------------------------------------------
        # ASPECT LABEL AND BOX
        #-----------------------------------------------
        self.QaspectLabel = QtVFixedLabel("Aspect:")
        self.QaspectBox = QtDisplay()
        self.QinfoSubGrid.addWidget(self.QaspectLabel,3,0,1,1)
        self.QinfoSubGrid.addWidget(self.QaspectBox,3,1,1,1)
        #-----------------------------------------------
        # FEQUENCY LABEL AND BOX
        #-----------------------------------------------
        self.QfrequencyLabel = QtVFixedLabel("Frequency Number:")
        self.QfrequencyBox = QtDisplay()
        self.QinfoSubGrid.addWidget(self.QfrequencyLabel,3,2,1,1)
        self.QinfoSubGrid.addWidget(self.QfrequencyBox,3,3,1,1)
        #-----------------------------------------------
        # 1ST PERSON SINGULAR INDICATIVE
        #-----------------------------------------------
        self.QfirstSgLabel = QtVFixedLabel("1st Person Singular:")
        self.QfirstSgBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QfirstSgLabel,0,0,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QfirstSgBox,1,0,1,1)
        #-----------------------------------------------
        # 2ND PERSON SINGULAR INDICATIVE
        #-----------------------------------------------
        self.QsecondSgLabel = QtVFixedLabel("2nd Person Singular:")
        self.QsecondSgBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QsecondSgLabel,2,0,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QsecondSgBox,3,0,1,1)
        #-----------------------------------------------
        # 3RD PERSON SINGULAR INDICATIVE
        #-----------------------------------------------
        self.QthirdSgLabel = QtVFixedLabel("3rd Person Singular:")
        self.QthirdSgBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QthirdSgLabel,4,0,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QthirdSgBox,5,0,1,1)
        #-----------------------------------------------
        # 1ST PERSON PLURAL INDICATIVE
        #-----------------------------------------------
        self.QfirstPlLabel = QtVFixedLabel("1st Person Plural:")
        self.QfirstPlBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QfirstPlLabel,0,2,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QfirstPlBox,1,2,1,1)
        #-----------------------------------------------
        # 2ND PERSON PLURAL INDICATIVE
        #-----------------------------------------------
        self.QsecondPlLabel = QtVFixedLabel("2nd Person Plural:")
        self.QsecondPlBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QsecondPlLabel,2,2,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QsecondPlBox,3,2,1,1)
        #-----------------------------------------------
        # 3rd PERSON PLURAL INDICATIVE
        #-----------------------------------------------
        self.QthirdPlLabel = QtVFixedLabel("3rd Person Plural:")
        self.QthirdPlBox = QtDisplay()
        self.QNPIFormsSubGrid.addWidget(self.QthirdPlLabel,4,2,1,1)
        self.QNPIFormsSubGrid.addWidget(self.QthirdPlBox,5,2,1,1)
        # ---------------------------------------------
        # PAST AND IMPERATIVE FORMS AREA
        #----------------------------------------------
        #    ___________
        #   |      |P&I*|     P&I - Past and Imperative Forms - QPastSubGrid
        #   |______|____|
        #   |   |    |  |
        #   |___|____|__|
        #
        self.QPastSubGrid = QtGui.QGridLayout()
        self.QverbBrowserGrid.addLayout(self.QPastSubGrid,0,2,1,1)
        #----------------------------------------------
        # PAST AND IMPERATIVE AREA LABEL:
        #----------------------------------------------
        self.QPastPaneLabel = QtSectionLabel("Imperative and Past Forms")
        self.QPastSubGrid.addWidget(self.QPastPaneLabel,0,0,1,2)
        #-----------------------------------------------
        # IMPERATIVE SINGULAR
        #-----------------------------------------------
        self.QimperativeSgLabel = QtVFixedLabel("Imperative Singular:")
        self.QimperativeSgBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QimperativeSgLabel,1,0,1,1)
        self.QPastSubGrid.addWidget(self.QimperativeSgBox,1,1,1,1)
        #-----------------------------------------------
        # IMPERATIVE PLURAL
        #-----------------------------------------------
        self.QimperativePlLabel = QtVFixedLabel("Imperative Plural:")
        self.QimperativePlBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QimperativePlLabel,2,0,1,1)
        self.QPastSubGrid.addWidget(self.QimperativePlBox,2,1,1,1)
        #-----------------------------------------------
        # PAST MASCULINE
        #-----------------------------------------------
        self.QpastMascLabel = QtVFixedLabel("Past Masculine:")
        self.QpastMascBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QpastMascLabel,3,0,1,1)
        self.QPastSubGrid.addWidget(self.QpastMascBox,3,1,1,1)
        #-----------------------------------------------
        # PAST FEMININE
        #-----------------------------------------------
        self.QpastFemLabel = QtVFixedLabel("Past Feminine:")
        self.QpastFemBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QpastFemLabel,4,0,1,1)
        self.QPastSubGrid.addWidget(self.QpastFemBox,4,1,1,1)
        #-----------------------------------------------
        # PAST NEUTER
        #-----------------------------------------------
        self.QpastNeutLabel = QtVFixedLabel("Past Neuter:")
        self.QpastNeutBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QpastNeutLabel,5,0,1,1)
        self.QPastSubGrid.addWidget(self.QpastNeutBox,5,1,1,1)
        #-----------------------------------------------
        # PAST PLURAL
        #-----------------------------------------------
        self.QpastPlLabel = QtVFixedLabel("Past Plural:")
        self.QpastPlBox = QtDisplay()
        self.QPastSubGrid.addWidget(self.QpastPlLabel,6,0,1,1)
        self.QPastSubGrid.addWidget(self.QpastPlBox,6,1,1,1)
        #-----------------------------------------------
        # DYNAMICALLY ALLOCATED SPACE FOR EXAMPLES - this holder will be populated by a displayVerb function, since the number of examples
        # varies from verb to verb
        #-----------------------------------------------
        self.QexamplesGrid = QtGui.QGridLayout()
        self.QverbBrowserGrid.addLayout(self.QexamplesGrid,1,0,1,3)
        #-----------------------------------------------
        # BOTTOM SECIONS
        #-----------------------------------------------
        #    ___________
        #   |      |    |     QbottomGrid - houses the three subdivisions of the bottom sections
        #   |______|____|
        #   |***********|
        #   |___________|
        #
        self.QbottomGrid = QtGui.QGridLayout()
        self.QverbBrowserGrid.addLayout(self.QbottomGrid,2,0,1,3)
        #-----------------------------------------------
        # VERB BROWSER AREA
        #-----------------------------------------------
        #    ___________
        #   |      |    |
        #   |______|____|
        #   |vb*|    |  |     VB - verb browser (shows available verbs)
        #   |___|____|__|
        #
        #-----------------------------------------------
        self.QverbListGrid = QtGui.QGridLayout()
        self.QbottomGrid.addLayout(self.QverbListGrid,0,0,1,1)
        self.QverbListLabel = QtSectionLabel("Browse Available Verbs")
        self.QverbList = QtGui.QListWidget()
        #----------------------------------------------
        # DATE STUDIED DISPLAY
        #----------------------------------------------
        self.QdateLabel = QtVFixedLabel('Due date:')
        self.QdateDisplay = QtDisplay()
        self.QverbListGrid.addWidget(self.QdateLabel,0,0,1,1)
        self.QverbListGrid.addWidget(self.QdateDisplay,0,1,1,1)
        self.QverbListGrid.addWidget(self.QverbListLabel,1,0,1,2)
        self.QverbListGrid.addWidget(self.QverbList,2,0,1,2)
        #------------------------------------------------
        #    ___________
        #   |      |    |
        #   |______|____|
        #   |   | btn|  |
        #   |___|____|__|     btn - buttons to add verbs to quiz
        #
        #------------------------------------------------
        self.QbuttonAreaGrid = QtGui.QGridLayout()
        self.QbottomGrid.addLayout(self.QbuttonAreaGrid,0,1,1,1)
        self.QchangeUserBtn = QtGui.QPushButton("Change User")
        self.QautoQuizBtn = QtGui.QPushButton("Quiz on Most Overdue Items (auto)")
        self.QautoStudyBtn = QtGui.QPushButton("Study Next Three Verbs (auto)")
        self.QcustomQuizBtn = QtGui.QPushButton("Quiz on Custom List -->")
        self.QcustomStudyBtn = QtGui.QPushButton("Study Verbs on Custom List -->")
        self.QaddToListBtn = QtGui.QPushButton("-- Add to Quiz List -->")
        self.QremoveFromListBtn = QtGui.QPushButton("<-- Remove from Quiz List --")
        self.QbuttonAreaGrid.addWidget(self.QchangeUserBtn,0,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QautoStudyBtn,1,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QcustomStudyBtn,2,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QautoQuizBtn,3,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QcustomQuizBtn,4,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QaddToListBtn,5,0,1,1)
        self.QbuttonAreaGrid.addWidget(self.QremoveFromListBtn,6,0,1,1)
        #-------------------------------------------------
        #    ___________
        #   |      |    |
        #   |______|____|
        #   |   |    | q|
        #   |___|____|__|
        #                     q - list of verbs selected for custom quiz
        #-------------------------------------------------
        self.QcustomQuizGrid = QtGui.QGridLayout()
        self.QbottomGrid.addLayout(self.QcustomQuizGrid,0,2,1,1)
        self.QcustomQuizLabel = QtSectionLabel("Custom Quiz List")
        self.QcustomQuizList = QtGui.QListWidget()
        #----------------------------------------------
        # CURRENT USER DISPLAY
        #----------------------------------------------
        self.QuserLabel = QtVFixedLabel('Current User:')
        self.QuserBox = QtDisplay()
        self.QcustomQuizGrid.addWidget(self.QuserLabel,0,0,1,1)
        self.QcustomQuizGrid.addWidget(self.QuserBox,0,1,1,1)
        self.QcustomQuizGrid.addWidget(self.QcustomQuizLabel,1,0,1,2)
        self.QcustomQuizGrid.addWidget(self.QcustomQuizList,2,0,1,2)
        self.QverbBrowser.setLayout(self.QverbBrowserGrid)
        self.setWindowTitle("RusKey Verb Browser")
        self.setCentralWidget(self.QverbBrowser)
        self.QuserBox.setText(self.user)
        self.verbs = DB.get_SortedVerbList(self.user) #load the verb list in the relevant due date order for user
        self.QverbList.addItems(self.verbs) #add the verbs in order to the QListWidget
        self.QverbList.setCurrentRow(0) #select the first row by default
        self.QplayAudioButton.clicked.connect(self.playConjugationAudio)
        self.populateVerb() #populate the conjugation for the verb in the first row
        self.QverbList.itemSelectionChanged.connect(self.populateVerb) # any time a new row is selected, populate the conjugation for that row
        self.QaddToListBtn.clicked.connect(self.addVerbToCustom)
        self.QchangeUserBtn.clicked.connect(self.manageUsers)
        self.QremoveFromListBtn.clicked.connect(self.removeVerbFromCustom)
        self.QautoQuizBtn.clicked.connect(self.autoQuizSession)
        self.QautoStudyBtn.clicked.connect(self.autoStudySession)
        #==============================================
        # About window - this window dialog will be executed when the user clicks the "about" link in the file menu
        #==============================================
        self.QaboutWindow = QtGui.QMessageBox(self)
        self.QaboutWindow.setGeometry(150,150,300,300)
        self.QaboutWindow.setText("RusKey is an opensource project developed by Eli Ginsburg-Marcy. The examples, conjugations, and frequency rankings it contains are derived from data scraped from en.openrussian.org")
        self.QaboutWindow.setWindowTitle("About RusKey")
        self.QaboutWindow.setIcon(QtGui.QMessageBox.Information)
        self.QaboutWindow.setStandardButtons(QtGui.QMessageBox.Close)
        #==============================================
        # Manage User Window - executed when the user clicks change user in the main window or manage users from the main menu
        #==============================================
        self.QmanageUsersWindow = QtGui.QDialog(self)
        self.QmanageUsersWindow.setWindowFlags(QtCore.Qt.Window)
        self.QmanageUsersWindow.setGeometry(150,150,400,400)
        self.QmanageUsersGrid = QtGui.QGridLayout()
        self.QuserDispLabelMgUsers = QtVFixedLabel("Current User:")
        self.QuserDisplayMgUsers = QtDisplay()
        self.QuserDisplayMgUsers.setText(self.user)
        self.QchangeUserBtnMgUsers = QtGui.QPushButton("Change to Selected User")
        self.QdeleteUserBtn = QtGui.QPushButton("Delete Selected User")
        self.QuserList = QtGui.QListWidget()
        self.QmanageUsersGrid.addWidget(self.QuserDispLabelMgUsers,0,0,1,1)
        self.QmanageUsersGrid.addWidget(self.QuserDisplayMgUsers,0,1,1,1)
        self.QmanageUsersGrid.addWidget(self.QchangeUserBtnMgUsers,1,0,1,2)
        self.QmanageUsersGrid.addWidget(self.QdeleteUserBtn,2,0,1,2)
        self.QmanageUsersGrid.addWidget(self.QuserList,3,0,1,2)
        self.QmanageUsersWindow.setLayout(self.QmanageUsersGrid)
        self.QmanageUsersWindow.setWindowTitle("Manage Users")
        #==============================================
        # Quiz Window - This dialog will be executed when the user executes a study or quiz session
        #==============================================
        self.QsessionWindow = QtGui.QDialog(self.QverbBrowser)
        self.QsessionWindow.setGeometry(150,150,600,400)
        self.QsessionGrid = QtGui.QGridLayout()
        #The top portion of the session window will change depending on what is being studied/quizzed;
        #the bottom will consist of two progress bars displaying your progress on the overall quiz and your progress on the individual verbs
        #===============================================
        #Study widget for infinitive - just displays the infinitive
        self.QsessionStudyInfinitiveWidget = QtGui.QWidget()
        self.QsessionStudyInfinitiveGrid = QtGui.QGridLayout()
        self.QsessionStudyInfinitiveInfo = QtVFixedLabel('You will be quizzed on the following infinitive:')
        self.QsessionStudyInfinitiveForm = QtDisplay()
        self.QsessionStudyInfinitiveMeaning = QtFixedTextBox()
        self.QsessionStudyInfinitiveGrid.addWidget(self.QsessionStudyInfinitiveInfo)
        self.QsessionStudyInfinitiveGrid.addWidget(self.QsessionStudyInfinitiveForm)
        self.QsessionStudyInfinitiveGrid.addWidget(self.QsessionStudyInfinitiveMeaning)
        self.QsessionStudyInfinitiveWidget.setLayout(self.QsessionStudyInfinitiveGrid)
        self.QsessionGrid.addWidget(self.QsessionStudyInfinitiveWidget,0,0,1,2)
        # self.QsessionStudyInfinitiveWidget.hide()
        #=================================================
        self.QsessionQuizInfinitiveWidget = QtGui.QWidget() #this widget will be used to quiz the user on the meaning/infinitive of the verb
        self.QsessionQuizInfinitiveGrid = QtGui.QGridLayout()
        self.QsessionQuizInfinitiveInfo = QtVFixedLabel('Select the Russian verb meaning:')
        self.QsessionQuizInfinitiveMeaning = QtDisplayLong()
        self.QsessionQuizInfinitiveBtnGroup = QtGui.QButtonGroup(self.QsessionQuizInfinitiveWidget)
        self.QsessionQuizInfinitiveOptionA = QtGui.QRadioButton()
        self.QsessionQuizInfinitiveOptionB = QtGui.QRadioButton()
        self.QsessionQuizInfinitiveOptionC = QtGui.QRadioButton()
        self.QsessionQuizInfinitiveOptionD = QtGui.QRadioButton()
        self.QsessionQuizInfinitiveBtnGroup.addButton(self.QsessionQuizInfinitiveOptionA)
        self.QsessionQuizInfinitiveBtnGroup.addButton(self.QsessionQuizInfinitiveOptionB)
        self.QsessionQuizInfinitiveBtnGroup.addButton(self.QsessionQuizInfinitiveOptionC)
        self.QsessionQuizInfinitiveBtnGroup.addButton(self.QsessionQuizInfinitiveOptionD)
        self.QsessionQuizInfinitiveGrid.addWidget(self.QsessionQuizInfinitiveInfo,0,0,1,4)
        self.QsessionQuizInfinitiveGrid.addWidget(self.QsessionQuizInfinitiveMeaning,1,0,1,4)
        self.QsessionQuizInfinitiveGrid.addWidget(self.QsessionQuizInfinitiveOptionA,2,0,1,1)
        self.QsessionQuizInfinitiveGrid.addWidget(self.QsessionQuizInfinitiveOptionB,2,1,1,1)
        self.QsessionQuizInfinitiveGrid.addWidget(self.QsessionQuizInfinitiveOptionC,2,2,1,1)
        self.QsessionQuizInfinitiveGrid.addWidget(self.QsessionQuizInfinitiveOptionD,2,3,1,1)
        self.QsessionQuizInfinitiveWidget.setLayout(self.QsessionQuizInfinitiveGrid)
        self.QsessionGrid.addWidget(self.QsessionQuizInfinitiveWidget,0,0,1,2)
        self.QsessionQuizInfinitiveWidget.hide()
        #=================================================
        #Widgets for verb progress and quiz progress that are always displayed on the bottom of the session window
        self.QverbProgressLabel = QtVFixedLabel('Verb Progress')
        self.QquizProgressLabel = QtVFixedLabel('Quiz Progress')
        self.QverbProgressBar = QtGui.QProgressBar()
        self.QquizProgressBar = QtGui.QProgressBar()
        self.QsessionGrid.addWidget(self.QverbProgressLabel,1,0,1,1)
        self.QsessionGrid.addWidget(self.QquizProgressLabel,2,0,1,1)
        self.QsessionGrid.addWidget(self.QverbProgressBar,1,1,1,1)
        self.QsessionGrid.addWidget(self.QquizProgressBar,2,1,1,1)
        self.QsessionWindow.setLayout(self.QsessionGrid)


    def populateVerb(self): #function to update conjugation display when new verb in QverbList is selected
        verbKey = self.verbListtoTransInfin(self.QverbList.currentItem().text())
        print(verbKey)
        formsList = DB.get_formsList(verbKey)
        self.QinfinitiveBox.setText(formsList[0])
        self.QmeaningBox.setText(formsList[1])
        self.QaspectBox.setText(formsList[2])
        self.QfrequencyBox.setText(formsList[3])
        self.QfirstSgBox.setText(formsList[4])
        self.QsecondSgBox.setText(formsList[5])
        self.QthirdSgBox.setText(formsList[6])
        self.QfirstPlBox.setText(formsList[7])
        self.QsecondPlBox.setText(formsList[8])
        self.QthirdPlBox.setText(formsList[9])
        self.QimperativeSgBox.setText(formsList[10])
        self.QimperativePlBox.setText(formsList[11])
        self.QpastMascBox.setText(formsList[12])
        self.QpastFemBox.setText(formsList[13])
        self.QpastNeutBox.setText(formsList[14])
        self.QpastPlBox.setText(formsList[15])
        self.QdateDisplay.setText(DB.get_dueDateText(verbKey, self.user))


    def aboutAction(self):
        self.QaboutWindow.exec_()


    def manageUsers(self):
        self.QverbList.clear()
        self.QuserList.addItems(DB.get_userList())
        def verifyChangeUserBox():
            """verification window for changing users"""
            self.Qverify = QtGui.QMessageBox(self.QmanageUsersWindow)
            self.Qverify.setText("Are you sure you wish to change users?")
            self.Qverify.setIcon(QtGui.QMessageBox.Warning)
            self.Qverify.setStandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if self.QuserList.currentItem().text() != self.user:
                result = self.Qverify.exec_()
                if result == QtGui.QMessageBox.Yes:
                    self.user = self.QuserList.currentItem().text()
                    self.QuserDisplayMgUsers.setText(self.user)
                    self.QuserBox.setText(self.user)
                    self.QverbList.clear()
                    self.verbs = DB.get_SortedVerbList(self.user) #load the verb list in the relevant due date order for user
                    self.QverbList.addItems(self.verbs) #add the verbs in order to the QListWidget
                    self.QverbList.setCurrentRow(0)
        def deleteUser():
            """verification window for deleting a user"""
            if self.QuserList.currentItem().text() == self.user:
                self.Qnotice = QtGui.QMessageBox(self.QmanageUsersWindow)
                self.Qnotice.setText("Cannot delete the current user!")
                self.Qnotice.setIcon(QtGui.QMessageBox.Information)
                self.Qnotice.setStandardButtons(QtGui.QMessageBox.Ok)
                self.Qnotice.exec_()
            else:
                self.Qverify = QtGui.QMessageBox(self.QmanageUsersWindow)
                self.Qverify.setText("Are you sure you wish to DELETE the given user? This operation cannot be undone.")
                self.Qverify.setIcon(QtGui.QMessageBox.Warning)
                self.Qverify.setStandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                result = self.Qverify.exec_()
                if result == QtGui.QMessageBox.Yes:
                    DB.del_user(self.QuserList.currentItem().text())
                    self.QuserList.clear()
                    self.QuserList.addItems(DB.get_userList())

        self.QdeleteUserBtn.clicked.connect(deleteUser)
        self.QchangeUserBtnMgUsers.clicked.connect(verifyChangeUserBox)
        self.QmanageUsersWindow.exec_()

    def addVerbToCustom(self):
        target = self.QcustomQuizList.findItems(self.QverbList.currentItem().text(), QtCore.Qt.MatchExactly)
        if target == []:
            self.QcustomQuizList.addItem(self.QverbList.currentItem().text())

    def removeVerbFromCustom(self):
        rownum = self.QcustomQuizList.currentRow()
        self.QcustomQuizList.takeItem(rownum)

    def playConjugationAudio(self):
        verbAudio = './verbAudio/' + self.verbListtoTransInfin(self.QverbList.currentItem().text(),numbers=True) + '.mp3'
        print(verbAudio)
        playsound(verbAudio)



    def changeUserMsgBox(self, parent, userList):
        """create a dialog box which displays exising users and allows users to be added"""
        user, selectUser = QtGui.QInputDialog.getItem(parent,"Choose a User","Select a user or enter a new user:",userList)
        if selectUser and user != "":
            return user
        while (not selectUser) or (user == ""):
            user, selectUser = QtGui.QInputDialog.getItem(parent,"Choose a User","Select a user or enter a new user:",userList)
            if selectUser and user != "":
                return user


    def closeApp(self):
        sys.exit()





    def autoStudySession(self):
        """grabs the first three non-studied verbs from the QverbList widget and executes a study session.
        During the study session, the user is first presented with the conjugation for each of the three verbs,
        then given a brief quiz matching the infinitive to meaning. The process then repeats with each example (i.e.
        the user is presented with one example from each verb and is then quizzed on those three examples)"""
        self.studyVerbs = []
        for i in range(self.QverbList.count()):
            if len(self.studyVerbs) > 2:
                break
            verb = self.verbListtoTransInfin(self.QverbList.item(i).text())
            if not verbShelf[key].was_previouslyStudied(self.user):
                self.studyVerbs.append(key)
        self.launchSessionWindow(verbShelf)

    def autoQuizSession(self):
        """grabs the three most overdue verbs (including verbs which are not yet due if there are no overdue verbs) and
        exectues a quiz session. During the quiz session, the user is quized on matching the three infinitives to their meanings,
        then on one example from each verb, then on a second example, etc."""
        self.quizVerbs = []
        with shelve.open('./verbs/verbsDB') as verbShelf:
            for i in range(3):# grab the first three items, since these should already be in most overdue order
                verbToAdd = self.verbListtoDictKey(self.QverbList.item(i).text())
                if verbShelf[verbToAdd].was_previouslyStudied(self.user):
                    self.quizVerbs.append(verbToAdd)
            if len(self.quizVerbs) == 0:
                self.QnoVerbsStudiedWarning = QtGui.QMessageBox(self)
                self.QnoVerbsStudiedWarning.setText("You haven't studied any verbs yet. Study some verbs before attempting to review.")
                self.QnoVerbsStudiedWarning.setIcon(QtGui.QMessageBox.Warning)
                self.QnoVerbsStudiedWarning.setStandardButtons(QtGui.QMessageBox.Ok)
                self.QnoVerbsStudiedWarning.exec_()
            else:
                self.launchSessionWindow(verbShelf, study=False)

    def launchSessionWindow(self, shelf, study=True):
        """helper function for the quiz and study functions - creates widgets according to whether the user has selected study or quiz"""
        if study:
            self.sessionVerbKeys = self.studyVerbs
        else:
            self.sessionVerbKeys = self.quizVerbs
        self.sessionExampleCountList = []
        for key in self.sessionVerbKeys:
            self.sessionExampleCountList.append(len(shelf[key].get_examplesList()))
        self.sessionExampleMax = max(self.sessionExampleCountList) #session will proceed by iterating through the verbs,
        # first showing infinitives and meanings, then showing the first example, then the second, etc.;
        #self.sessionExampleMax will determine how many iterations are needed to exhaust the verb with the most examples
        print(self.sessionExampleMax)
        self.QsessionWindow.exec_()

    def getBestMatches(self, shelf, infinitive):
        """takes an open shelf file (shelf) and an infinitive form (string) and returns the three closest matching infinitives (strings) in the verbShelf DB (as a list)"""
        infinitiveList = [] #this will hold all the infinitives that do not match the given infinitive
        infinitiveScoresList = [] #this will hold scores comparing the infitives in infinitiveList to the given infinitive; the more similar, the higher the score; indexes of scores and infinitives should match
        bestMatchList = [] #the three best matches will be appended to this list
        for key in shelf:
            if key != 'users':
                if shelf[key].get_infinitive() != infinitive: # check that infinitive does not match given infintive
                    score = fuzz.ratio(shelf[key].get_infinitive(), infinitive) #calculate score based on similarity
                    infinitiveList.append(shelf[key].get_infinitive()) #add the infitive compared to the infinitiveList
                    infinitiveScoresList.append(score) #add the corresponding score to the infinitiveScoreList
        for i in range(3):
            maxScore = max(infinitiveScoresList) # pull the max score from the scores list
            maxScoreIndex = infinitiveScoresList.index(maxScore) # find the index for the element with the max score
            bestMatchList.append(infinitiveList[maxScoreIndex]) # use that index to find the corresponding infinitive
            del(infinitiveList[maxScoreIndex])
            del(infinitiveScoresList[maxScoreIndex])# delete the score and infinitive for the first best match
        return bestMatchList



    def verbListtoTransInfin(self, string, numbers=False):
        """string - a verb as listed in an item in the QverbList widget
        (e.g. "0001 быть") and returns the transliterated inifitive, with or
        without the leading frequency number (depending on the numbers
        argument, which defaults to False)"""
        transliterateDict = {'а':'a',
                             'б':'b',
                             'в':'v',
                             'г':'g',
                             'д':'d',
                             'е':'je',
                             'ё':'jo',
                             'ж':'zh',
                             'з':'z',
                             'и':'i',
                             'й':'j',
                             'к':'k',
                             'л':'l',
                             'м':'m',
                             'н':'n',
                             'о':'o',
                             'п':'p',
                             'р':'r',
                             'с':'s',
                             'т':'t',
                             'у':'u',
                             'ф':'f',
                             'х':'kh',
                             'ц':'ts',
                             'ч':'ch',
                             'ш':'sh',
                             'щ':'shch',
                             'ъ':'',
                             'ы':'y',
                             'ь':'',
                             'э':'e',
                             'ю':'ju',
                             'я':'ja',
                             chr(769):''}
        result = ""
        if not numbers:
            for letter in string:
                result += transliterateDict.get(letter, "")
        else:
            for letter in string:
                result += transliterateDict.get(letter, letter)
                result = result.replace(' ','')
        result = result.replace(' ',''""'')
        return result


if __name__ == '__main__':

    app =  QtGui.QApplication(sys.argv)
    w = mainWindow()
    w.show()
    sys.exit(app.exec_())
verbList = os.listdir('./verbs')
verbList.sort()
formsList = ['быть',
            'imperfective',
            1,
            'be',
            'бу́ду',
            'бу́дешь',
            'бу́дет',
            'бу́дем',
            'бу́дете',
            'будут',
            'бу́дь',
            'бу́дьте',
            'бы́л',
            'была́',
            'бы́ло',
            'бы́ли']
audioFile = './verbs/0001byt.mp3'
