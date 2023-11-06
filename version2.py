from tkinter import *
from PIL import ImageTk,Image  
from threading import Thread
from time import sleep
import keyboard
from os.path import exists
import shutil

class Fullscreen_Window:

    def __init__(self, mainApplication):
        self.mainApplication = mainApplication
        self.initTkWindow()   
        self.addKeyBindings()
        self.initLabelForImage()

    def initTkWindow(self):
        self.tkWindow = Tk()
        self.tkWindow.state('zoomed')  # This just maximizes it so we can see the window. It's nothing to do with fullscreen.
        self.tkWindow.attributes("-fullscreen", True)
        self.tkWindow.update()
        
    def addKeyBindings(self):
        self.tkWindow.bind("<Escape>", self.onEscape)  

    def initLabelForImage(self):
        self.labelPicture = Label(self.tkWindow)
        self.labelPicture.pack()

    def displayImage(self, imagePath):
        self.plainImage = Image.open(imagePath)
        self.scaleImage()
        self.python_image = ImageTk.PhotoImage(self.plainImage)
        self.labelPicture.configure(image=self.python_image)

    def close_window(self, event=None):
        self.tkWindow.destroy()

    def onEscape(self, event=None):
        self.mainApplication.quit()

    def scaleImage(self):
        windowWidth = self.tkWindow.winfo_width()
        windowHeight = self.tkWindow.winfo_height()
        
        imageWidth = self.plainImage.width
        imageHeight = self.plainImage.height

        scaleWidth = windowWidth/imageWidth
        scaleHeight = windowHeight/imageHeight
            
        targetWidth = windowWidth
        targetHeight = windowHeight

        if scaleWidth < scaleHeight:
            targetHeight = imageHeight * scaleWidth
        else:
            targetWidth = imageWidth * scaleHeight

        self.plainImage = self.plainImage.resize((int(targetWidth),int(targetHeight)))



class ButtonWaiter:
    def __init__(self, button, minDebounceDelayInSeconds):
        self.button = button
        self.minDebounceDelayInSeconds = minDebounceDelayInSeconds
    
    def waitForPress(self):
        self.interrupt = False
        counter = 0
        while self.interrupt == False:
            if self.button.isPressed():
                counter = counter + 1
                sleep(1)
            else:
                counter = 0
            if counter >= self.minDebounceDelayInSeconds:
                break
    
    def stopWaiting(self):
        self.interrupt = True 

class FileNameDeterminer:
    def __init__(self,folderPath,fileEnding):
        self.folderPath = folderPath
        self.currentCounter = 0
        self.ending = fileEnding

    def getNextAvailableFileName(self):
        nextCandidateName = self.getNextCandidate()
        while self.doesFileExist(nextCandidateName):
            nextCandidateName = self.getNextCandidate()
        return self.folderPath + nextCandidateName

    def doesFileExist(self,fileName):
        return exists(self.folderPath + fileName)

    def getNextCandidate(self):
        self.currentCounter = self.currentCounter + 1
        prefix = ""
        if self.currentCounter < 1000:
            prefix = "0"
        if self.currentCounter < 100:
            prefix = "00"
        if self.currentCounter < 10:
            prefix = "000"
        return prefix + str(self.currentCounter) + "." + self.ending

class FakeCamera():
    def __init__(self):
        self.counter = 0

    def showPreviewAndMakePicture(self,filePath):
        self.counter = self.counter + 1
        if self.counter % 2 == 0:
            shutil.copy('./0001.jpg', filePath)
        else:
            shutil.copy('./0002.jpg', filePath)


class KeyboardButton:
    def __init__(self, button):
        self.button = button

    def isPressed(self):
        return keyboard.is_pressed(self.button)
    
class GPIOButton:
    def __init__(self):
        self.d = ""
    
    def isPressed(self):
        return True

class MainProgram:
    def __init__(self):
        self.fullscreenWindow = Fullscreen_Window(self)
        self.fullscreenWindow.displayImage('./0002.jpg')
        self.buttonWaiter = ButtonWaiter(self.getRelevantButton(),3)
        self.fileNameDetermineer = FileNameDeterminer('./','jpg')
        self.camera = FakeCamera()
        self.stop = False

    def start(self):
        Thread(target=self.waitAndToogle).start()
        self.fullscreenWindow.tkWindow.mainloop()

    def getRelevantButton(self):
        button = GPIOButton()
        if button.isPressed():
            sleep(2)
            if button.isPressed():
                button = KeyboardButton('m')
        return button

    def quit(self):
        self.stop = True
        self.buttonWaiter.stopWaiting()
        self.fullscreenWindow.close_window()

    def waitAndToogle(self):
        sleep(2)
        while self.stop == False:
            self.buttonWaiter.waitForPress()
            if self.stop == True:
                break
            nextFileNamePath = self.fileNameDetermineer.getNextAvailableFileName()
            self.camera.showPreviewAndMakePicture(nextFileNamePath)
            self.fullscreenWindow.displayImage(nextFileNamePath) 

if __name__ == '__main__':
    mainProgram = MainProgram()
    mainProgram.start()
