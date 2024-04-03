#!/home/mahdi/anaconda3/bin/python

import argparse
import numpy as np
import bvbabel as bv
import nibabel as nb
import pickle as pkl

from glob import glob

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-i',
                   '--input_dir',
                   dest='input_dir',
                   type=str,
                   help='Input directory')

group.add_argument('-f',
                   '--filename',
                   dest='filename',
                   type=str)

parser.add_argument('-o',
                    '--output_dir',
                    dest='output_dir',
                    type=str,
                    help='Output directory',
                    required=False)

args = parser.parse_args()

if args.output_dir is None:
    if args.filename is None:
        output_dir = args.input_dir.replace('.vmr', '.nii.gz')
    else:
        output_dir = args.filename.replace('.vmr', '.nii.gz')
else:
    output_dir = args.output_dir

if args.filename:
    print(f'converting {args.filename}')
    header, data = bv.vmr.read_vmr(args.filename)

    print('pickeling header...', end=' ')
    try:
        with open(output_dir + args.filename.replace('.vmr', '.pkl'), 'wb') as f:
            pkl.dump(header, f)
    except Exception as e:
        print('Error')
    img = nb.Nifti1Image(data, affine=np.eye(4))
    nb.save(img, output_dir)
    print('done!')
    exit(0)

elif args.input_dir:

    for file in glob(args.input_dir + '*.vmr'):
        print('found: %s' % file)
        header, data = bv.vmr.read_vmr(file)
        print('pickeling header...', end=' ')
        with open(output_dir + file.replace('.vmr', '.pkl'), 'wb') as f:
            pkl.dump(header, f)
        img = nb.Nifti1Image(data, affine=np.eye(4))
        img.header["pixdim"][1] = header["VoxelSizeX"]
        img.header["pixdim"][2] = header["VoxelSizeY"]
        img.header["pixdim"][3] = header["VoxelSizeZ"]
        nb.save(img, output_dir + file.replace('.vmr', '.nii.gz'))
        print('done!')

    exit(0)
