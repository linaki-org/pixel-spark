# Pixel Spark

Pixel spark is an adressable LED (pixel) mapping software. With it, you can crete your mapping, your animations, and then compile everything into arduino code.

> [!NOTE]
> PixelSpark is a quick and dirty Python app I created a while ago.
> I keep it here for reference purposes, but if you need an open-source pixel mapping software,
> I highly recommend you check out [XLights](https://xlights.org), which is pretty much what I wanted to recreate with PixelSpark

## Installation
This repo isn't very up-to-date. For the latest versions, go on [gitlab](https://gitlab.com/linaki/pixel-spark)
To install pixel spark, you can clone this repo , install pyperclip and python-tk and run pixelspark.py, or donwload pixel.exe (I am sorry, actually, the executable version only works on a 64 bits intel cpu windows computer ☹)

## Usage
First, you need to create your mapping. To do so, click the "New light chain" button and click the start (input) and then the end (output) of your chain or strip. Then, tell pixelspark the starting (input) adress and the chain length.  
Then, you can create an animation. For this, click on "New animation rect", create the start rectangle, and then move it to the animation end. Specify the animation duration and start timestamp.  
Finally, you need to compile your animations to work on an arduino. Make sure you have the Arduino IDE and the FastLED library installed. Click on the "Generate arduino code" button, specify the max adress you have on your mapping, and press enter. The code is generated and copied to your clipboard.  
You can now paste it in a new empty arduino project and upload it.  

## Enjoy !!
