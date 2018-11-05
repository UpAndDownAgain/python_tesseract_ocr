from PIL import Image
import pytesseract
import argparse
import cv2
import os
import sys

#print cv2.__version__
ap = argparse.ArgumentParser()
ap.add_argument("-iy", "--image_y", required=True, help="path to input image of Y coordinates ")
ap.add_argument("-ix", "--image_x", required=True, help="path to input image of X coordinates ")
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing")
ap.add_argument("-o", "--output", type=str, default="output.txt", help="output file name")
args = vars(ap.parse_args())

image_x = cv2.imread(args["image_x"])
image_y = cv2.imread(args["image_y"])

gray_x = cv2.cvtColor(image_x, cv2.COLOR_BGR2GRAY)
gray_y = cv2.cvtColor(image_y, cv2.COLOR_BGR2GRAY)

if args["preprocess"] == "thresh":
    gray_y = cv2.threshold(gray_y, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray_x = cv2.threshold(gray_x, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
elif args["preprocess"] == "blur":
    gray_y = cv2.medianBlur(gray_y, 3)
    gray_x = cv2.medianBlur(gray_x, 3)

filename_x = "{}_x.png".format(os.getpid())
filename_y = "{}_y.png".format(os.getpid())

cv2.imwrite(filename_x, gray_x)
cv2.imwrite(filename_y, gray_y)

text_x = pytesseract.image_to_string(Image.open(filename_x))
text_y = pytesseract.image_to_string(Image.open(filename_y))

os.remove(filename_x)
os.remove(filename_y)

coordinates_x = text_x.split()
coordinates_y = text_y.split()

if len(coordinates_y) != len(coordinates_x):
	print("!Warning! List of X and Y coordinates dont have same length")
	exit()

outfile = open(args["output"], "w+")
outText = ""

for n in range(0, len(coordinates_y)):
	outText += coordinates_y[n]
	outText += " "
	outText += coordinates_x[n]
	outText += "\n"

outfile.write(outText)
outfile.close()

#cv2.imshow("Image", image)
#cv2.imshow("Output", gray)
#cv2.waitKey(0)
