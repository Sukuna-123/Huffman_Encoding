# Huffman Coding Compressor/Decompressor

## Project Overview

This project provides a command-line tool written in Python for lossless file compression and decompression using the Huffman coding algorithm. By analyzing character frequencies in a text file, it builds an optimal prefix tree to encode data with variable-length bitstrings, reducing overall file size.

## Introduction

Huffman coding is a fundamental algorithm in data compression. It assigns shorter codes to more frequent symbols and longer codes to less frequent symbols, ensuring a prefix-free code that can be uniquely decoded. This implementation reads plain-text files, generates a binary `.bin` output, and restores the original text without any loss of information.

## Installation

No external dependencies are required beyond the Python standard library. Ensure you have Python 3.7 or later installed.

```bash
# Clone the repository
git clone https://github.com/Sukuna-123/huffman-compressor.git
cd huffman-compressor
```

## Usage

To compress and decompress a file, run:

```bash
python huffman.py
# When prompted, enter the path to your text file, for example: data/input.txt
```

### Example Output

```
Compression Complete
   • Original size   : 9,024 bytes
   • Compressed size : 3,818 bytes
   • Space saved     : 5,206 bytes (57.69%)

Decompressed successfully! Output written to: input_decompressed.txt
```

## How It Works

1. **Frequency Analysis**: Reads the input file and counts how often each character appears.
2. **Tree Construction**: Creates a min-heap of nodes, merging the two least-frequent nodes until a single Huffman tree remains.
3. **Code Generation**: Traverses the tree to assign binary codes (`0` for left, `1` for right) to each character.
4. **Encoding & Padding**: Converts the original text into a bitstring of codes, prepends an 8-bit header indicating padding length, and pads with zeros to align to bytes.
5. **Byte Writing**: Splits the padded bitstring into bytes and writes them to a `.bin` file.
6. **Decompression**: Reverses the process by reading bytes, removing padding, and decoding bit sequences back into the original text.

## Results

In testing with standard English text, this implementation consistently achieves between 50% and 70% reduction in file size. The example above demonstrates a **57.69%** space savings on a 9 KB input.

