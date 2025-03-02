#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import filedialog
import pygubu
import os

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "app.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class PyClipCounterUI:
    def __init__(
        self,
        master=None,
        translator=None,
        on_first_object_cb=None,
        data_pool=None
    ):
        self.builder = pygubu.Builder(
            translator=translator,
            on_first_object=on_first_object_cb,
            data_pool=data_pool
        )
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = self.builder.get_object("Tk1", master)
        self.builder.connect_callbacks(self)
        # Initiate variables
        useTemplate = True
        self.var("isUsingLeadingZeroes").set(True)
        self.var("isAutomaticallyNext").set(True)


    def run(self):
        self.mainwindow.mainloop()

    def obj(self, id):
        return self.builder.get_object(id)

    def var(self, id):
        return self.builder.get_variable(id)

    def loadTextFile(self):
        filetypes = [('text files', '*.txt')]
        f = filedialog.askopenfile(title='Open a text file. Each line defines one clip',
            initialdir=os.getcwd(),
            filetypes=filetypes)
        if f != None:
            try:
                cliplist = self.var("ClipList")
                filelist = list()
                with open(f.name) as txtfile:
                    for line in txtfile:
                        filelist.append(line)
                cliplist.set(filelist)
                self.var("TextFileName").set(f.name)
                self.switchUseTemplate(False)
            except:
                self.switchUseTemplate(True)

    def switchUseTemplate(self, doUseTemplate):
        if doUseTemplate:
            useTemplate = True
            self.var("TextFileName").set("")
            self.var("ClipList").set(list())
            templateFrame = self.obj("TemplateFrame")
            for child in templateFrame.winfo_children():
                try:
                    child.configure(state="enable")
                except:
                    print("failed" + str(child))
            #self.obj("ListBox").configure(state="disabled")
        else:
            useTemplate = False
            templateFrame = self.builder.get_object("TemplateFrame")
            for child in templateFrame.winfo_children():
                try:
                    child.configure(state="disabled")
                except:
                    print("failed:" + str(child))
            #self.obj("ListBox").configure(state="enable")

    def unloadTextFile(self):
        self.switchUseTemplate(True)


    def copyLastClip(self):
        pass

    def copyCurrentClip(self):
        pass

    def copyNextClip(self):
        pass


if __name__ == "__main__":
    app = PyClipCounterUI()
    app.run()
