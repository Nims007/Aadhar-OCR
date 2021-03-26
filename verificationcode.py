#Libraries to import
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import cv2 
import numpy as np
from matplotlib import pyplot as plt
from fuzzywuzzy import fuzz
import re
import difflib
import csv
import nltk
import os
import os.path
import json
import sys
import string
import PIL




#Fetching files from db
try:
	filename1  = "img.pdf"
	filename2 = "img2.jpeg"
except:
	print("Error Code - fileloadingdb-sql \nAn error occured, please inform us by contacting us via email at email@cogenteservices.com or via phone at +91-120-4832550 and provide the error code")



#Coverting pdf to img if necessary
try:
	if filename1.endswith('.pdf') and filename2.endswith('.pdf'):
	#frontside
		pages1 = convert_from_path(filename1, 500)  #converting pdf to img
		for page in pages1:
			page.save('out1.jpg', 'JPEG')
		img1reso = PIL.Image.open('D:/dataset/out1.jpg')#if pdf converted
		w1, h1 = img1reso.size
		img1reso = img1reso.save('output1.jpeg')

	#back side
		pages2 = convert_from_path(filename2, 500)  #converting pdf to img
		for page in pages2:
			page.save('out2.jpg', 'JPEG')
		img2reso = PIL.Image.open('D:/dataset/out2.jpg')#if pdf converted
		w2, h2 = img2reso.size
		img2reso = img2reso.save('output2.jpeg')



	elif filename1.endswith('.pdf'):
		pages1 = convert_from_path(filename1, 500)  #converting pdf to img
		for page in pages1:
			page.save('out1.jpg', 'JPEG')
		img1reso = PIL.Image.open('D:/dataset/out1.jpg')#if pdf converted
		w1, h1 = img1reso.size
		img1reso = img1reso.save('output1.jpeg')

		img2reso = PIL.Image.open(str(filename2))
		w2, h2 = img2reso.size
		img2reso = img2reso.save('output2.jpeg')



	elif filename2.endswith('.pdf'):
		img1reso = PIL.Image.open(str(filename1))
		w1, h1 = img1reso.size
		img1reso = img1reso.save('output1.jpeg')

		pages2 = convert_from_path(filename2, 500)  #converting pdf to img
		for page in pages2:
			page.save('out2.jpg', 'JPEG')
		img2reso = PIL.Image.open('D:/dataset/out2.jpg')#if pdf converted
		w2, h2 = img2reso.size
		img2reso = img2reso.save('output2.jpeg')



	else:
		img1reso = PIL.Image.open(str(filename1))
		w1, h1 = img1reso.size
		img1reso = img1reso.save('output1.jpeg')

		img2reso = PIL.Image.open(str(filename2))
		w2, h2 = img2reso.size
		img2reso = img2reso.save('output2.jpeg')

except:
	print("Error Code - fileverifying-PIL \nAn error occured, please contact us via email at email@cogenteservices.com or via phone at +91-120-4832550 and provide the error code")



pytesseract.pytesseract.tesseract_cmd = 'D:/Tessertact-OCR/tesseract.exe' #guiding to Tesseract path




