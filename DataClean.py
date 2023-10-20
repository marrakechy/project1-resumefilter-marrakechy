import os
import re
from PyPDF2 import PdfReader


def getText(name):
	list = os.listdir("data\DSResume\\"+name)
	outfile = open("data\\"+name+"Text.txt","w")
	for item in list:
		with open("data\DSResume\\"+name+"\\"+item) as infile:
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

#makeTrain("newFiles/DSResumes.txt",.75)
#makeTrain("newFiles/OtherResumes.txt",.25)


#absolute paths to your directories
DSResumes_path = r"C:\Users\test1\PycharmProjects\project1-resumefilter-marrakechy\data\DSResume"
OtherResumes_path = r"C:\Users\test1\PycharmProjects\project1-resumefilter-marrakechy\data\OtherResumes"
UnknownResumes_path = r"C:\Users\test1\PycharmProjects\project1-resumefilter-marrakechy\data\UnknownResumes"


def extract_text_from_pdfs(path, output_file_name):
    # get list of pdfs in the specified directory
    pdf_list = [file for file in os.listdir(path) if file.lower().endswith('.pdf')]

    # create or overwrite the output text file
    with open(output_file_name, 'w', encoding='utf-8') as outfile:
        for pdf in pdf_list:
            pdf_path = os.path.join(path, pdf)
            full_text_for_pdf = []  # list to collect all text from a single PDF

            # extract text from the current pdf
            with open(pdf_path, 'rb') as pdf_file:
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:  # make sure that there's text before writing
                        full_text_for_pdf.append(extracted_text.replace('\n', ' '))

            # after reading all pages from a PDF, write its content in one line to the outfile
            outfile.write(' '.join(full_text_for_pdf) + '\n')

#extracting texts and writing
extract_text_from_pdfs(DSResumes_path, "data/DSResumes.txt")
extract_text_from_pdfs(OtherResumes_path, "data/OtherResumes.txt")
extract_text_from_pdfs(UnknownResumes_path, "data/UnknownResumes.txt")