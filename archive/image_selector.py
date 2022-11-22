#!/usr/bin/python

import configparser
import argparse
import re

parser = argparse.ArgumentParser(description='Prase ini file and return image name')
parser.add_argument('-f', '--file', help='ini file to parse', required=True)
parser.add_argument('-s','--section', help='section to parse', required=True)
parser.add_argument('-i', '--image', help='option to parse', required=True)

args = parser.parse_args()

config = configparser.ConfigParser(allow_no_value=True)
config.read(args.file)
images = config[args.section]

# use regex to find an item within images that contains the image name
for item in images:
    if re.search(args.image, item):
        print(item)
        break