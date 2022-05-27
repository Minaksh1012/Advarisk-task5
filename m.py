# from PIL import Image
  
# # open method used to open different extension image file
# im = Image.open(r"/home/minakshi/Desktop/Advarisk Task5/TamilNadu/TamilNadu/c.jpeg") 
  
# # This method will show image in any image viewer 
# im.show() 



# import PyPDF2
# #open the PDF file
# PDFfile = open("/home/minakshi/Desktop/Advarisk Task5/TamilNadu/TamilNadu/a.pdf", 'rb')

# PDFfilereader = PyPDF2.PdfFileReader(PDFfile)
# import pdb;pdb.set_trace()
#print the number of pages
# print(PDFfilereader.numPages)

#provide the page number
# pages = PDFfilereader.getPage(0)

#extracting the text in PDF file
# print(pages.extractText())

#close the PDF file
# PDFfile.close()


# import pdfplumber
# with pdfplumber.open(r'ac029036.pdf') as pdf:
#     first_page = pdf.pages[24]
#     print(first_page.extract_text())


# import PyPDF2

# with open("/home/minakshi/Desktop/Advarisk Task5/TamilNadu/TamilNadu/a.pdf", "rb") as pdf_file:
#     read_pdf = PyPDF2.PdfFileReader(pdf_file)
#     number_of_pages = read_pdf.getNumPages()
#     page = read_pdf.pages[0]
#     page_content = page.extract_text()
# print(page_content)



# import fitz # install using: pip install PyMuPDF

# with fitz.open("/home/minakshi/Desktop/Advarisk Task5/TamilNadu/TamilNadu/a.pdf") as doc:
#     text = ""
#     for page in doc:
#         text += page.get_text()

# print(text)





# from PyPDF2 import PdfFileReader,PdfFileWriter
# import pdb;pdb.set_trace()
# file_path="/home/minakshi/Desktop/Advarisk Task5/TamilNadu/TamilNadu/a.pdf"
# pdf=PdfFileReader(file_path)
# with open("tamil.csv","w") as f:
#     for page_no in range(pdf.numPages):
#         page_obj=pdf.getPage(page_no)
#         try:
#             txt=page_obj.extract_text()
#             print("".center(100,"-"))
#         except:
#             pass  
#         else:

#             f.write("page{0}\n".format(page_no+1))
#             f.write(''.center(100,"-")) 
#             f.write(txt)
    # f.close()       
 
#     # Import libraries
# from PIL import Image
# import pytesseract
# import sys
# from pdf2image import convert_from_path
# import os
# import re

# # Path of the pdf
# PDF_file = "/home/minakshi/Desktop/Advarisk Task5/TamilNadu/TamilNadu/a.pdf"

# '''
# Part #1 : Converting PDF to images
# '''
# # import pdb;pdb.set_trace()
# # Store all the pages of the PDF in a variable
# pages = convert_from_path(PDF_file, 150)

# # Counter to store images of each page of PDF to image
# image_counter = 1

# # Iterate through all the pages stored above
# for page in pages:
# # for i, page in enumerate(pages):
# # 	page.save('img/page_{}'.format(i), 'JPEG')
# # 	print(im																	age_to_string(Image.open('img/page_{}'.format(i))))

# 	# Declaring filename for each page of PDF as JPG
# 	# For each page, filename will be:
# 	# PDF page 1 -> page_1.jpg
# 	# PDF page 2 -> page_2.jpg
# 	# PDF page 3 -> page_3.jpg
# 	# ....
# 	# PDF page n -> page_n.jpg
# 	filename = "page_"+str(image_counter)+".jpg"
		
# 		# Save the image of the page in system
# 	page.save(filename, 'JPEG')

# 		# Increment the counter to update filename
# 	image_counter = image_counter + 1

# '''
# Part #2 - Recognizing text from the images using OCR
# '''
# # Variable to get count of total number of pages
# filelimit = image_counter-1

# # Creating a text file to write the output
# outfile = "out_text.txt"
# # import pdb;pdb.set_trace()
# # Open the file in append mode so that
# # All contents of all images are added to the same file
# f = open(outfile, "a")

# # Iterate from 1 to total number of pages
# for i in range(1, 100):

# 	# Set filename to recognize text from
# 	# Again, these files will be:
# 	# page_1.jpg
# 	# page_2.jpg
# 	# ....
# 	# page_n.jpg
# 	filename = "page_"+str(i)+".jpg"
# 	# EPIC=[]
# 	# Recognize the text as string in image using pytesserct
# 	text = str(((pytesseract.image_to_string(Image.open(filename)))))
# 	EPIC_NO = re.findall("[A-Z]{3}[0-9]{7}",text)
# 	# EPIC.append(EPIC_NO)
# 	print(EPIC_NO)

# 	# The recognized text is stored in variable text
# 	# Any string processing may be applied on text
# 	# Here, basic formatting has been done:
# 	# In many PDFs, at line ending, if a word can't
# 	# be written fully, a 'hyphen' is added.
# 	# The rest of the word is written in the next line
# 	# Eg: This is a sample text this word here GeeksF-
# 	# orGeeks is half on first line, remaining on next.
# 	# To remove this, we replace every '-\n' to ''.
# 	text = text.replace('-\n', '')	

# 	# Finally, write the processed text to the file.
# 	f.write(text)

# # Close the file after writing all the text.
# # f.close()
     