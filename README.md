StegoShield is a desktop steganography tool that lets you hide secret messages inside images and retrieve them later. It uses the Least Significant Bit (LSB) technique to embed text into image pixels in a way that is invisible to the naked eye.
What it does
You can load any image, type in a secret message, and save a new version of that image with the message hidden inside it. Later, you or anyone else with the tool can open that image and extract the hidden message from it.
How it works
The message is converted to binary and embedded into the least significant bits of the RGB pixel values in the image. This causes no visible change to the image. A special end marker is used so the decoder knows when to stop reading.
The tool also uses two data structures internally: a Bloom Filter to avoid encoding the same message twice, and a Trie to validate messages during decoding. These are mostly there to make the logic more robust and to demonstrate their practical use.
Requirements

Python 3.x
Pillow (pip install pillow)
Tkinter (comes bundled with most Python installations)

python stegoShield.py
```

A simple window will open with two buttons: one to encode and one to decode.

- **Encode Image** - Pick an image, enter your message, and save the output image.
- **Decode Image** - Pick an encoded image and the hidden message will be printed to the console.

## Notes

- Use PNG format for best results. JPEG compression can corrupt the hidden data.
- The image needs to be large enough to hold the message. A small 100x100 image can hold roughly 3750 characters.
- The Bloom Filter check is session-based, so it resets each time you restart the app.

## Project structure
```
stegoShield.py   # Main file containing all logic and the GUI
