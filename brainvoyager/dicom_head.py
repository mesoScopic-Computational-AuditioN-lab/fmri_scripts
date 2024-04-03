#!/home/mahdi/anaconda3/bin/python

import argparse
import numpy as np
import bvbabel as bv
import nibabel as nb
import pickle as pkl

from glob import glob

from pydicom import dcmread

parser = argparse.ArgumentParser()
parser.add_argument('-f',
                    '--filename',
                    dest='filename',
                    type=str,
                    help='Filename.',
                    required=True)
args = parser.parse_args()
filename = args.filename

ds = dcmread(filename)
for element in ds:
    print(element)

