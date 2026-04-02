# Import necessary libraries
import tkinter as tk  # For creating the graphical user interface (GUI)
from tkinter import filedialog, simpledialog  # For file dialogs and simple input dialogs
from PIL import Image  # For handling images

# Define a Bloom Filter class to efficiently check for duplicate messages
class BloomFilter:
    def __init__(self, size):
        """
        Initialize the Bloom Filter with a specified size.
        The size determines the number of bits in the bit array.
        """
        self.size = size  # Size of the Bloom Filter
        self.bit_array = [False] * size  # Initialize the bit array with all False values

    def add(self, item):
        """
        Add an item to the Bloom Filter.
        This involves hashing the item and setting the corresponding bit in the bit array to True.
        """
        index = hash(item) % self.size  # Calculate the index using a hash function
        self.bit_array[index] = True  # Set the bit at the calculated index to True

    def lookup(self, item):
        """
        Check if an item is possibly present in the Bloom Filter.
        Returns True if the bit at the calculated index is True, indicating the item might be present.
        """
        index = hash(item) % self.size  # Calculate the index using a hash function
        return self.bit_array[index]  # Return the value of the bit at the calculated index

# Define a Trie (Prefix Tree) class to store and manage encoded messages efficiently
class TrieNode:
    def __init__(self):
        """
        Initialize a node in the Trie.
        Each node contains a dictionary to store child nodes and a flag to mark the end of a word.
        """
        self.children = {}  # Dictionary to store child nodes
        self.end_of_word = False  # Flag to mark the end of a word

class Trie:
    def __init__(self):
        """
        Initialize the Trie with a root node.
        """
        self.root = TrieNode()  # Create the root node

    def insert(self, word):
        """
        Insert a word into the Trie.
        Traverse the Trie based on the characters of the word, creating new nodes if necessary.
        """
        node = self.root  # Start at the root node
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()  # Create a new node if the character is not present
            node = node.children[char]  # Move to the child node
        node.end_of_word = True  # Mark the end of the word

    def search(self, word):
        """
        Search for a word in the Trie.
        Traverse the Trie based on the characters of the word and return True if the word is found.
        """
        node = self.root  # Start at the root node
        for char in word:
            if char not in node.children:
                return False  # Return False if the character is not found
            node = node.children[char]  # Move to the child node
        return node.end_of_word  # Return True if the word is marked as complete

# Initialize the Bloom Filter and Trie globally for use throughout the project
bloom_filter = BloomFilter(1000)  # Create a Bloom Filter with a size of 1000
trie = Trie()  # Create a Trie instance

# Function to encode a secret message into an image using LSB steganography
def encode_image(image_path, secret_message, output_path):
    """
    Encode a secret message into an image.
    Uses the Least Significant Bit (LSB) method for steganography.
    """
    try:
        # Check if the message has already been encoded using the Bloom Filter
        if bloom_filter.lookup(secret_message):
            print("Message already encoded.")  # Prevent duplicate encoding
            return

        # Add the message to the Bloom Filter and Trie
        bloom_filter.add(secret_message)  # Add to Bloom Filter
        trie.insert(secret_message)  # Insert into Trie

        # Open the image using Pillow
        img = Image.open(image_path)
        pixels = list(img.getdata())  # Get pixel data from the image

        # Convert the secret message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
        binary_message += '11111111'  # Add an end marker to the binary message

        # Modify pixel values to encode the message using LSB steganography
        encoded_pixels = []
        message_index = 0
        for pixel in pixels:
            new_pixel = list(pixel)
            for i in range(3):  # Modify RGB channels
                if message_index < len(binary_message):
                    new_pixel[i] = (new_pixel[i] & ~1) | int(binary_message[message_index])
                    message_index += 1
            encoded_pixels.append(tuple(new_pixel))

        # Create and save the encoded image
        img.putdata(encoded_pixels)
        img.save(output_path)
        print(f"Encoded image saved as {output_path}")
    except Exception as e:
        print(f"Encoding failed: {str(e)}")

# Function to decode a hidden message from an encoded image
def decode_image(image_path):
    """
    Decode a hidden message from an encoded image.
    Uses the Least Significant Bit (LSB) method for steganography.
    """
    try:
        # Open the encoded image using Pillow
        img = Image.open(image_path)
        pixels = list(img.getdata())  # Get pixel data from the image

        # Extract binary data from pixel values using LSB steganography
        binary_message = ''
        for pixel in pixels:
            for i in range(3):  # Extract from RGB channels
                binary_message += str(pixel[i] & 1)

                # Check for the end marker
                if binary_message.endswith('11111111'):
                    binary_message = binary_message[:-8]  # Remove the end marker
                    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
                    
                    # Validate the decoded message against the Trie
                    if trie.search(decoded_message):
                        print(f"Hidden Message: {decoded_message}")
                        return
                    
                    print("Decoded message not found in Trie.")
                    return

        print("No hidden message detected.")
    except Exception as e:
        print(f"Decoding failed: {str(e)}")

# Main function to create the GUI and handle user interactions
def main():
    root = tk.Tk()
    root.title("Steganography Tool")

    # Function to handle the encoding button click
    def encode():
        image_path = filedialog.askopenfilename(title="Select Image to Encode")
        if not image_path:
            return

        secret_message = simpledialog.askstring("Input Secret Message", "Enter the secret message:")
        if not secret_message:
            return

        output_path = filedialog.asksaveasfilename(title="Save Encoded Image", defaultextension=".png")
        if not output_path:
            return

        encode_image(image_path, secret_message, output_path)

    # Function to handle the decoding button click
    def decode():
        image_path = filedialog.askopenfilename(title="Select Encoded Image to Decode")
        if not image_path:
            return

        decode_image(image_path)

    # Create buttons for encoding and decoding
    tk.Button(root, text="Encode Image", command=encode).pack()
    tk.Button(root, text="Decode Image", command=decode).pack()

    # Start the GUI event loop
    root.mainloop()

# Run the main function to start the application
if __name__ == "__main__":
    main()
