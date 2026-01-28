import serial
from time import sleep
import numpy as np
import cv2

def setPixel(index, color):
    s.write(f"{index}c{color[0]}r{color[1]}g{color[2]}b".encode())

def show():
    s.write(b"s")

def find_image_difference(image1, image2):
    # Check if images are of the same size
    if image1.shape != image2.shape:
        print("Error: Images must be of the same size.")
        return

        # Compute the absolute difference between the two images
    diff = cv2.absdiff(image1, image2)

    # Convert the difference image to grayscale
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to create a binary mask of the differences
    _, mask = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)

    # Use the mask to extract only the differences
    result = cv2.bitwise_and(diff, diff, mask=mask)
    return result



def automap(port, num_pixels, webcam):
    global s
    s=port
    #sleep(2)
    cap = cv2.VideoCapture(webcam)
    sleep(2)
    radius = 41
    pixels = {}
    for i in range(num_pixels):
        # load the image and convert it to grayscale
        offImg = cap.read()[1]
        setPixel(i, (255, 255, 255))
        show()
        sleep(0.2)
        onImg = cap.read()[1]
        image = find_image_difference(onImg, offImg)
        setPixel(i, (0, 0, 0))
        show()
        sleep(0.1)
        # cv2.imshow("differences", image)
        orig = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # perform a naive attempt to find the (x, y) coordinates of
        # the area of the image with the largest intensity value
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        cv2.circle(image, maxLoc, 5, (255, 0, 0), 2)
        # display the results of the naive attempt
        cv2.imshow("MapSpark live webcam view", image)
        gray = cv2.GaussianBlur(gray, (radius, radius), 0)
        # (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        if maxVal > 10:
            pixels[i]=maxLoc
        if cv2.waitKey(33) == 27:
            break
    cv2.destroyAllWindows()
    print(pixels)
    return pixels

if __name__=="__main__":
    automap(serial.Serial("COM3"), 20, 0)