import heapq
import os
from logger.logger import Logger
from Cipher.Cipher import Cipher


class HeapNode:
    __log_obj = Logger("logs\\Log.log")

    def __init__(self, ascii_value, freq):
        self.ascii_value = ascii_value
        self.freq = freq
        self.left = None  # stores the left child's reference
        self.right = None  # stores the right child's reference
        HeapNode.__log_obj.add_log("Heap Node initialized")

    # Functions that help us build the min heap
    def __lt__(self, other):
        """overloading the less than operator"""
        return self.freq < other.freq

    def __eq__(self, other):
        """overloads the equal to operator"""
        if other is None:
            return False
        if not isinstance(other, HeapNode):  # Safeguarding ourselves if other is not a HeapNode
            return False
        return self.freq == other.freq


class HuffmanCoding:
    __log_obj = Logger("logs//Log.log")

    def __init__(self, path):
        self.path = path
        self.heap = []  # min heap
        self.codes = {}  # mappings between ASCII code and Huffman Codes
        self.reverse_mapping = {}  # mappings b/w Huffman Code and ASCII code
        self.filename, self.file_format = os.path.splitext(self.path)

    def make_freq_dict(self, byte_array_data):
        """method to build ASCII value and frequency mappings"""
        try:
            frequency = {}  # dictionary storing ASCII code and frequencies

            for index, item in enumerate(byte_array_data):
                if item not in frequency:
                    frequency[item] = 1
                else:
                    frequency[item] += 1
            HuffmanCoding.__log_obj.add_log("frequency dictionary built")
            return frequency

        except Exception as e:
            HuffmanCoding.__log_obj.add_log("Problem in make_freq_dict function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def make_heap(self, frequency):
        """build the min heap, which helps us in creating the Huffman Tree"""
        try:
            for ascii_value in frequency:
                node = HeapNode(ascii_value, frequency[ascii_value])  # Creating node of Heap Node
                heapq.heappush(self.heap, node)
            HuffmanCoding.__log_obj.add_log("make_heap function successful")


        except Exception as e:
            HuffmanCoding.__log_obj.add_log("problem in make_heap function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def merge_codes(self):
        """creates the Huffman Tree. Also save the root in heap"""
        try:
            while len(self.heap) > 1:
                node1 = heapq.heappop(self.heap)  # get the top most node
                node2 = heapq.heappop(self.heap)  # get the top most node

                newNode = HeapNode(None, node1.freq + node2.freq)  # create a new node with frequencies of the
                # two nodes

                # newNode becomes the parent of node1 and node2
                newNode.left = node1
                newNode.right = node2

                # push newNode back into the heap

                heapq.heappush(self.heap, newNode)
            HuffmanCoding.__log_obj.add_log("merge codes function successful")



        except Exception as e:
            HuffmanCoding.__log_obj.add_log("problem in merge codes function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def make_codes_helper(self, node, current_code):
        """helper function to build huffman tree codes"""
        try:
            if node is None:  # reached the leaf node
                return

            if node.ascii_value is not None:  # code can be built for this ASCII Value
                self.codes[node.ascii_value] = current_code
                self.reverse_mapping[current_code] = node.ascii_value

            # recursive call
            self.make_codes_helper(node.left, current_code + "0")  # call on the left child
            self.make_codes_helper(node.right, current_code + "1")  # call on the right child

        except Exception as e:
            HuffmanCoding.__log_obj.add_log(str(e))

    def make_codes(self):
        """function to make codes from the Huffman Tree. We will make this recursive."""
        try:
            root = heapq.heappop(self.heap)
            current_code = ""
            self.make_codes_helper(root, current_code)

            HuffmanCoding.__log_obj.add_log("make_codes function successful")


        except Exception as e:
            HuffmanCoding.__log_obj.add_log("Problem in make_codes function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def get_encoded_text(self, byte_array_data):
        """function to encode the ASCII code to the Huffman Codes"""
        try:
            encoded_text = ""

            for index, item in enumerate(byte_array_data):
                encoded_text += self.codes[item]

            HuffmanCoding.__log_obj.add_log("get_encoded text function successful")
            return encoded_text

        except Exception as e:
            HuffmanCoding.__log_obj.add_log("Problem in get_encoded_text function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def pad_encoded_text(self, encoded_text):
        """function to pad the encoded_text so that encoded text is multiple of 8 as 1 bute = 8 bits"""
        try:
            extra_padding = 8 - (len(encoded_text) % 8)

            for i in range(extra_padding):
                encoded_text += "0"

            padded_info = "{0:08b}".format(extra_padding)
            encoded_text = padded_info + encoded_text
            HuffmanCoding.__log_obj.add_log("pad encoded function successful")
            return encoded_text
        except Exception as e:
            HuffmanCoding.__log_obj.add_log("problem in pad encoded function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def get_byte_array(self, padded_encoded_text):
        """converts bits to bytes"""
        try:
            b = bytearray()
            for i in range(0, len(padded_encoded_text), 8):
                byte = padded_encoded_text[i:i + 8]
                b.append(int(byte, 2))  # by default base is 10, we want 2 to be the base
            HuffmanCoding.__log_obj.add_log("get byte array function successful")
            return b
        except Exception as e:
            HuffmanCoding.__log_obj.add_log("problem in get_byte_array")
            HuffmanCoding.__log_obj.add_log(str(e))

    def encrypt(self, byte_array_data, key):
        try:

            cip = Cipher()

            cip.encrypt_file(byte_array_data, key)

            HuffmanCoding.__log_obj.add_log("encrypt function successful")
            return byte_array_data

        except Exception as e:
            HuffmanCoding.__log_obj.add_log("problem in encrypt function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def compress(self, output_path, key):
        """function to compress the file"""
        try:
            output_path += ".bin"

            with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
                text = file.read()  # reading the byte data
                text = text.strip()

                byte_array_data = bytearray(text)  # making byte array

                frequency = self.make_freq_dict(byte_array_data)  # creating mappings b/w ASCII codes and their
                # frequencies

                self.make_heap(frequency)  # creating the min heap
                self.merge_codes()  # creating huffman tree
                self.make_codes()  # creating code for each ASCII code

                encoded_text = self.get_encoded_text(byte_array_data)

                padded_encoded_text = self.pad_encoded_text(encoded_text)

                b = self.get_byte_array(padded_encoded_text)

                encrypted_data = self.encrypt(b, key)

                output.write(b)
            HuffmanCoding.__log_obj.add_log("Compress function successful")


        except Exception as e:
            HuffmanCoding.__log_obj.add_log("Problem in Compress function")
            HuffmanCoding.__log_obj.add_log(str(e))

    """decompression functions"""

    def remove_padding(self, bit_string):
        """function that removes the padding bits from bit string"""
        try:
            padded_info = bit_string[:8]  # padding bits are added in the first 8 bits

            extra_padding = int(padded_info, 2)  # getting the extra_padding in the form of integer. binary to int
            # conversion done hence base 2

            bit_string = bit_string[8:]  # removing the first 8 bits that store the padded bits
            encoded_text = bit_string[:-1 * extra_padding]  # removing the padded bits

            return encoded_text

        except Exception as e:
            HuffmanCoding.__log_obj.add_log("problem in remove padding function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def decode_text(self, encoded_text):
        """function that converts the Huffman codes to ASCII codes"""
        try:
            current_code = ""

            decoded_byte_data = bytearray()

            for bit in encoded_text:
                current_code += bit

                if current_code in self.reverse_mapping:  # iterate till we get some valid code
                    ascii_code = self.reverse_mapping[current_code]  # recover ASCII code from this Huffman code
                    decoded_byte_data.append(ascii_code)
                    current_code = ""  # reset the current code

            return decoded_byte_data
        except Exception as e:
            HuffmanCoding.__log_obj.add_log("Problem in Decode Text function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def decrypt(self, byte_array_data, key):
        try:
            cip = Cipher()
            cip.decrypt_file(byte_array_data, key)
            return byte_array_data
        except Exception as e:
            HuffmanCoding.__log_obj.add_log("Problem in decrypt function")
            HuffmanCoding.__log_obj.add_log(str(e))

    def decompress(self, input_path, output_path, key):
        """function that decompresses the file"""
        try:


            output_path += self.file_format

            with open(input_path, 'rb') as file, open(output_path, 'wb') as output:
                bit_string = ""

                # decrypting
                x = file.read()

                y = bytearray(x)

                decrypt_file = self.decrypt(y, key)

                if os.path.exists("temp.bin"):
                    os.remove("temp.bin")
                f = open("temp.bin", 'wb')
                f.write(decrypt_file)
                f.close()

                # getting file back from Huffman Tree
                file = open("temp.bin", 'rb')

                byte = file.read(1)

                while len(byte) > 0:
                    byte = ord(byte)
                    bits = bin(byte)[2:].rjust(8, '0')
                    bit_string += bits
                    byte = file.read(1)

                file.close()

                encoded_text = self.remove_padding(bit_string)

                decoded_byte_data = self.decode_text(encoded_text)

                output.write(decoded_byte_data)




        except Exception as e:
            HuffmanCoding.__log_obj.add_log("Problem in decompress function")
            HuffmanCoding.__log_obj.add_log(str(e))
