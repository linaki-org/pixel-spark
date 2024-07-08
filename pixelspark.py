"""I am sorry, this code is really bad 💩. You know it and I know it."""

import tkinter as TK
from tkinter.simpledialog import askstring, askinteger
from tkinter.messagebox import showinfo, askyesno
from tkinter.colorchooser import askcolor
import pyperclip

class Pixel:
    def __init__(self, x, y, color, id):
        self.x=x
        self.y=y
        self.r, self.g, self.b=color
        self.id=id

class App:
    def __init__(self):
        self.tk=TK.Tk()
        self.tk.title("Pixel Spark")
        self.can = TK.Canvas(self.tk, height=900, width=1500, background="black")
        self.can.pack()
        TK.Button(self.tk, text="New light chain", command=lambda: self.can.bind("<Button-1>", self.newChain)).pack()
        TK.Button(self.tk, text="New animation rect", command=lambda: self.can.bind("<Button-1>", self.newAnimationRect)).pack()
        TK.Button(self.tk, text="Generate arduino code", command=self.generateArduino).pack()
        self.pixels=[]
        self.ovals=[]
        self.start=None
        self.chain=None
        self.rect=None
        self.coords=None
        self.frames={}


    def newChain(self, e):
        self.start=e.x, e.y
        self.chain=self.can.create_line(*self.start, self.start[0]+1, self.start[1]+1, fill="white")
        self.can.unbind("<Button-1>")
        self.can.bind("<Button-1>", self.finishChain)
        self.can.bind("<Motion>", self.moveChain)

    def moveChain(self, e):
        self.can.coords(self.chain, *self.start, e.x, e.y)

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
            self.ovals.append(self.can.create_oval(x-3, y-3, x+3, y+3, fill="black", outline="red"))
        self.can.delete(self.chain)

    def newAnimationRect(self, e):
        self.start = e.x, e.y
        self.rect = self.can.create_rectangle(*self.start, self.start[0] + 1, self.start[1] + 1, fill="white")
        self.can.unbind("<Button-1>")
        self.can.bind("<Button-1>", self.finishRect)
        self.can.bind("<Motion>", self.moveRect)

    def finishRect(self, e):
        self.can.unbind("<Button-1>")
        self.can.unbind("<Motion>")
        self.can.bind("<Motion>", self.moveAnimationEnd)
        self.can.bind("<Button-1>", self.finishAnimationRect)
        self.coords=self.start, (e.x, e.y)
        self.start=e.x, e.y


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
        time=askinteger("Pixel Spark", "Enter slide time in seconds")*100
        start=askinteger("Pixel Spark", "Enter start time in seconds from the beginning")*100
        off=askyesno("Pixel Spark", "Do you want LEDs to turn off after rect passage ?")
        color=askcolor(title="Pixel Spark")[0]
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
                self.frames[start+i] |= pixels
        print(self.frames)

    def moveAnimationEnd(self, e):
        self.can.move(self.rect, e.x-self.start[0], e.y-self.start[1])
        self.start = e.x, e.y
    def generateArduino(self):
        lastFrame=0
        frames=list(self.frames.keys())
        frames.sort()
        numLeds=askinteger("Pixel Spark", "How many LEDS do you want to compile for ?")
        code="#include <FastLED.h>\nCRGB leds[%s];void setup() {FastLED.addLeds<WS2812B, 5>(leds, %s);}\nvoid loop() {"%(numLeds, numLeds)
        for frame in frames:
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



a=App()
if __name__ == '__main__':
    a.tk.mainloop()
