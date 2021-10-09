from typing import List

from valder_ciphers import *
import argparse
import os.path

supported_ciphers: List[str] = ['caesar', 'vigenere', 'null']


def process(args: argparse.Namespace):
    if not os.path.isfile(args.input):
        raise RuntimeError(f"File not found: {args.input}")

    with open(args.input, "rt") as file:
        content: List[str] = file.readlines()

        if args.encrypt:
            encrypt(args, content)
        elif args.decrypt:
            decrypt(args, content)
        else:
            raise RuntimeError("Neither --encrypt nor --decrypt were specified.")
        print(f"Output file: {args.output}")


def encrypt(args: argparse.Namespace, content: List[str]):
    with open(args.output, "wt") as file:
        if args.encrypt == 'null':
            null = NullCipher()
            file.writelines(null.encode(line) for line in content)
        elif args.encrypt == 'caesar':
            caesar = CaesarCipher(args.shift)
            file.writelines(caesar.encode(line) for line in content)
        elif args.encrypt == 'vigenere':
            vigenere = VigenereCipher(args.keyword)
            file.writelines(vigenere.encode(line) for line in content)
            with open(args.output + "_key.txt", "wt") as keyfile:
                keyfile.write(vigenere.key)
                keyfile.write("\n")
                print(f"Key: {args.output + '_key.txt'}")
        else:
            raise RuntimeError(f"Cipher not recognized: {args.encrypt}")


def decrypt(args: argparse.Namespace, content: List[str]):
    with open(args.output, "wt") as file:
        if args.decrypt == 'null':
            null = NullCipher()
            file.writelines(null.decode(line) for line in content)
        elif args.decrypt == 'caesar':
            caesar = CaesarCipher(args.shift)
            file.writelines(caesar.decode(line) for line in content)
        elif args.decrypt == 'vigenere':
            if not os.path.isfile(args.decrypt_key):
                parser.error("No decrypt key specified.")
                exit(1)
            vigenere = VigenereCipher("")
            with open(args.decrypt_key, "rt") as keyfile:
                vigenere.key = keyfile.readline()
                file.writelines(vigenere.decode(line) for line in content)
        else:
            raise RuntimeError(f"Cipher not recognized: {args.decrypt}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ciphers and deciphers text files")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--encrypt',
        choices=supported_ciphers,
        dest='encrypt',
        help='Encrypt using specified algorithm.',
    )
    group.add_argument(
        '--decrypt',
        choices=supported_ciphers,
        dest='decrypt',
        help='Decrypt using specified algorithm.',
    )
    parser.add_argument(
        '--input',
        required=True,
        dest='input',
        type=str,
        help='Path to the input text file.',
    )
    parser.add_argument(
        '--output',
        required=True,
        dest='output',
        type=str,
        help='Path to the output text file.',
    )
    parser.add_argument(
        '--shift',
        dest='shift',
        type=int,
        help='Shift for Caesar encryption.',
    )
    parser.add_argument(
        '--keyword',
        dest='keyword',
        type=str,
        help='Keyword used for encrypting using Vigenere cipher.',
    )
    parser.add_argument(
        '--decrypt-key',
        dest='decrypt_key',
        type=str,
        help='Path to the file with key used for encrypting using Vigenere cipher.',
    )
    arguments = parser.parse_args()
    process(arguments)
