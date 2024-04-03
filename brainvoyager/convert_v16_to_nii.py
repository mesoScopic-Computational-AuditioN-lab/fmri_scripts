#!/usr/bin/python

import argparse
import numpy as np
import pickle as pkl
import nibabel as nib
import bvbabel as bvb

parser = argparse.ArgumentParser(description='Converts v16 to nii.gz')
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
parser.add_argument('--set_voxel_size',
                    '-s',
                    required=False,
                    type=str,
                    help='Output File')

args = parser.parse_args()

if args.output is None:
    args.output = args.input.replace('.v16', '.nii.gz')

print(f'converting {args.input} to {args.output}')

header, data = bvb.v16.read_v16(args.input)
img = nib.Nifti1Image(data, affine=np.eye(4))

if args.set_voxel_size is None:
    img.header["pixdim"][1] = header["VoxelSizeX"]
    img.header["pixdim"][2] = header["VoxelSizeY"]
    img.header["pixdim"][3] = header["VoxelSizeZ"]
else:
    img.header["pixdim"][1] = args.set_voxel_size
    img.header["pixdim"][2] = args.set_voxel_size
    img.header["pixdim"][3] = args.set_voxel_size

nib.save(img, args.output)

print('pickeling header...', end=' ')
try:
    with open(args.input.replace('.v16', '.pkl'), 'wb') as f:
        pkl.dump(header, f)
        print('done!')
except Exception as e:
    print(f'Error, {e}')
