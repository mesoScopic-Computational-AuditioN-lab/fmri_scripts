#!/home/mahdi/anaconda3/bin/python

import argparse
import numpy as np
import bvbabel as bv
import nibabel as nb
import pickle as pkl

from glob import glob

parser = argparse.ArgumentParser()
parser.add_argument('-i',
                    '--input_dir',
                    dest='input_dir',
                    type=str,
                    help='Input directory.',
                    required=True)
parser.add_argument('-o',
                    '--output_dir',
                    dest='output_dir',
                    type=str,
                    help='Output directory.',
                    required=True)
args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

for file in glob(input_dir + '*.vmr'):
    print('found: %s' % file)
    print('pickeling file...', end=' ')
    header, _ = bv.vmr.read_vmr(file)
    with open(output_dir + file.replace('.vmr', '.pkl'), 'wb') as f:
        pkl.dump(header, f)
    print('done!')