#Verification code
try:
	
	print(w1,h1,w2,h2)


	if w1 > 1000 and h1 > 600 and w2 > 1000 and h2 > 600:
		#Aadhar front side
		if filename1.endswith('.pdf'):
			img1 = cv2.imread('output1.jpeg', cv2.IMREAD_GRAYSCALE) #if using with pdf conv
		else:
			img1 = cv2.imread('output1.jpeg', cv2.IMREAD_GRAYSCALE) #if using without pdf conv


		sobelX1 = cv2.Sobel(img1, cv2.CV_64F, 1, 0, ksize = 1)
		sobelY1 = cv2.Sobel(img1, cv2.CV_64F, 0, 1, ksize = 1)

		sobelX1 = np.uint8(np.absolute(sobelX1))
		sobelY1 = np.uint8(np.absolute(sobelY1))

		sobelCombined1 = cv2.bitwise_or(sobelX1, sobelY1)

		if filename1.endswith('.pdf'):
			blurred1 = cv2.blur(img1, (3,3)) #for pdf->img
		else:
			blurred1 = cv2.blur(sobelCombined1, (4,3)) #for direct img input

		canny1 = cv2.Canny(blurred1, 5, 250)

		pts1 =np.argwhere(canny1>0)
		y11,x11 = pts1.min(axis=0)
		y21,x21 = pts1.max(axis=0)

		cropped1 = img1[y11:y21, x11:x21]
		#cv2.imwrite("cropped.png", cropped)

		resizedimage1 = cv2.resize(cropped1, (1080, 720), interpolation=cv2.INTER_CUBIC) #actual 


		cv2.imwrite("resizedimage1.jpeg", resizedimage1)


		im1 = Image.open('resizedimage1.jpeg')
		box1 = (250, 150, 1200, 430) #actual

		croppedimg1 = im1.crop(box1)
		croppedimg1.save('croppedimg1.jpeg')


		#Aadhar back side

		if filename2.endswith('.pdf'):
			img2 = cv2.imread('output2.jpeg', cv2.IMREAD_GRAYSCALE)#if using with pdf conv
		else:
			img2 = cv2.imread('output2.jpeg', cv2.IMREAD_GRAYSCALE) #if using without pdf conv

		sobelX2 = cv2.Sobel(img2, cv2.CV_64F, 1, 0, ksize = 1)
		sobelY2 = cv2.Sobel(img2, cv2.CV_64F, 0, 1, ksize = 1)

		sobelX2 = np.uint8(np.absolute(sobelX2))
		sobelY2 = np.uint8(np.absolute(sobelY2))

		sobelCombined2 = cv2.bitwise_or(sobelX2, sobelY2)

		if filename2.endswith('.pdf'):
			blurred2 = cv2.blur(img2, (3,3)) #for pdf->img
		else:
			blurred2 = cv2.blur(sobelCombined2, (4,3)) #for direct img input


		canny2 = cv2.Canny(blurred2, 5, 250)

		pts2 =np.argwhere(canny2>0)
		y12,x12 = pts2.min(axis=0)
		y22,x22 = pts2.max(axis=0)

		cropped2 = img2[y12:y22, x12:x22]
		#cv2.imwrite("cropped.png", cropped)
	
		resizedimage2 = cv2.resize(cropped2, (1080, 720), interpolation=cv2.INTER_CUBIC) #actual 


		cv2.imwrite("resizedimage2.jpeg", resizedimage2)


		im2 = Image.open('resizedimage2.jpeg')
		box2 = (450, 150, 1200, 500) #actual

		croppedimg2 = im2.crop(box2)
		croppedimg2.save('croppedimg2.jpeg')


		#Extracting text

		#Front side
	
		text1 = pytesseract.image_to_string(croppedimg1)
		f1 = open('output1.txt', 'w', encoding="utf-8")
		print(text1.lower(), file = f1)
		print('end', file = f1)
		f1.close()

		fi1 = open('output1.txt', 'r', encoding = 'utf-8')
		text1 = fi1.read().replace("'", "").replace("`", "").replace(" ","").replace("‘", "").replace("_", "-").replace("”","").replace(";", "").replace('"','').replace("fdob", "dob").replace("|", "").replace("{","").replace("}","").replace("[","").replace("]","").replace(":","").replace("@","").replace("#","").replace("$","").replace(":","").replace("^","").replace("&","").replace("*","").replace("|", "").replace("(", "").replace(")", "")
		#print(text)
		lines1 = text1.split('\n')
		#print(lines1)




		#Back side

		text2 = pytesseract.image_to_string(croppedimg2)

		f2 = open('output2.txt', 'w', encoding="utf-8")
		print(text2.lower(), file = f2)
		print('end', file = f2)
		f2.close()


		sep = ","
		fi2 = open('output2.txt', 'r', encoding = 'utf-8')
		text2=fi2.read().replace("5", "").replace("-", "").replace("|", "").replace("0", "").replace("1", "").replace("'", "").replace(" ", "").replace("s/o", "").replace("2","").replace("3","").replace("4","").replace("6","").replace("7","").replace("8","").replace("9","").split(sep, 1)[0].replace("/","").replace(":","").replace("{","").replace("}","").replace("[","").replace("]","").replace(":","").replace("@","").replace("#","").replace("$","").replace(":","").replace("‘", "").replace("_", "-").replace("”","").replace(";", "").replace('"','').replace("(", "").replace(")", "")
		#text2 = fi2.read()
		#print(text)
		lines2 = text2.split('\n')
		#print(lines2)



		#Name and dob verifying from front side


		s = 'Name'
		#t = s.lower()
		name = list(s.lower())
		dob = 'XX-XX-XXXX'
		DOB = 'dob' + dob
		#print(DOB)
	
		#t = len(k)


		c = difflib.get_close_matches(name, lines1, 1, 0.95)
		#print(c)

		finalname = ''.join(c)
		print("Name: " +finalname)

		d = difflib.get_close_matches(DOB, lines1, 1, 0.95)
		#print(d)
		finaldob = ''.join(d)
		print(finaldob)


		rationame = fuzz.ratio(s.lower(), finalname.lower())
		ratiodob = fuzz.ratio(DOB, d)




		#fathers name verifying from back side


		x = 'Father Name'
		fname = list(x.lower())


		j = difflib.get_close_matches(fname, lines2, 1, 0.90)
		#print(j)

		finalfname = ''.join(j)
		print("Father's Name: " +finalfname)

		ratiofname = fuzz.ratio(x.lower(), finalfname.lower())




		if rationame > 0.95 and ratiodob > 0.8 and ratiofname > 0.8:
			print('aadhar verified')
			#initiating csv file and writing to csv
			csv_columns = ['Name', 'year of birth', "Father's name"]
			specs = {}
			specs['name'] = s
			specs['dob'] = dob
			specs['Father name'] = x
			l = [specs]

			print(specs)


			def write_csv(data):
				with open('test.csv', 'a') as file:
					writer = csv.writer(file)
					writer.writerow([data['name'], data['dob'], data['Father name']])


			write_csv(specs)

		else:
			print("Please reupload")


		#cleaning up

		#os.remove('out.jpg')
		os.remove('resizedimage1.jpeg')
		os.remove('resizedimage2.jpeg')
		#os.remove('croppedimg1.jpeg')
		os.remove('croppedimg2.jpeg')
		os.remove('output1.jpeg')
		os.remove('output2.jpeg')
		if os.path.exists('out1.jpg'):
			os.remove("out1.jpg")

		else: 
			pass


		if os.path.exists('out2.jpg'):
			os.remove("out2.jpg")

		else:
			pass


		
		fi1.close()
		fi2.close()
		#os.remove('output1.txt')
		os.remove('output2.txt')
	else: 
		print("Please make sure image image resolution is greater than or equal to 1000x600")


except:
	print("Error Code - verifying-tess \nAn unexpected error occured, please contact us via email at email@cogenteservices.com or via phone at +91-120-4832550 and provide the error code")




