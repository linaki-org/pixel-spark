"""I am sorry, this code is really digusting. You know it and I know it. 💩"""

import tkinter as TK
from tkinter.simpledialog import askfloat, askinteger, askstring
from tkinter.messagebox import showinfo, askyesno, showerror
from tkinter.colorchooser import askcolor
import pyperclip
from time import sleep, time
import serial
import automapper
#from colour import Colo

PIGGY_BUFFER=256
FRAME_INTERVAL=0.01

class PixelTk(TK.Tk):
    def report_callback_exception(self, exc, val, tb):
        showerror("An error occured", str(val))

class Pixel:
    def __init__(self, x, y, color, id):
        self.x=x
        self.y=y
        self.r, self.g, self.b=color
        self.id=id
        self.oval=None
        self.canvas=None

    def setColor(self, color):
        self.r, self.g, self.b=color
        self.r=int(self.r)
        self.g=int(self.g)
        self.b=int(self.b)

    def update(self):
        self.canvas.itemconfig(self.oval, fill=f'#{self.r:02x}{self.g:02x}{self.b:02x}')

    def draw(self, canvas):
        self.canvas=canvas
        self.oval = self.canvas.create_oval(self.x - 3, self.y - 3, self.x + 3, self.y + 3, fill="black", outline="grey")

