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

for file in glob(input_dir + '*.fmr'):
    print('found: %s' % file)
    header, data = bv.fmr.read_fmr(file)
    print('pickeling header...', end=' ')
    with open(output_dir + file.replace('.fmr', '.pkl'), 'wb') as f:
        pkl.dump(header, f)
    img = nb.Nifti1Image(data, affine=np.eye(4))
    nb.save(img, output_dir + file.replace('.fmr', '.nii.gz'))
    print('done!')
