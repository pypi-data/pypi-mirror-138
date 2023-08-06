#!/usr/bin/env python

import argparse
import logging
import math
import sys

from PIL import Image
from pyzbar.pyzbar import decode


def _to_image(qrcode: list, black_char: str) -> Image:
    """
    Converts an ASCII QR code list to a RGB image.
    :param qrcode: The ASCII QR code.
    :param black_char: The character in the ASCII QR code that represents the black squares.
    :return: A QR code with a white background.
    """
    img = Image.new('RGB', (len(qrcode[0]), len(qrcode)), 'white')
    pixels = img.load()

    for y, line in enumerate(qrcode):
        for x, _ in enumerate(line):
            if qrcode[y][x] == black_char:
                pixels[y, x] = (0, 0, 0)

    img = img.resize((img.width * 2, img.height * 2))

    return img


def _calculate_width(num_chars: int) -> int:
    """
    Calculates the width of the qr code for decoding.
    :param num_chars: The length of the ASCII QR code.
    :return: The width of the QR code.
    """
    # QR Codes are perfect squares, so calculating the square root will find the width.
    square_factor = math.sqrt(num_chars)

    if square_factor.is_integer():
        return int(square_factor)

    raise RuntimeError("No width was found for the QR code, are there trailing characters?")


def _read_file(file) -> list:
    """
    Reads an ASCII QR code file into a list of lines.
    :param file: The filename to read from.
    :return: A list of lines.
    """
    with open(file) as f:
        qrcode = f.readlines()

    # If the qr code is not broken up.
    if len(qrcode) == 1:
        # Strip all newlines.
        contents = "".join([line.strip() for line in qrcode])
        width = _calculate_width(len(contents))

        if len(contents) % width != 0:
            raise RuntimeError(f"QR code has characters left over after dividing by width ({width}).")

        qrcode = []
        for i in range(0, int(len(contents)/width)):
            start = i * width
            qrcode.append(contents[start:start + width])

    # Extra spaces are needed after second newline to ensure top row of QR code is indented.
    logging.info(f"Read the following QR Code from %s:\n\n  %s\n",
                 file, "\n  ".join(qrcode))

    return qrcode


def _get_chars(qrcode_chars: list) -> list:
    """
    Retrieves the set of characters that make up the QR code.
    :param qrcode_chars: The ASCII QR code.
    :return: A list of two QR code characters.
    """
    first_char = qrcode_chars[0][0]
    for line in qrcode_chars:
        for c in line:
            if c != first_char:
                return [first_char, c]

    raise RuntimeError("ASCII QR code only uses one character, unable to decode.")


def parse_ascii_qrcode(file: str, dump_qr_code: bool = False) -> str:
    """
    Retrieves the data from an ASCII QR code.
    :param file: The filename to read from.
    :param dump_qr_code: Whether to write the QR code image to disk.
    :return: The data stored in the QR code.
    """
    qrcode_chars = _read_file(file)

    # Loop through the QR code characters to find the black character.
    for c in _get_chars(qrcode_chars):
        img = _to_image(qrcode_chars, c)
        decoded_qr_code = decode(img)
        if decoded_qr_code:
            if dump_qr_code:
                filename = file.rsplit(".", 1)[0] + ".png"
                img.save(filename, 'PNG')
                logging.info(f"Wrote QR code to {filename}")

            return str(decoded_qr_code[0].data, "utf-8")


def _parse_args() -> argparse.Namespace:
    """
    Creates an arg parser for AsciiQrCode and parses the supplied args.
    :return: The parsed args.
    """
    parser = argparse.ArgumentParser(description='Processes ASCII QR Codes.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='Enable verbose logging.')
    parser.add_argument('--dump-qr-code', action='store_true', default=False,
                        help='Write the created QR code image to disc.')
    parser.add_argument('file', type=str, help='A file containing an ASCII QR code.')

    # Print help when no args are supplied.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        exit(1)

    return parser.parse_args()


def _main():
    """
    Separate main function to avoid polluting the main scope.
    :return:
    """
    args = _parse_args()
    logging.getLogger().setLevel(logging.INFO if args.verbose else logging.WARNING)

    data = parse_ascii_qrcode(args.file, args.dump_qr_code)
    print(f"Data from qr code: \n{data}\n")
    exit(0)


if __name__ == '__main__':
    _main()