class App:
    def __init__(self):
        self.tk=PixelTk()
        self.tk.title("Pixel Spark")
        self.can = TK.Canvas(self.tk, height=500, width=1000, background="black")
        self.can.pack()
        top=TK.Frame(self.tk)
        middle=TK.Frame(self.tk)
        bottom=TK.Frame(self.tk)
        top.pack()
        middle.pack()
        bottom.pack()
        TK.Button(top, text="New light chain", command=lambda: self.can.bind("<Button-1>", self.newChain)).pack(side=TK.LEFT)
        TK.Button(top, text="New animation rect", command=lambda: self.can.bind("<Button-1>", self.newAnimationRect)).pack(side=TK.LEFT)
        TK.Button(top, text="Turn selected color", command=self.selectedColor).pack(side=TK.LEFT)
        #TK.Button(top, text="Turn selected to HSV gradient", command=self.hsvGradient).pack(side=TK.LEFT)
        TK.Button(top, text="Add color order rule", command=self.colorRule).pack(side=TK.LEFT)
        TK.Button(top, text="Play", command=self.play).pack(side=TK.LEFT)
        #TK.Button(self.tk, text="         ").pack(side=TK.LEFT)
        TK.Button(middle, text="Generate arduino code", command=self.generateArduino).pack(side=TK.LEFT)
        TK.Button(middle, text="Generate lumi piggy command", command=self.generatePiggy).pack(side=TK.LEFT)
        TK.Button(middle, text="Start automapper", command=self.automapper).pack(side=TK.LEFT)
        TK.Button(middle, text="Play on piggy", command=self.playPiggy).pack(side=TK.LEFT)
        TK.Button(middle, text="Setup serial port", command=self.setupSerial).pack(side=TK.LEFT)

        self.tk.bind("<Button-1>", lambda e: self.tk.bind("<Motion>", self.select))
        self.tk.bind("<ButtonRelease-1>", lambda e: self.tk.unbind("<Motion>"))
        self.pixels=[]
        self.ovals=[]
        self.start=None
        self.chain=None
        self.rect=None
        self.coords=None
        self.serial=None
        self.frames={}
        self.selected=[]
        self.colorRules={}

    def colorRule(self):
        start=askinteger("PixelSpark", "Enter rule start address")
        length=askinteger("PixelSpark", "Enter rule length")
        order=askstring("PixelSpark", "Enter new color order like RGB")
        for i in range(length):
            self.colorRules[start+i]=order
            pixels=self.findPixelsWithId(i)



    def select(self, e):
         x, y=e.x, e.y
         for pixel in self.pixels:
            if x<pixel.x+5 and x>pixel.x-5 and y<pixel.y+5 and y>pixel.y-5:
                if pixel not in self.selected:
                    pixel.setColor((255, 255, 255))
                    pixel.update()
                    self.selected.append(pixel)
                """elif pixel!=self.selected[-1]:
                    pixel.setColor((0, 0, 0))
                    pixel.update()
                    self.selected.append(self.selected.index(pixel))"""

    def selectedColor(self):
        color=askcolor()[0]
        start=askinteger("Pixel Spark", "Enter timecode in seconds")
        if start*100 not in self.frames:
            self.frames[start*100]={}
        for pixel in self.selected:
            self.frames[start*100][pixel.id]=color
            pixel.setColor((0, 0, 0))
            pixel.update()
        self.selected=[]

    def hsvGradient(self):
        start=askcolor()
        stop=askcolor()
        if not start[0] or not stop[0]:
            return
        red = Color(start[1])
        colors = list(red.range_to(Color(stop[1]), len(self.selected)))
        for i, c in enumerate(colors):
            self.selected[i].setColor((int(c.get_red()*255), int(c.get_green()*255), int(c.get_blue()*255)))


    def newChain(self, e):
        self.start=e.x, e.y
        self.chain=self.can.create_line(*self.start, self.start[0]+1, self.start[1]+1, fill="white")
        self.can.unbind("<Button-1>")
        self.can.bind("<Button-1>", self.finishChain)
        self.can.bind("<Motion>", self.moveChain)

    def moveChain(self, e):
        self.can.coords(self.chain, *self.start, e.x, e.y)

    def findPixelsWithId(self, id):
        pixels=[]
        for pixel in self.pixels:
            if pixel.id==id:
                pixels.append(pixel)
        return pixels

    def renderPixels(self):
        computedFrames = {}
        perf = time()
        print("Rendering sequence pixels")
        for frame in self.frames:
            state = self.frames[frame]
            computedFrames[frame]=[]
            for id in state:
                color = state[id]
                pixels = self.findPixelsWithId(id)
                computedFrames[frame].append((pixels, color))
        print("Sequence pixels rendered in", time() - perf, "seconds")
        return computedFrames
    def play(self):
        passCycles=0
        computedFrames=self.renderPixels()
        for frame in sorted(list(computedFrames)):
            start=time()
            for pixels, color in computedFrames[frame]:
                for pixel in pixels:
                    pixel.setColor(color)
                    pixel.update()
                self.tk.update()
            delay=FRAME_INTERVAL-(time()-start)
            if delay>0:
                sleep(delay)


    def finishChain(self, e):
        self.can.unbind("<Button-1>")
        self.can.unbind("<Motion>")
        start=askinteger("Pixel Spark", "Enter start adress")
        numLeds=askinteger("Pixel Spark", "Enter number of leds")
        stepX=(e.x-self.start[0])/numLeds
        stepY = (e.y - self.start[1]) / numLeds
        print(stepX, stepY)
        for i in range(start, start+numLeds):
            x=self.start[0]+stepX*(i-start)
            y=self.start[1]+stepY*(i-start)
            self.pixels.append(Pixel(x, y, (0, 0, 0), i))
            self.pixels[-1].draw(self.can)
        self.can.delete(self.chain)
        self.can.unbind("<Motion>")

    def newAnimationRect(self, e):
        self.start = e.x, e.y
        self.rect = self.can.create_rectangle(*self.start, self.start[0] + 1, self.start[1] + 1, fill="white")
        self.can.unbind("<Button-1>")
        self.can.bind("<Button-1>", self.finishRect)
        self.tk.unbind("<Motion>")
        self.can.bind("<Motion>", self.moveRect)

    def finishRect(self, e):
        self.can.unbind("<Button-1>")
        self.can.unbind("<Motion>")
        self.can.bind("<Motion>", self.moveAnimationEnd)
        self.can.bind("<Button-1>", self.finishAnimationRect)
        self.coords=self.start, (e.x, e.y)


    def moveRect(self, e):
        self.can.coords(self.rect, *self.start, e.x, e.y)

    def finishAnimationRect(self, e):
        self.can.unbind("<Button-1>")
        self.can.unbind("<Motion>")
        height=self.coords[1][1]-self.coords[0][1]
        width = self.coords[1][0] - self.coords[0][0]
        startX=self.coords[0][0]
        startY=self.coords[0][1]
        stopX=self.can.coords(self.rect)[0]
        stopY=self.can.coords(self.rect)[1]
        self.can.delete(self.rect)
        while True:
            time=askfloat("Pixel Spark", "Enter slide time in seconds")
            if time!=0:
                break
            showerror("PixelSpark", "Slide time cannot be zero")
        time*=100
        time=int(time)
        start=askfloat("Pixel Spark", "Enter start time in seconds from the beginning")*100
        start=int(start)
        off=askyesno("Pixel Spark", "Do you want LEDs to turn off after rect passage ?")
        color=askcolor(title="Pixel Spark")
        if not color[0]:
            return
        color=color[0]
        stepX=(stopX-startX)/time
        stepY = (stopY - startY) / time
        lastPixels=[]
        for i in range(time):
            x=startX+stepX*i
            y=startY+stepY*i
            print(x, y)
            pixels={}

            for pixel in self.pixels:
                if (pixel.x>x and pixel.x<x+width) and (pixel.y>y and pixel.y<y+height):
                    pixels[pixel.id]=color
            if off:
                oldPixels = list(pixels.keys())
                for pixel in lastPixels:
                    if pixel not in pixels:
                        pixels[pixel]=(0, 0, 0)
                lastPixels=oldPixels

            if not pixels:
                continue
            if start+i-1 in self.frames and pixels==self.frames[start+i-1]:
                continue

            if start+i not in self.frames:
                self.frames[start+i] = pixels
            else:
                self.frames[start+i].update(pixels)
        print("[-] Frames computed")
        self.tk.unbind("<Motion>")

    def moveAnimationEnd(self, e):
        self.can.move(self.rect, e.x-self.start[0], e.y-self.start[1])
        self.start = e.x, e.y
    def generateArduino(self):
        lastFrame=0
        numLeds=askinteger("Pixel Spark", "How many LEDS do you want to compile for ?")
        code="#include <FastLED.h>\nCRGB leds[%s];void setup() {FastLED.addLeds<WS2812B, 5>(leds, %s);}\nvoid loop() {"%(numLeds, numLeds)
        for frame in sorted(list(self.frames.keys())):
            pixels=self.frames[frame]
            delay=frame-lastFrame
            delay*=10
            code+="delay(%s);"%delay
            for id in pixels:
                print(id)
                pixel=pixels[id]
                code+="leds[%s]=CRGB(%s, %s, %s);"%(id, *pixel)
            code+="FastLED.show();"
            lastFrame=frame
        code+="}"
        pyperclip.copy(code)
        showinfo("Pixel Spark", "Arduino code copied to clipboard")
        self.tk.unbind("<Motion>")
    def getColorValue(self, color, value):
        if value=="R":
            return color[0]
        elif value=="G":
            return color[1]
        else:
            return color[2]
    def transformColorOrder(self, color, order):
        transformed=[]
        for i in order:
            transformed.append(self.getColorValue(color, i))
        return tuple(transformed)

    def generatePiggy(self, copy=True):
        lastFrame=0
        code=""
        lastColor=(0, 0, 0)
        for frame in sorted(list(self.frames.keys())):
            pixels=self.frames[frame]
            delay=frame-lastFrame
            delay*=10
            for id in pixels:
                pixel=pixels[id]
                if id in self.colorRules:
                    print("Color rule found for  pixel")
                    pixel=self.transformColorOrder(pixel, self.colorRules[id])
                if pixel==lastColor:
                    code+="%sC"%id
                else:
                    code+="%sR%sG%sB%sC"%(int(pixel[0]), int(pixel[1]), int(pixel[2]), id)
                    lastColor=pixel
            lastFrame=frame
            code+="s"
        if copy:
            pyperclip.copy(code)
            showinfo("Pixel Spark", "Piggy code copied to clipboard")
        self.tk.unbind("<Motion>")
        return code

    def automapper(self):
        if not self.serial:
            showerror("Error-PixelSpark", "No serial port setup")
        pixels=automapper.automap(self.serial, askinteger("MapSpark", "How many pixels do you want to automap ?"), 0)
        for index in pixels:
            x, y = pixels[index]
            self.pixels.append(Pixel(x, y, (0, 0, 0), index))
            self.pixels[-1].draw(self.can)
        self.tk.unbind("<Motion>")

    def playPiggy(self):
        if not self.serial:
            showerror("Error-PixelSpark", "No serial port setup")
        code=self.generatePiggy(False)
        print("[-] Piggy code generated")
        for cmd in code.split("s"):
            for op in [cmd[i:i+PIGGY_BUFFER] for i in range(0, len(cmd), PIGGY_BUFFER)]:
                if not op:
                    continue
                op+="b"
                self.serial.write(op.encode())
                #print(op)
            sleep(FRAME_INTERVAL)
            self.serial.write(b"s")
        self.tk.unbind("<Motion>")
    def setupSerial(self):
        port=askstring("PixelSpark port setup", "Enter serial port")
        try:
            self.serial=serial.Serial(port, 115200)
        except serial.SerialException as e:
            showerror("Error-PixelSpark", e)
        self.tk.unbind("<Motion>")



a=App()
if __name__ == '__main__':
    a.tk.mainloop()
