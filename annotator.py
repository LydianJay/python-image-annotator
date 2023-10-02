import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox as ms

from tkinter import filedialog as fd
from PIL import Image, ImageTk
import pandas as pd
import os
import shutil
import updator as up



class MyApp:
    def __init__(self):
        self.appVer = "1.4"
        #reqVer = up.getVersion()
        #if reqVer != "FAIL" and reqVer != self.appVer:
        #    ms.showinfo("Update Available: " + reqVer, "https://github.com/LydianJay/python-image-annotator")

        self.window = tk.Tk()
        self.window.geometry("600x600")  
        self.window.resizable(False, False) 
        self.window.title("Image Annotator")
        self.folderPath = ""
        self.imagePath = []
        self.currentIndex = 0
        self.tkImage= None
        self.showImage = False
        self.imageLabel = tk.Label(self.window, text='NO IMAGE')
        self.initMenuBar()
        self.initExtraWidget()


        self.classes = pd.DataFrame()
        self.classes['Filename'] = []

        self.window.bind("<F1>", self.keyF1Press)
        self.window.bind("<F2>", self.keyF2Press)
        self.window.bind("<F3>", self.keySetValue)
        self.window.bind("<Up>", self.keySelectUp)
        self.window.bind("<Down>", self.keySelectDown)
        
        
    def nextImage(self):
        if self.currentIndex < len(self.imagePath) - 1:
            self.currentIndex += 1 
            self.updateImageDisplay()
            self.updateClassValueDisplay()
            self.idxLbl.configure(text=str(self.currentIndex)+"/"+str(len(self.imagePath) - 1))
            self.fileNameLbl.configure(text=os.path.basename(self.imagePath[self.currentIndex]))

    def prevImage(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.updateImageDisplay()
            self.updateClassValueDisplay()
            self.idxLbl.configure(text=str(self.currentIndex)+"/"+str(len(self.imagePath) - 1))
            self.fileNameLbl.configure(text=os.path.basename(self.imagePath[self.currentIndex]))
    
    def saveAnnotation(self):
        saveFilePath = fd.asksaveasfilename(defaultextension='.csv')
        if saveFilePath:
            self.classes.to_csv(saveFilePath, index=False)
        
    def updateClassValueDisplay(self):
        idx = self.classSelector.current()
        if idx < 0:
            return

        current_values = list(self.classSelector['values'])
        strVal = current_values[idx]
        valStr = str(self.classes.at[self.currentIndex, strVal])
        self.classVal.configure(text=valStr)
            
    def updateCallback(self, event):
        self.updateClassValueDisplay()
        

    def initMenuBar(self):
        self.menuBar = tk.Menu(self.window, bg="#A0A0A0")
        self.menuBar.add_command(label="OPEN FOLDER", command=self.openFolder)
        self.menuBar.add_command(label="FOLDER RENAME", command=self.renameFilesInFolder)
        self.menuBar.add_command(label="NEXT", command=self.nextImage)
        self.menuBar.add_command(label="PREV", command=self.prevImage)
        self.menuBar.add_command(label="ADD", command=self.addImage)
        self.menuBar.add_command(label="DEL", command=self.deleteImage)
        self.menuBar.add_command(label = "SAVE CSV", command=self.saveAnnotation)
        self.menuBar.add_command(label = "LOAD CSV", command=self.openCSV)
        
        self.window.config(menu=self.menuBar, bg="#8592a1")

        



    def keySetValue(self, event):
        self.setValue()

    def keyF1Press(self, event):
        self.prevImage()

    def keyF2Press(self, event):
        self.nextImage()

    
    def deleteImage(self):
        temp = self.imagePath[self.currentIndex]
        os.remove(self.imagePath[self.currentIndex])
        self.classes.drop(self.currentIndex, inplace=True, axis=0)
        self.classes.reset_index(inplace= True, drop =True)
        self.imagePath.remove(temp)
        self.updateClassValueDisplay()
        self.updateImageDisplay()
        self.idxLbl.configure(text="0/"+str(len(self.imagePath) - 1))
        self.fileNameLbl.configure(text=os.path.basename(self.imagePath[self.currentIndex]))
        



    def keySelectUp(self, event):
        idx = self.classSelector.current()
        

        if idx > 0:
            idx -= 1
            self.classSelector.current(idx)
            self.updateClassValueDisplay()

    def keySelectDown(self, event):
        idx = self.classSelector.current()
        sz = len(self.classSelector['values'])

        if idx < sz - 1:
            idx += 1
            self.classSelector.current(idx)
            self.updateClassValueDisplay()



    def addImage(self):
        dir = fd.askdirectory()
        ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        if dir:
            for fileName in os.listdir(dir):
                if fileName.lower().endswith(ext):
                    shutil.copy(os.path.join(dir, fileName), self.folderPath)
                    self.imagePath.append(os.path.join(self.folderPath, fileName))
                    temp = [0 for i in range(len(self.classes.columns.values) - 1)]
                    temp.insert(0, fileName)
                    self.classes = pd.concat([self.classes, pd.DataFrame([temp], columns=self.classes.columns.values)], ignore_index=True)
                    
                    

            self.updateClassValueDisplay()
            self.idxLbl.configure(text=str(self.currentIndex) + "/" + str(len(self.imagePath) - 1))
            self.fileNameLbl.configure(text=os.path.basename(self.imagePath[self.currentIndex]))

                    
                    





    def initExtraWidget(self):
        self.label1 = tk.Label(text = 'CLASSES')
        self.label1.place(x = 20, y=510)
        self.label1.update()

        self.classSelector = ttk.Combobox(self.window)
        self.classSelector.place(x = 75, y= 510)
        self.classSelector.bind('<<ComboboxSelected>>', self.updateCallback)
        self.classSelector.update()

        self.classVal = tk.Label(text='0')
        self.classVal.place(x = (self.classSelector.winfo_x() + self.classSelector.winfo_width() + 5)  , y=510)
        self.classVal.update()

        self.setButton = tk.Button(self.window, text="FLIP VALUE", command = self.setValue)
        self.setButton.place(x = (self.classVal.winfo_x() + self.classVal.winfo_width() + 5), y=510)
        self.setButton.update()


        self.createButton = tk.Button(text='CREATE CLASS', command=self.createClass)
        self.createButton.place(x = 400, y=510)
        self.createButton.update()

        self.className = tk.Text(self.window, width=10, height = 1)
        self.className.place(x = (self.createButton.winfo_x() + self.createButton.winfo_width() + 5), y=510)
        self.className.update()


        self.deleteButton = tk.Button(text='DELETE CLASS', command=self.deleteClass)
        self.deleteButton.place(x = self.className.winfo_x() - self.createButton.winfo_width() - 5, y=520 + self.className.winfo_height())
        self.deleteButton.update()


        self.lbl = tk.Label(text = 'INDEX: ')
        self.lbl.place(x = 20, y=540)
        self.lbl.update()

        self.idxLbl = tk.Label(text = '0')
        self.idxLbl.place(x = self.lbl.winfo_x() + self.lbl.winfo_width() + 5, y=540)
        self.idxLbl.update()

        self.fileNameLbl = tk.Label(text = 'NO IMAGES LOADED')
        self.fileNameLbl.place(x = 20, y=565)
        self.fileNameLbl.update()

        self.goText = tk.Text(self.window, width=4, height=1)
        self.goText.place(x = self.idxLbl.winfo_x() + self.idxLbl.winfo_width() + 150, y=540)
        self.goText.update()

        self.goButton = tk.Button(text="GO", command=self.goTo)
        self.goButton.place(x = self.goText.winfo_x() + self.goText.winfo_width() +5, y=540)
        self.goButton.update()

    def goTo(self):
        self.currentIndex = int(self.goText.get("1.0", "end-1c"))
        self.updateClassValueDisplay()
        self.updateImageDisplay()
        self.idxLbl.configure(text= str(self.currentIndex) + "/"+ str(len(self.imagePath) - 1))
        self.fileNameLbl.configure(text=os.path.basename(self.imagePath[self.currentIndex]))




    def createClass(self):
        str = self.className.get("1.0", "end-1c")
        self.className.delete("1.0", "end")
        self.classSelector['values'] = tuple( list(self.classSelector['values']) + [str])
        self.classSelector.update()
        self.classes[str] = [0 for i in range(len(self.imagePath))]
        
    
    def deleteClass(self):
        idx = self.classSelector.current()
        
        if idx != -1:
            current_values = list(self.classSelector['values'])
            self.classes = self.classes.drop(current_values[idx], axis=1)
            del current_values[idx]
            self.classSelector['values'] = tuple(current_values)
        

    def setValue(self):
        idx = self.classSelector.current()
        current_values = list(self.classSelector['values'])
        str = current_values[idx]
        
        if self.classes.at[self.currentIndex, str] == 0:
            self.classes.at[self.currentIndex, str] = 1
            self.classVal.configure(text='1')
        else:
            self.classVal.configure(text='0')
            self.classes.at[self.currentIndex, str] = 0


    def openCSV(self):
        if len(self.imagePath) <= 0:
            ms.showerror("ERROR", "No images loaded!")
            return

        filePath = fd.askopenfilename()
        if filePath:
            read = pd.read_csv(filePath)

            if len(read) != len(self.imagePath):
                ms.showerror("ERROR", "Images count does not match with csv content count!")
                return
           

            self.classes = read
            classNames = [str(item) for item in self.classes.columns.values]
            classNames.remove("Filename")
            self.classSelector['values'] = classNames
            self.updateClassValueDisplay()

    def renameFilesInFolder(self):
        dir = fd.askdirectory()
        ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        counter = 0
        
        if dir:
            for fileName in os.listdir(dir):
                if fileName.lower().endswith(ext):
                    old_path = os.path.join(dir, fileName)
                    base_name, file_extension = os.path.splitext(fileName)
                    new_name = f"{counter}{file_extension}"
                    new_path = os.path.join(dir, new_name)
                    os.rename(old_path, new_path)
                    self.imagePath.append(new_path)
                    counter += 1

    def updateImageDisplay(self):
        if self.currentIndex < 0 or self.currentIndex >= len(self.imagePath):
            return
        window_width = self.window.winfo_width()  
        window_height = self.window.winfo_height()
        fileName = self.imagePath[self.currentIndex]

        if fileName:
            image = Image.open(fileName)
            image = image.resize((window_width,window_height - 100))
            self.tkImage = ImageTk.PhotoImage(image)
            self.imageLabel.config(image=self.tkImage, text='')
            self.imageLabel.pack(fill=tk.BOTH)

    def openFolder(self):
        self.folderPath = fd.askdirectory()
        ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        self.imagePath = []
        filenames = []
        if self.folderPath:
            for fileName in os.listdir(self.folderPath):
                if fileName.lower().endswith(ext):
                    self.imagePath.append(os.path.join(self.folderPath, fileName))
                    filenames.append(fileName)
        

        if len(filenames) <= 0:
            ms.showinfo("INFO", "Folder does not contain images!")
            return

        self.classes['Filename'] = filenames
        self.updateImageDisplay()
        self.idxLbl.configure(text="0/"+str(len(filenames) - 1))
        self.fileNameLbl.configure(text=filenames[0])

                    

            


    def loop(self):
        self.window.mainloop()





if __name__ == "__main__":
    app = MyApp()
    app.loop()