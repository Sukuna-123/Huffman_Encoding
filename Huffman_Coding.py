import heapq
import os

class BinaryTree:
    def __init__(self, value, frequ):
        self.value = value
        self.frequ = frequ
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequ < other.frequ

    def __eq__(self, other):
        return self.frequ == other.frequ


class HuffmanCode:

    def __init__(self, path):
        self.path = path
        self.__heap = []
        self.__code = {}
        self.__reversecode = {}

    def __frequency_from_text(self, text):
        frequ_dict = {}
        for char in text:
            frequ_dict[char] = frequ_dict.get(char, 0) + 1
        return frequ_dict

    def __build_heap(self, frequency_dict):
        for key, frequency in frequency_dict.items():
            heapq.heappush(self.__heap, BinaryTree(key, frequency))

    def __build_binary_tree(self):
        while len(self.__heap) > 1:
            node1 = heapq.heappop(self.__heap)
            node2 = heapq.heappop(self.__heap)
            merged = BinaryTree(None, node1.frequ + node2.frequ)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.__heap, merged)

    def __build_tree_code_helper(self, root, curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.__code[root.value] = curr_bits
            self.__reversecode[curr_bits] = root.value
            return
        self.__build_tree_code_helper(root.left, curr_bits + '0')
        self.__build_tree_code_helper(root.right, curr_bits + '1')

    def __build_tree_code(self):
        root = heapq.heappop(self.__heap)
        self.__build_tree_code_helper(root, '')

    def __build_encoded_text(self, text):
        return ''.join(self.__code[char] for char in text)

    def __build_padded_text(self, encoded_text):
        padding_value = 8 - (len(encoded_text) % 8)
        padded_info = f"{padding_value:08b}"
        return padded_info + encoded_text + ('0' * padding_value)

    def __build_byte_array(self, padded_text):
        return [int(padded_text[i:i+8], 2) for i in range(0, len(padded_text), 8)]

    def compression(self):
        filename, _ = os.path.splitext(self.path)
        output_path = filename + '.bin'

        with open(self.path, 'r', encoding='utf-8') as file, open(output_path, 'wb') as output:
            text = file.read().rstrip()
            frequency_dict = self.__frequency_from_text(text)
            self.__build_heap(frequency_dict)
            self.__build_binary_tree()
            self.__build_tree_code()

            encoded_text = self.__build_encoded_text(text)
            padded_text = self.__build_padded_text(encoded_text)
            bytes_array = self.__build_byte_array(padded_text)

            output.write(bytes(bytes_array))

        original_size = os.path.getsize(self.path)
        compressed_size = os.path.getsize(output_path)
        bytes_saved = original_size - compressed_size
        percent_saved = (bytes_saved / original_size) * 100 if original_size > 0 else 0

        print("\nCompression Complete")
        print(f"   • Original size   : {original_size:,} bytes")
        print(f"   • Compressed size : {compressed_size:,} bytes")
        print(f"   • Space saved     : {bytes_saved:,} bytes ({percent_saved:.2f}%)\n")

        return output_path

    def __remove_padding(self, text):
        padded_info = text[:8]
        extra_padding = int(padded_info, 2)
        return text[8:-extra_padding] if extra_padding > 0 else text[8:]

    def __decompress_text(self, text):
        decoded_text = ''
        current_bits = ''
        for bit in text:
            current_bits += bit
            if current_bits in self.__reversecode:
                decoded_text += self.__reversecode[current_bits]
                current_bits = ''
        return decoded_text

    def decompress(self, input_path):
        filename, _ = os.path.splitext(input_path)
        output_path = filename + '_decompressed.txt'

        with open(input_path, 'rb') as file, open(output_path, 'w', encoding='utf-8') as output:
            bit_string = ''.join(format(byte, '08b') for byte in file.read())
            actual_text = self.__remove_padding(bit_string)
            decompressed_text = self.__decompress_text(actual_text)
            output.write(decompressed_text)

        print(f"Decompressed successfully! Output written to: {output_path}\n")
        return output_path


# User Interaction
if __name__ == "__main__":
    path = input("Enter the path of your file: ").strip().strip('"')
    if not os.path.isfile(path):
        print("Invalid file path. Please check again.")
    else:
        huffman = HuffmanCode(path)
        compressed = huffman.compression()
        huffman.decompress(compressed)