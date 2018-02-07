#!/usr/bin/env python
# -----------------------------------------------
__author__ = "DADIC  Andro"
__version__ = "1.0.0"
# Release Notes ---------------------------------
"""
--/--/2017 : Creation of the window
--/--/2017 : Drawing of a watch
24/01/2018 : Definition of DoQuit() and DoNew()
26/01/2018 : Definition of DoImport() and DoExport()
"""
# -----------------------------------------------
from threading import Thread
from tkinter import *
from generation import *
# from fitness import *
import pickle
import time

_thread, _pause = None, True
k = 0


def doExport():
    my_file = open("save_data.txt", "w")
    my_file.write("generation 1")
    my_file.close()
    score = [0, 1, 2]
    with open('database', 'wb') as data:
        my_pickler = pickle.Pickler(data)
        my_pickler.dump(score)
    return


def doImport():
    with open('database', 'rb') as data:
        my_depickler = pickle.Unpickler(data)
        score = my_depickler.load()
    return


class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Projet Mon(s)tres")

        # ********MAIN MENU***********
        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.fileMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="New", command=self.doNew)
        self.fileMenu.add_command(label="Export", command=doExport)
        self.fileMenu.add_command(label="Import", command=doImport)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.doQuit)

        self.editMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.editMenu)
        self.editMenu.add_command(label="Play", command=self.doPlay)
        self.editMenu.add_command(label="Stop", command=self.doStop)

        # **********Toolbar*************
        self.toolbar = Frame(self)

        self.buttonPlay = Button(self.toolbar, text="Play", command=self.doPlay)
        self.buttonPlay.pack(side=LEFT, padx=2, pady=2)
        self.buttonExport = Button(self.toolbar, text="Export", command=doExport)
        self.buttonExport.pack(side=LEFT, padx=2, pady=2)
        self.buttonExport = Button(self.toolbar, text="Import", command=doImport)
        self.buttonExport.pack(side=LEFT, padx=2, pady=2)
        self.buttonQuit = Button(self.toolbar, text="Exit", command=self.doQuit)
        self.buttonQuit.pack(side=RIGHT, padx=2, pady=2)

        self.toolbar.pack(side=BOTTOM, fill=X)

        # *************Canvas***********
        self.Gui = Canvas(self, width=800, height=800, background="white")
        self.Gui.pack(side=TOP)
        self._thread, self._pause, self._stop = None, False, True
        self.k = 0


    def doNew(self):
        if self._thread is not None:
            self._thread, self._pause, self._stop = None, False, True
        self.destroy()
        self.__init__()

    def doQuit(self):
        if self._thread is not None:
            self._thread, self._pause, self._stop = None, False, True
        self.destroy()

        return


    def action(self):
        for i in range(1000):
            if self._stop:
                break
            while self._pause:
                print("Pause... (count: {})".format(i))
                time.sleep(0.1)
            print("Playing... (count: {})".format(i))
            time.sleep(0.1)
        print("Stopped.")


    def doPlay(self):
        if self._thread is None:
            self._stop = False
            self._thread = Thread(target=self.action)
            self._thread.start()
        self._pause = False
        self.buttonPlay.configure(text="Stop", command=self.doStop)

        if self.k == 0:
            self.k += 1
            nbMonstres = 1
            minObj = 5
            maxObj = 20
            gen = generate(nbMonstres, minObj, maxObj)
            # print(gen)
            j = 0

            for j in range(0, len(gen[0])):
                item = gen[0][j]

                if item.__class__.__name__ == "Gear":
                    r = item.nb_teeth * GEARS_MODULE / 4
                    x = item.x_position / 4
                    y = item.y_position / 4
                    cercle = self.Gui.create_oval(10 + x - r, 10 + y - r, 10 + x + r, 10 + y + r, fill="", outline="black",
                                                  width=3)

                elif item.__class__.__name__ == "Escape_Wheel":
                    r = item.nb_teeth * GEARS_MODULE / 4
                    x = item.x_position / 4
                    y = item.y_position / 4
                    cercle = self.Gui.create_oval(10 + x - r, 10 + y - r, 10 + x + r, 10 + y + r, fill="", outline="orange",
                                             width=3)

                elif item.__class__.__name__ == "Barrel":
                    r = item.nb_teeth * GEARS_MODULE / 4
                    x = item.x_position / 4
                    y = item.y_position / 4
                    cercle = self.Gui.create_oval(10 + x - r, 10 + y - r, 10 + x + r, 10 + y + r, fill="", outline="red",
                                             width=3)

                elif item.__class__.__name__ == "Balance_Wheel":

                    x = item.x_position / 4
                    y = item.y_position / 4
                    cercle = self.Gui.create_oval(10 + x - 20, 10 + y - 20, 10 + x + 20, 10 + y + 20, fill="", outline="green",
                                             width=3)

                elif item.__class__.__name__ == "Hand":

                    x = item.x_position / 4
                    y = item.y_position / 4
                    line = self.Gui.create_line(10 + x, 10 + y,
                                           10 + x + 25, 10 + y, fill="violet", width=2)
                elif item.__class__.__name__ == "Fork":
                    x = item.x_position / 4
                    y = item.y_position / 4
                    line = self.Gui.create_line(10 + x - 12, 10 + y - 12, 10 + x, 10 + y, 10 + x - 12, 10 + y + 12, 10 + x,
                                           10 + y,
                                           10 + x + 15, 10 + y, fill="grey", width=2)

                elif item.__class__.__name__ == "Axis":
                    x = item.x_position / 4
                    y = item.y_position / 4
                    cercle = self.Gui.create_oval(10 + x, 10 + y, 10 + x, 10 + y, fill="", outline="blue", width=5)


    """
    Ici on doit definir les fonction de generation
    """


    def doStop(self):
        self._pause = True
        self.buttonPlay.configure(text="Play", command=self.doPlay)


window = App()
window.mainloop()
