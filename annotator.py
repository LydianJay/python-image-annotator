import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import pandas as pd
import os



class MyApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("600x600")  # Set the size of the window to 400x300
        self.window.resizable(False, False)  # Make the window non-resizable
        self.window.title("Anotator")
        
        self.folderPath = ""
        self.imagePath = []
        self.currentIndex = 0
        self.tkImage= None
        self.showImage = False
        self.imageLabel = tk.Label(self.window, text='NO IMAGE')
        self.initMenuBar()
        self.initExtraWidget()


        self.classes = pd.DataFrame()
        
    def nextImage(self):
        if self.currentIndex < len(self.imagePath):
            self.currentIndex += 1 
            self.updateImageDisplay()
            
    def prevImage(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.updateImageDisplay()
    
    def saveAnnotation(self):
        saveFilePath = fd.asksaveasfilename(defaultextension='.csv')
        if saveFilePath:
            self.classes.to_csv(saveFilePath, index=False)
        
      
        

    def initMenuBar(self):
        self.menuBar = tk.Menu(self.window, bg="#A0A0A0")
        self.menuBar.add_command(label="OPEN FOLDER", command=self.openFolder)
        self.menuBar.add_command(label="OPEN FILE", command=self.openFile)
        self.menuBar.add_command(label="CONTENT RENAME", command=self.renameFilesInFolder)
        self.menuBar.add_command( label="NEXT", command=self.nextImage)
        self.menuBar.add_command( label="PREV", command=self.prevImage)
        self.menuBar.add_command(label = "SAVE CSV", command=self.saveAnnotation)
        self.window.config(menu=self.menuBar, bg="#8592a1")

    def initExtraWidget(self):
        self.label1 = tk.Label(text = 'CLASSES')
        self.label1.place(x = 20, y=510)
        self.label1.update()

        self.classSelector = ttk.Combobox(self.window)
        self.classSelector.place(x = 75, y= 510)
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
            del current_values[idx]
            self.classes = self.classes.drop(current_values[idx], axis=1)
            self.classSelector['values'] = tuple(current_values)
        



    def setValue(self):
        idx = self.classSelector.current()
        current_values = list(self.classSelector['values'])
        str = current_values[idx]
        print('Old values: ', self.classes[str])
        if self.classes.at[self.currentIndex, str] == 0:
            self.classes.at[self.currentIndex, str] = 1
            self.classVal.configure(text='1')
        else:
            self.classVal.configure(text='0')
            self.classes.at[self.currentIndex, str] = 0
        print('New values: ', self.classes[str])
            




  
    def openFile(self):
        fileName = fd.askopenfilename()
        window_width = self.window.winfo_width()  
        window_height = self.window.winfo_height()  
      
        if fileName:
            image = Image.open(fileName)
            image = image.resize((window_width,window_height - 100))
            self.tkImage = ImageTk.PhotoImage(image)
            self.imageLabel.config(image=self.tkImage, text='')
            self.imageLabel.pack(fill=tk.BOTH)
            

    def renameFilesInFolder(self):
        self.folderPath = fd.askdirectory()
        ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        counter = 0
        self.imagePath = []
        
        if self.folderPath:
            for fileName in os.listdir(self.folderPath):
                if fileName.lower().endswith(ext):
                    old_path = os.path.join(self.folderPath, fileName)
                    base_name, file_extension = os.path.splitext(fileName)
                    new_name = f"{counter}{file_extension}"
                    new_path = os.path.join(self.folderPath, new_name)
                    os.rename(old_path, new_path)
                    self.imagePath.append(new_path)
                    counter += 1

    def updateImageDisplay(self):
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
        
        if self.folderPath:
            for fileName in os.listdir(self.folderPath):
                if fileName.lower().endswith(ext):
                    self.imagePath.append(os.path.join(self.folderPath, fileName))

        self.updateImageDisplay()
                    

            
        
                       
                       





    def loop(self):
        self.window.mainloop()





if __name__ == "__main__":
    app = MyApp()
    app.loop()