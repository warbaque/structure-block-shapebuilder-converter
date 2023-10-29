#! /usr/bin/env python3

import nbtlib
import json
from pprint import pp
import argparse
import sys

#================================================

def parse_args():
    parser = argparse.ArgumentParser(
        prog='transformer',
        description='Transforms structure block format into shapebuilder')

    parser.add_argument('nbt', help="nbt file to transform")
    parser.add_argument('-p', '--palette', default="palette.json", help="palette mappings to be used (default=palette.json)")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default='-', help="output file (default=stdout)")

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()

#================================================

def transform(nbt_file, palette, out):
    nbt_file = nbtlib.load(nbt_file)
    with open(palette) as f:
        palette_keys = json.load(f)

    x_size, y_size, z_size = nbt_file['']['size']
    layered_shape = [[[' '] * x_size for _ in range(y_size)] for _ in range(z_size)]
    palette_mapping = [palette_keys[block['Name']] for block in nbt_file['']['palette']]

    for block in nbt_file['']['blocks']:
        x, y, z = block['pos']
        layered_shape[z][y][x] = palette_mapping[block['state']]

    for z in range(z_size):
        for y in range(y_size):
            layered_shape[z][y] = ''.join(layered_shape[z][y])

    pp(layered_shape, depth=2, stream=out)

#================================================

args = parse_args()
transform(nbt_file=args.nbt, palette=args.palette, out=args.output)
