from PIL import Image
import sys

def encode():

	f = open(str(sys.argv[2]),"r") # message to hide
	text = f.read()
	f.close()
	if len(text) == 0: # message without characters
		return 0
	# Value of every character of the hidden message in binary expressed in 8 bits + bits of control
	# Control bits are 0 if is not the last character, otherwise it is 1.
	binary = "" # string of hidden message in binary + control bits.
	for i in range(len(text)):
		binary = binary + bin(ord(text[i]))[2:].zfill(8)
		if i == len(text)-1:
			binary = binary + "1" # control bit set to 1 (last case)
		else:
			binary = binary + "0" # control bit set to 0
	image = Image.open(sys.argv[1]) # cover image
	pix = image.load()
	if image.mode == "RGB": #image has RGB pixels
		rgba = 0
	else:
		rgba = 1 # image has RGBA pixels
	width, height = image.size #size of the image
	count_letter = 0 # number of the letter of the message
	for i in range(0,width):
		for j in range(0,height):
			if rgba == 1:
				RGBA = image.getpixel((i,j)) #current pixel
				R,G,B,A = RGBA
			else:
				RGB = image.getpixel((i,j)) #current pixel
				R,G,B = RGB
			if bin(R)[2:].zfill(8)[7:] == "0": #lsb of the component is 0
				R = R | int(binary[count_letter])
			else:
				if int(binary[count_letter]) == 0: #the digit of the message is 0
					R = R & int(254)
				else:
					R = R & int(255)
			count_letter = count_letter + 1
			if bin(G)[2:].zfill(8)[7:] == "0":
				G = G | int(binary[count_letter])
			else:
				if int(binary[count_letter]) == 0:
					G = G & int(254)
				else:
					G = G & int(255)
			count_letter = count_letter + 1
			if bin(B)[2:].zfill(8)[7:] == "0":
				B = B | int(binary[count_letter])
			else:
				if int(binary[count_letter]) == 0:
					B = B & int(254)
				else:
					B = B & int(255)
			count_letter = count_letter + 1
			#now we set the current pixel with the new value
			if rgba == 1:
				pix[i,j] = eval("(" + str(R) + ", " + str(G) + ", " + str(B) + ", " + str(A) + ")") 
			else:
				pix[i,j] = eval("(" + str(R) + ", " + str(G) + ", " + str(B) + ")")
			if count_letter == len(binary): #we arrived to the end of the message
				break
		if count_letter == len(binary):
				break
	image.save('modified.png') #new image with the hidden message

def split(input, size): #splits a string in n digits
	return [input[start:start+size] for start in range(0, len(input), size)]
def decode():
	image = Image.open(sys.argv[2]) # image to decode the hidden message
	pix = image.load()
	width, height = image.size # size of the image
	pixel_count = 1 #every 3 pixels we check control bit
	string = "" #will be the result
	end = 0
	for i in range(0,width):
		if end == 1: #we finished (control bit = 1)
			break
		for j in range(0,height):
			if image.mode == "RGBA":
				RGBA = image.getpixel((i,j))
				R,G,B,A = RGBA
			else:
				RGB = image.getpixel((i,j))
				R,G,B = RGB
			string = string + str(bin(R)[2:].zfill(8)[7:]) #append the lsb of the component
			string = string + str(bin(G)[2:].zfill(8)[7:]) #append the lsb of the component
			if pixel_count < 3: # B doesn't have a control bit
				string = string + str(bin(B)[2:].zfill(8)[7:])
				pixel_count = pixel_count + 1
			else: # B has a control bit
				if str(bin(B)[2:].zfill(8)[7:]) == "1": # we finished the message
					end = 1
					break
				else: #we still have message to extract
					pixel_count = 1
	listing = split(string, 8)
	print ''.join(str(unichr(int(i,2))) for i in listing) # print the result with ASCII characters

if len(sys.argv) >= 2:
	if sys.argv[1] == "--h":
		if len(sys.argv) == 2:
			print "Usage: To encode a message: steganography.py [original image] [text file]"
			print "		Example: python steganography.py original-image.png message.txt"
			print "Usage: To decode the message: steganography.py --decode [modified image]"
			print "		Ejemplo: python steganography.py --decode modified.png"
		else:
			print "The input is not correct. Use the option --h to see the available options."
	elif sys.argv[1] != "--h" and sys.argv[1] != "--decode":
		if len(sys.argv) != 3:
			print "The input is not correct. Use the option --h to see the available options."
		else:
			if encode() != 0:
				print "Congratulations, the image modified.png was created with the hidden message."
			else:
				print "The text file is empty."
	elif sys.argv[1] == "--decode":
		if len(sys.argv) != 3:
			print "The input is not correct. Use the option --h to see the available options."
		else: 
			decode()
	else:
		print "The input is not correct. Use the option --h to see the available options."
else:
	print "The input is not correct. Use the option --h to see the available options."
