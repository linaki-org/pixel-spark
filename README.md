# Pixel Spark

Pixel spark is a smart addressable LED (pixel) mapping software. With it, you can create a digital LED mapping, animations, and then compile your creations to arduino code.

> [!NOTE]
> PixelSpark is a quick and dirty Python app I created a while ago.
> I keep it here for reference purposes, but if you need an open-source pixel mapping software,
> I highly recommend you check out [XLights](https://xlights.org), which is pretty much what I wanted to recreate with PixelSpark

## Installation
To install PixelSpark, just clone this repo and run `python3 -m pip install -r requirements.txt`

## Usage
First, you need to create your mapping. To do so, click the "New light chain" button and click the start (input) and then the end (output) of your chain or strip. Then, tell pixelspark the starting (input) adress and the chain length.  
Then, you can create an animation. For this, click on "New animation rect", create the start rectangle, and then move it to the animation end. Specify the animation duration and start timestamp.  
Finally, you need to compile your animations to work on an arduino. Make sure you have the Arduino IDE and the FastLED library installed. Click on the "Generate arduino code" button, specify the max adress you have on your mapping, and press enter. The code is generated and copied to your clipboard.  
You can now paste it in a new empty arduino project and upload it.  

## Enjoy !!


## Versions history
- 1.5
    - Minor bug fixes
    - Fixing compatibility with linux/older python versions
    - Adding color order rules
    - Reorganizing buttons panel
    - Reducing canvas size to work with smaller screens
    - Adding security for slide time and color
    - Switching slide time and timecode from int to float
    
- 1.4
    - Adding possibility to light a group to a certain color
    - Fixing automapper (it was not working)
    - Adding piggy code compression of same color on several pixels
    
- 1.3
    - Adding pixel sequence simulation
    - Adding play on piggy button
    - Adding automapper
