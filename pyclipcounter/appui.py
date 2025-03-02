#!/usr/bin/python3
import pathlib
import tkinter as tk
from tkinter import filedialog
import pygubu
import pyperclip
import os, math

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
        self.useTemplate = True
        self.clipIndex = 0
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
            self.useTemplate = True
            self.var("TextFileName").set("")
            self.var("ClipList").set(list())
            templateFrame = self.obj("TemplateFrame")
            for child in templateFrame.winfo_children():
                try:
                    child.configure(state="enable")
                except:
                    print("failed" + str(child))
            # self.obj("ListBox").configure(state="disabled")
        else:
            self.useTemplate = False
            templateFrame = self.builder.get_object("TemplateFrame")
            for child in templateFrame.winfo_children():
                try:
                    child.configure(state="disabled")
                except:
                    print("failed:" + str(child))
            # self.obj("ListBox").configure(state="enable")

    def unloadTextFile(self):
        self.switchUseTemplate(True)

    def setClipIndexTemplate(self, newIndex):
        if newIndex >= self.var("countStart").get():
            if newIndex <= self.var("countEnd").get():
                self.clipIndex = newIndex
                self.var("countCurrent").set(newIndex)
            else:
                self.clipIndex = self.var("countEnd").get()
                self.var("countCurrent").set(self.var("countEnd").get())
        else:
            self.clipIndex = self.var("countStart").get()
            self.var("countCurrent").set(self.var("countStart").get())

    def setClipIndexTextFile(self, newIndex):
        if len(self.var("ClipList")) > 0 and newIndex < len(self.var("ClipList")):
            self.clipIndex = newIndex
            self.obj("ListBox").activate(newIndex)

    def copyTemplateClip(self):
        s = self.var("clipTemplate").get()
        snumber = str(self.clipIndex)
        if self.var("isUsingLeadingZeroes").get():
            maxlen = math.floor(math.log10(self.var("countEnd").get()))
            snumber = (maxlen - math.floor(math.log10(self.clipIndex))) * "0" + str(self.clipIndex)
        s = s.replace("<>", snumber)
        print("Copy Template Clip:" + s)
        

    def copyTextclip(self):
        print("Copy Text Clip:" + str(self.clipIndex))


    def copyLastClip(self):
        newIndex = self.clipIndex - 1
        if self.useTemplate:
            self.setClipIndexTemplate(newIndex)
            self.copyTemplateClip()
        else:
            self.setClipIndexTextFile(newIndex)
            self.copyTextClip()


    def copyCurrentClip(self):
        if self.useTemplate:
            self.setClipIndexTemplate(self.clipIndex)
            self.copyTemplateClip()
        else:
            self.setClipIndexTextFile(self.clipIndex)
            self.copyTextClip()

    def copyNextClip(self):
        newIndex = self.clipIndex + 1
        if self.useTemplate:
            self.setClipIndexTemplate(newIndex)
            self.copyTemplateClip()
        else:
            self.setClipIndexTextFile(newIndex)
            self.copyTextClip()


if __name__ == "__main__":
    app = PyClipCounterUI()
    app.run()
