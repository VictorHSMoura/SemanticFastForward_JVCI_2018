# coding=utf8

from Tkinter import *
import Tkinter as tk
import Tkconstants, tkFileDialog
import os, matlab.engine, subprocess
from functools import partial
from video import Video
from hyperlapse import SemanticHyperlapse
from stabilizer import Stabilizer
from hyperlapseExceptions import InputError
import threading, sys

class MainWindow(object):
    def __init__(self, root):
        self.root = root
        self.inputFile = []
        self.extractor = []
        self.speedUp = None
        self.weights = []
        self.errorLabel = None
        self.buttons = []
        self.logText = None

    def start(self):
        self.setInputFileLabel()
        self.setExtractor()
        self.setSpeedUpEntry()
        self.setWeightsEntries()
        self.setErrorLabel()
        self.setButtons()
        self.setMenu()
        self.root.title('Semantic Hyperlapse')
        self.root.mainloop()

    def setInputFileLabel(self):
        Label(self.root, text = 'Input Video: ').grid(row=0, sticky=W)
        self.inputFile.append(StringVar())
        self.inputFile.append(Label(self.root, textvariable = self.inputFile[0]))
        self.inputFile.append('')

        self.inputFile[1].grid(row=0, column=1, columnspan=2)

    def setExtractor(self):
        Label(self.root, text = "Extractor: ").grid(row=1, sticky=W)
        self.extractor.append(StringVar())
        self.extractor.append(
            Radiobutton(self.root, text = "face",
                        variable=self.extractor[0], value="face")
        )
        self.extractor.append(
            Radiobutton(self.root, text = "pedestrian",
                        variable=self.extractor[0], value="pedestrian")
        )
        
        self.extractor[1].grid(row=1, column=1)
        self.extractor[2].grid(row=1, column=2)

    def setSpeedUpEntry(self):
        Label(self.root, text = 'Final Speed: ').grid(row=2, sticky=W)
        self.speedUp = tk.Entry(self.root, width=4)

        self.speedUp.grid(row=2, column=1, columnspan=2, sticky=W+E+N+S)

    def setWeightsEntries(self):
        weight_names = ['α', 'β', 'γ', 'η']

        for i in range(len(weight_names)):
            Label(self.root,
                  text = weight_names[i] + ' Weights: ').grid(row=i+3, sticky=W)
            self.weights.append([tk.Entry(self.root, width=4) for _ in range(2)])
            [weight.insert(0, '50') for weight in self.weights[i]]

        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                self.weights[i][j].grid(row=i+3, column=j+1)

    def setErrorLabel(self):
        self.errorLabel = Label(self.root, text = '')

    def setButtons(self):
        self.buttons.append(
            Button(root, text='Speed Up and Stabilize', command=self.preProcessAndRun)
        )
        self.buttons[0].grid(row=7, column=1, columnspan=2)


    def setMenu(self):
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label='OpenFile', command=self.openOriginalVideo)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.root.quit)
        menubar.add_cascade(label='File', menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label='Help Index', command=self.help)
        helpmenu.add_command(label='About...', command=self.about)
        menubar.add_cascade(label='Help', menu=helpmenu)
        self.root.config(menu=menubar)

    def about(self):
        aboutscreen = tk.Toplevel(self.root)
        text = tk.Text(aboutscreen, wrap=WORD)
        scroll = tk.Scrollbar(self.root, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.tag_configure('italics', font=('Arial', 10, 'italic'))
        text.tag_configure('title', font=('Arial', 15, 'bold'))
        text.tag_configure('normal', font=('Arial', 10))
        text.insert(tk.END, 'About\n\n', 'title')
        text.insert(tk.END, 'See more about the project on:\n', 'normal')
        text.insert(tk.END, '\thttps://github.com/verlab/SemanticFastForward'
                            + '_ECCVW_2016\n', 'italics')
        text.configure(state='disabled')
        text.pack()
        aboutscreen.title('About')

    def help(self):
        helpscreen = tk.Toplevel(self.root)
        text = tk.Text(helpscreen, wrap=WORD)
        scroll = tk.Scrollbar(self.root, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.tag_configure('bold_italics', font=('Arial', 10, 'bold', 'italic'))
        text.tag_configure('title', font=('Arial', 15, 'bold'))
        text.tag_configure('subtitle', font=('Arial', 12, 'bold'))
        text.tag_configure('normal', font=('Arial', 10))
        text.insert(tk.END, 'Instructions:\n\n', 'title')
        
        text.insert(tk.END, '1: ', 'bold_italics')
        text.insert(tk.END, 'Go to File->OpenVideo and select the video '
                            + 'file that will be accelerated.\n', 'normal')
        text.insert(tk.END, '2: ', 'bold_italics')
        text.insert(tk.END, 'Choose the extractor (most semantic part) '
                            + 'for the video.\n', 'normal')
        text.insert(tk.END, '3: ', 'bold_italics')
        text.insert(tk.END, 'Choose the speedup (speedup > 1).\n', 'normal')
        text.insert(tk.END, '4: ', 'bold_italics')
        text.insert(tk.END, 'Choose graph weights α, β, γ, η. If you don\'t change '
                            + 'anything, the default parameters will be used.\n', 'normal')
        text.insert(tk.END, '5: ', 'bold_italics')
        text.insert(tk.END, 'Click on \'Speed Up and Stabilize\' and wait. Your '
                            + 'video is being accelerated and stabilized.\n', 'normal')
        
        text.configure(state='disabled')
        text.pack()
        helpscreen.title('Help')

    def openOriginalVideo(self):
        videoFile = tkFileDialog.askopenfilename(
                filetypes=([('All files', '*.*'), ('MP4 files', '*.mp4'),
                            ('AVI files', '*.avi')]))
        videoName = os.path.basename(videoFile)
        
        self.inputFile[0].set(videoName)
        self.inputFile[2] = videoFile

    def preProcess(self):
        video = Video(self.inputFile[2])
        speed = self.speedUp.get()
        extractor = self.extractor[0].get()
            
        alpha = [a.get() for a in self.weights[0]]
        beta = [b.get() for b in self.weights[1]]
        gama = [g.get() for g in self.weights[2]]
        eta = [e.get() for e in self.weights[3]]

        return (video, speed, extractor, alpha, beta, gama, eta)

    def preProcessAndRun(self):
        video, speed, extractor,\
            alpha, beta, gama, eta = self.preProcess()

        try:
            hyperlapse = SemanticHyperlapse(video, extractor, speed,
                                            alpha, beta, gama, eta)           
            self.createLogWindow()
            hyperlapse.run(self.addLog)
        except InputError as IE:
            self.errorLabel['text'] = IE.msg
            self.errorLabel.grid(row=8, columnspan=3)
    
    def videoStabilize(self):
        raise NotImplementedError

    def addLog(self, text, textType):
        self.logText.configure(state='normal')
        self.logText.insert('end', text, textType)
        self.logText.configure(state='disabled')
        self.logText.update_idletasks()

    def createLogWindow(self):
        log = tk.Toplevel(self.root)
        self.logText = tk.Text(log, wrap=WORD)
        scroll = tk.Scrollbar(log, command=self.logText.yview)
        self.logText.configure(yscrollcommand=scroll.set)
        self.logText.tag_configure('italics', font=('Arial', 10, 'italic'))
        self.logText.tag_configure('title', font=('Arial', 12, 'bold'))
        self.logText.tag_configure('normal', font=('Arial', 10))
        self.logText.pack()
        self.logText.update_idletasks()
        log.title('Semantic Hyperlapse Status')

os.chdir('../') # going to the main project folder
root = Tk()
window = MainWindow(root)
window.start()

