import argparse

def readFile(filename):
	with open(filename) as file:
		content = file.readlines()
	content = [x.strip() for x in content]
	return content

ap = argparse.ArgumentParser()
ap.add_argument("-ix", "--input_x", required=True, help="input file 1")
ap.add_argument("-iy", "--input_y", required=True, help="input file 2")
ap.add_argument("-o", "--output", type=str, default="combined", 
				help="output file")
args = vars(ap.parse_args())


content_x = readFile(args["input_x"])
content_y = readFile(args["input_y"])

with open(args["output"]+".txt", "w") as outfile:
	outText = ""
	for i in range(0, len(content_x)):
		outText += content_y[i] + " " + content_x[i] + "\n"
	outfile.write(outText)
