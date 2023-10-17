import os
import re

def getText(name):
	list = os.listdir("data\Archive\\"+name)
	outfile = open("data\\"+name+"Text.txt","w")
	for item in list:
		with open("data\Archive\\"+name+"\\"+item) as infile:
			try:
				data = infile.read()
				match = re.search("\n\n",data)
				loc = match.start()
				print(repr(data[loc:]), file=outfile)
			except UnicodeDecodeError:
				pass
	outfile.close()

#getText("spam")
#getText("ham")


def makeTrain(fname, size):

	with open(fname) as infile:
		data = [msg.strip() for msg in infile]
	trainNum = int(len(data)*size)

	pre, ext = fname.split(".")
	with open (pre+"_train."+ext,"w") as outfile:
		for line in data[:trainNum]:
			print(line, file = outfile)
	with open(pre + "_test." + ext, "w") as outfile:
		for line in data[trainNum:]:
			print(line, file=outfile)

#makeTrain("data/hamText.txt",.85)
#makeTrain("data/spamText.txt",.85)

