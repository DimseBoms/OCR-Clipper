import os, pyautogui, pytesseract, pyperclip, tkinter as tk
from PIL import ImageGrab, ImageTk, Image


screenshot = 'screenshot.png'
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'

#Renser arbeidsmappe
if os.path.exists(screenshot):
    os.remove(screenshot)
im = ImageGrab.grab()
im.save(screenshot)

copyTrue = False    #Variabel som programmet bruker for å finne ut om teksten skal kopieres. Ikke rør
capturedArea = 'capturedArea.png'

class App(tk.Frame):
    def __init__( self, parent):
        tk.Frame.__init__(self, parent)
        self._createVariables(parent)
        self._createCanvas()
        self._createCanvasBinding()

    def _createVariables(self, parent):
        self.parent = parent
        self.rectx0 = 0
        self.recty0 = 0
        self.rectx1 = 0
        self.recty1 = 0
        self.rectid = None
        self.windowx = root.winfo_screenwidth()
        self.windowy = root.winfo_screenheight()
        self.img = ImageTk.PhotoImage(Image.open(screenshot))

    def _createCanvas(self):
        self.canvas = tk.Canvas( self.parent,
                                 width = self.windowx,
                                 height = self.windowy )

        self.canvas.config(highlightthickness = 0)

        self.canvas.create_image( self.windowx,
                                  self.windowy,
                                  anchor='se',
                                  image=self.img )

        self.canvas.grid(row=0, column=0, sticky='nsew')

    def _createCanvasBinding(self):
        self.canvas.bind( "<Button-1>", self.startRect )
        self.canvas.bind( "<ButtonRelease-1>", self.stopRect )
        self.canvas.bind( "<B1-Motion>", self.movingRect )

    def startRect(self, event):
        #Oversett mus-skjerm koordinater til canvas koordinater
        self.rectx0 = self.canvas.canvasx(event.x)
        self.recty0 = self.canvas.canvasy(event.y)
        #Lager rektangel
        self.rectid = self.canvas.create_rectangle(
            self.rectx0, self.recty0, self.rectx0, self.recty0, outline='#E2475E')
        print('Rectangle {0} started at {1} {2} {3} {4} '.
              format(self.rectid, self.rectx0, self.recty0, self.rectx0,
                     self.recty0))
        #Sluttgjør startpunkt for rektangel
        global finalx0, finaly0
        finalx0 = self.rectx0
        finaly0 = self.recty0

    def movingRect(self, event):
        #Oversett mus-skjerm koordinater til canvas koordinater
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        #Modifiserer x1/y1 koordinater
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)
        print('Rectangle x1, y1 = ', self.rectx1, self.recty1)

    def stopRect(self, event):
        #Oversett mus-skjerm koordinater til canvas koordinater
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        #Modifiserer rektangel x1/y1 rektangel
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)
        print('Rectangle ended')
        #Sluttgjør rektangel sluttpunkt
        global finalx1, finaly1
        finalx1 = self.rectx1
        finaly1 = self.recty1
        destroyAndCapture()

def destroyAndCapture():
    root.destroy()
    global copyTrue
    copyTrue = True

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title('ImageClip')
    root.config(cursor="cross")
    root.bind("<Escape>", lambda x: root.destroy())
    app = App(root)
    root.mainloop()

if copyTrue == True: 
    print('Final coordinates = ' +
        str(finalx0) + ' ' + str(finaly0) + ' '+
        str(finalx1) + ' ' + str(finaly1))

    if finalx0 > finalx1:
        tempX = finalx0
        finalx0 = finalx1
        finalx1 = tempX

    if finaly0 > finaly1:
        tempY = finaly0
        finaly0 = finaly1
        finaly1 = tempY

    if os.path.exists(capturedArea):
        os.remove(capturedArea)
    im = pyautogui.screenshot(region=(finalx0, finaly0, finalx1 - finalx0, finaly1 - finaly0))
    try:
        im.save(capturedArea)
    except:
        print('Feil i tagning av skjermbilde')

try:
    if copyTrue == True:
        ocrOutput = pytesseract.image_to_string(Image.open(capturedArea), lang='nor', timeout=5).rstrip('\f\n')
        pyperclip.copy(ocrOutput)
        print('Tekst som er kopiert til utklippstavle: \n' + ocrOutput)
        messageText = 'Tekst:' + '\n' + '"' + ocrOutput + '"'

except:
    print('OCR feil')


#Rydder arbeidsområde
if os.path.exists(screenshot):
    os.remove(screenshot)
if os.path.exists(capturedArea):
    os.remove(capturedArea)
