import os
import re
from PyPDF2 import PdfReader

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



#absolute paths to your directories
DSResumes_path = r"C:\Users\test1\PycharmProjects\project1-resumefilter-marrakechy\data\DSResume"
OtherResumes_path = r"C:\Users\test1\PycharmProjects\project1-resumefilter-marrakechy\data\OtherResumes"
UnknownResumes_path = r"C:\Users\test1\PycharmProjects\project1-resumefilter-marrakechy\data\UnknownResumes"


def extract_text_from_pdfs(path, output_file_name):
	# Get list of PDFs in the specified directory
	pdf_list = [file for file in os.listdir(path) if file.lower().endswith('.pdf')]

	# Create or overwrite the output text file
	with open(output_file_name, 'w', encoding='utf-8') as outfile:
		for pdf in pdf_list:
			pdf_path = os.path.join(path, pdf)

			# Extract text from the current PDF
			with open(pdf_path, 'rb') as pdf_file:
				reader = PdfReader(pdf_file)
				for page in reader.pages:
					extracted_text = page.extract_text()
					if extracted_text:  # Ensure there's text before writing
						outfile.write(extracted_text)


# Extracting texts and writing to respective files
extract_text_from_pdfs(DSResumes_path, "DSResumes.txt")
extract_text_from_pdfs(OtherResumes_path, "OtherResumes.txt")
extract_text_from_pdfs(UnknownResumes_path, "UnknownResumes.txt")


