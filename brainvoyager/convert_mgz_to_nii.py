#!/usr/bin/python

import argparse
import numpy as np
import nibabel as nib

parser = argparse.ArgumentParser(description='Converts mgz to nii.gz')
parser.add_argument('--input',
                    '-i',
                    required=True,
                    type=str,
                    help='Input File')
parser.add_argument('--output',
                    '-o',
                    required=False,
                    type=str,
                    help='Output File')
args = parser.parse_args()

if args.output is None:
    args.output = args.input.replace('.mgz', '.nii.gz')
print(f'converting {args.input} to {args.output}')

data = nib.load(args.input)
# print(data.affine)
# data.affine = np.array([
#     [-1., 0., 0., 256.],
#     [0., 0., 1., 0.],
#     [0., -1., 0., 256.],
#     [0., 0., 0., 1.]]
# )

affine = data.affine

print('apply transformations...')
data = np.swapaxes(data.get_fdata(), 1, 2)
data = np.flip(data, axis=2)
data = np.flip(data, axis=0)

img_nifti = nib.Nifti1Image(data,
                            np.eye(4),  # data.affine,
                            header=nib.Nifti1Header())

nib.nifti1.save(img_nifti, args.output)
