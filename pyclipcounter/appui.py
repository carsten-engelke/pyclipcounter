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
        # Initiate variable listeners
        self.var("countCurrent").trace_add("write", self.manualUpdateTemplateIndex)
        self.obj("ListBox").bind("<<ListboxSelect>>", self.manualUpdateTextFileIndex)


    def run(self):
        self.mainwindow.mainloop()

    def obj(self, id):
        return self.builder.get_object(id)

    def var(self, id):
        return self.builder.get_variable(id)

    def manualUpdateTemplateIndex(s, index, mode, caller):
        print(str(s) + " index:" + str(index) + " mode:" + str(mode) + " caller:" + str(caller) + " newValue:" + s.var("countCurrent").get())
        try:
            s.clipIndex = int(s.var("countCurrent").get())
        except Exception as e:
            print(e.with_traceback())
        
    #still not working properly todo: repair!
    def manualUpdateTextFileIndex(s, event):
        s.clipIndex = s.obj("ListBox").curselection[0]


    def loadTextFile(self):
        filetypes = [('text files', '*.txt')]
        f = filedialog.askopenfile(title='Open a text file. Each line defines one clip',
                                   initialdir=os.getcwd(),
                                   filetypes=filetypes)
        if f != None:
            try:
                textClips = self.var("textClips")
                filelist = list()
                with open(f.name) as txtfile:
                    for line in txtfile:
                        line = line.strip("\n").strip(os.linesep)
                        filelist.append(line)
                textClips.set(filelist)
                self.var("TextFileName").set(f.name)
                self.switchUseTemplate(False)
            except:
                self.switchUseTemplate(True)

    def switchUseTemplate(self, doUseTemplate):
        if doUseTemplate:
            self.useTemplate = True
            self.var("TextFileName").set("")
            self.var("textClips").set(list())
            templateFrame = self.obj("TemplateFrame")
            for child in templateFrame.winfo_children():
                try:
                    child.configure(state=tk.NORMAL)
                except:
                    print("failed" + str(child))
            self.obj("ListBox").configure(state=tk.DISABLED)
        else:
            self.useTemplate = False
            templateFrame = self.builder.get_object("TemplateFrame")
            for child in templateFrame.winfo_children():
                try:
                    child.configure(state=tk.DISABLED)
                except:
                    print("failed:" + str(child))
            self.obj("ListBox").configure(state=tk.NORMAL)

    def unloadTextFile(self):
        self.switchUseTemplate(True)

    def setClipIndexTemplate(self, newIndex):
        try:
            if newIndex >= int(self.var("countStart").get()):
                if newIndex <= int(self.var("countEnd").get()):
                    self.clipIndex = newIndex
                    self.var("countCurrent").set(str(newIndex))
                else:
                    self.clipIndex = int(self.var("countEnd").get())
                    self.var("countCurrent").set(self.var("countEnd").get())
            else:
                self.clipIndex = int(self.var("countStart").get())
                self.var("countCurrent").set(self.var("countStart").get())
            return True
        except Exception as e:
            return False

    def setClipIndexTextFile(self, newIndex):
        try:
            if len(self.var("textClips").get()) > 0:
                if newIndex < len(self.var("textClips").get()):
                    self.clipIndex = newIndex
                    self.obj("ListBox").activate(newIndex)
                else: 
                    self.clipIndex = len(self.var("textClips").get()) - 1
                    self.obj("ListBox").activate(len(self.var("textClips").get()) - 1)
                return True
            else:
                return False
        except Exception as e:
            return False

    def copyTemplateClip(self):
        s = self.var("clipTemplate").get()
        snumber = str(self.clipIndex)
        if self.var("isUsingLeadingZeroes").get():
            maxlen = math.floor(math.log10(int(self.var("countEnd").get())))
            snumber = (maxlen - math.floor(math.log10(self.clipIndex))) * "0" + str(self.clipIndex)
        s = s.replace("<>", snumber)
        print(s)
        pyperclip.copy(s)
        

    def copyTextClip(self):
        s = self.var("textClips").get()
        print (s)
        pyperclip.copy(s)



    def copyLastClip(self):
        newIndex = self.clipIndex - 1
        if self.useTemplate and self.setClipIndexTemplate(newIndex):
                self.copyTemplateClip()
        else:
            if self.setClipIndexTextFile(newIndex):
                self.copyTextClip()


    def copyCurrentClip(self):
        if self.useTemplate and self.setClipIndexTemplate(self.clipIndex):
            self.copyTemplateClip()
        else:
            self.setClipIndexTextFile(self.clipIndex)
            self.copyTextClip()

    def copyNextClip(self):
        newIndex = self.clipIndex + 1
        if self.useTemplate and self.setClipIndexTemplate(newIndex):
            self.copyTemplateClip()
        else:
            self.setClipIndexTextFile(newIndex)
            self.copyTextClip()


if __name__ == "__main__":
    app = PyClipCounterUI()
    app.run()
