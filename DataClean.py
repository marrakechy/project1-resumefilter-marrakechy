
import os
import re
import PyPDF2


def extract_text_from_pdf(folder_name):
    texts = []
    list_of_files = os.listdir(folder_name)
    for item in list_of_files:
        file_path = os.path.join(folder_name, item)
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in range(reader.numPages):
                text += reader.getPage(page).extractText()
            texts.append(text)
    return texts


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

