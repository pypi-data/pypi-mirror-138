#!/usr/bin/python3

###########################################################################
#      ____  _____________  __    __  __ _           _____ ___   _        #
#     / __ \/ ____/ ___/\ \/ /   |  \/  (_)__ _ _ __|_   _/ __| /_\  (R)  #
#    / / / / __/  \__ \  \  /    | |\/| | / _| '_/ _ \| || (__ / _ \      #
#   / /_/ / /___ ___/ /  / /     |_|  |_|_\__|_| \___/|_| \___/_/ \_\     #
#  /_____/_____//____/  /_/      T  E  C  H  N  O  L  O  G  Y   L A B     #
#                                                                         #
#          Copyright 2022 Deutsches Elektronen-Synchrotron DESY.          #
#                          All rights reserved.                           #
#                                                                         #
###########################################################################

import argparse
import os
from itertools import zip_longest
from array import array
import hashlib
from bin2hpm import rle


def _grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') -> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)


def pad_key(key):
    return key + b' ' * (4 - len(key))


def enc_u32(val):
    return int.to_bytes(val, length=4, byteorder='big')


def enc_u8(val):
    return int.to_bytes(val, length=1, byteorder='big')


def convert_int_item(key, val):
    result = pad_key(key)
    result += enc_u32(4)
    result += enc_u32(val)
    return result


def convert_dec_item(key, val, blksize=None):
    return convert_int_item(key, int(val, 10))


def convert_hex_item(key, val, blksize=None):
    return convert_int_item(key, int(val, 16))


def convert_bitstream_item(key, val, blksize=None):
    offs, val = val.split(b' ')
    offs = int(offs, 10)
    result = b''

    payload = array('B')
    for bin_byte in _grouper(8, val):
        bin_byte = bytes(bin_byte).decode('utf-8')
        payload.append(int(bin_byte, 2))

    # Process bitstream in blocks
    blocks = _grouper(blksize, payload) if blksize is not None else [payload]

    for bin_blk in blocks:
        # Remove fill elements inserted by grouper
        bin_blk = array('B', filter(lambda x: x is not None, bin_blk))
        # Create RLE-encoded block
        block = enc_u32(offs)
        block += bytes(rle.encode(bin_blk))
        result += pad_key(key) + enc_u32(len(block)) + block
        offs += len(bin_blk) * 8

    return result


def convert_ftrow_item(key, val, blksize=None):
    payload = array('B')
    for bin_byte in _grouper(8, val):
        # Feature Row is in reverse bit order
        bin_byte = bin_byte[::-1]
        bin_byte = bytes(bin_byte).decode('utf-8')
        payload.append(int(bin_byte, 2))

    # Feature Row needs weird re-ordering
    payload = payload[7::-1] + payload[9:7:-1]

    return pad_key(key) + enc_u32(len(payload)) + bytes(payload)


CONV_TBL = {
    b'QP': convert_dec_item,        # Num. pins
    b'QF': convert_dec_item,        # Num. fuses
    b'L': convert_bitstream_item,   # Fuse data
    b'E': convert_ftrow_item,       # Feature row
    b'C': convert_hex_item,         # Fuse checksum
    # We don't need G, F, and UH
    # b'G': convert_dec_item,     # security fuses
    # b'F': convert_dec_item,     # fuse default
    # b'UH': convert_hex_item,    # user code
}


def jed_conv(infile, blksize=None):
    hash = hashlib.md5()

    with open(infile) as f:
        b = b''
        for line in f:
            # Remove comments and linefeeds
            l = line.strip().encode('utf-8')
            if l.startswith(b'\x02') or l.startswith(b'NOTE'):
                continue
            hash.update(l)
            if l.startswith(b'L'):
                # Line feed separates address from contents, add whitespace to keep separation
                l += b' '
            b += l

    # Save first 32 bits of hash as checksum
    u32_hash = hash.digest()[:4]
    # "CPLD" serves as magic value
    result = convert_int_item(
        b'CPLD', int.from_bytes(u32_hash, byteorder='big'))
    # Split .jed data into tokens and convert each one
    for item in b.split(b'*'):
        for key, func in CONV_TBL.items():
            if item.startswith(key):
                k, v = item[:len(key)], item[len(key):]
                result += func(k, v, blksize)
    return result, u32_hash


def main():
    parser = argparse.ArgumentParser(
        description='.jed file parser / converter'
    )
    parser.add_argument('infile',
                        type=str,
                        help='Source file for reading'
                        )
    parser.add_argument('-o', '--outfile',
                        type=str,
                        help='output file (derived from input file if not set)'
                        )
    parser.add_argument('-b', '--blksize',
                        type=int,
                        help='max. block size per packet'
                        )
    args = parser.parse_args()

    outfile = args.outfile
    if not outfile:
        basename, _ = os.path.splitext(os.path.basename(args.infile))
        outfile = basename + '.bin'

    print(f'Converting {args.infile} to {outfile}')
    with open(outfile, 'wb') as f:
        f.write(jed_conv(args.infile, blksize=args.blksize)[0])


if __name__ == '__main__':
    main()
