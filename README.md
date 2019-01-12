# Steganography-PNG
Steganography script in images PNG

It is a Python2.7 script that permits to encode or decode a message into/from PNG images. Doesn't matter if it uses RGB or RGBA to set the pixels. It works in both. 
It uses the LSB-replacement algorithm.

It is necessary the following libraries to execute the script:

- Image from PIL
- sys

<b><h2>IMPORTANT!!!</h2></b>
- The message needs to contain only ASCII characters.
- The message is not encrypted, it is inserted into the pixels in plain text.

To execute it, it is just necessary these steps:

<b><h3>To see the options:</h3></b>

    python steganography.py --h


<b><h3>To encode:</h3></b>

    python steganography.py [original_image.png] [text_file.txt]
Where [original_image.png] is the image that you choose to encode the message, and [text_file.txt] is the text to hide.
It will create the 'modified.png' in the same directory.

<b><h3>To  decode:</h3></b>

    python steganography.py --decode modified.png

Where modified.png is the image with the hidden message. It will prompt the hidden message in the console.
