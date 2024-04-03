#!/home/mahdi/anaconda3/bin/python
""" Converts Nifti to fmr. """

import sys
import argparse
import pickle as pkl
from glob import glob

import numpy as np
import bvbabel as bv
import nibabel as nb


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('-i',
                   '--input_dir',
                   dest='input_dir',
                   type=str,
                   help='Input directory.')
group.add_argument('-f',
                   '--file',
                   dest='file',
                   type=str)
parser.add_argument('-o',
                    '--output_dir',
                    dest='output_dir',
                    type=str,
                    help='Output directory.',
                    required=True)
args = parser.parse_args()

output_dir = args.output_dir


def convert_file(file):
    print('converting file to fmr...')
    try:
        with open(file.replace('.nii.gz', '.pkl'), 'rb') as f:
            header = pkl.load(f)
    except FileNotFoundError:
        sys.stderr.write('Error: Did not find header, skipping!\n')
        return -1
    except Exception as e:
        print(e)
        return -1
    nifti_data = nb.load(file).get_fdata()
    output_filename = output_dir + '/' + \
        file.split('/')[-1].replace('.nii.gz', '.fmr')
    x, y, z, t = nifti_data.shape
    bv.fmr.write_fmr(output_filename,
                     header,
                     nifti_data.astype(np.uint8))


def convert_dir(input_dir):
    print('Warning! Ignoring fmr for now...')
    for file in glob(input_dir + '*.nii*'):
        print(f'found: {file}')
        print('converting file to stc...')

        nifti_data = nb.load(file).get_fdata()
        nifti_filename = file.split('/')[-1]
        new_stc_filename = file.replace(".nii.gz", ".stc")
        bv.stc.write_stc(new_stc_filename, nifti_data)

        # change the prefix and write fmr in new file
        # new_fmr_filename = nifti_filename.replace('.nii.gz', '.fmr')
        # old_fmr_filename = file.replace('_transformed.nii.gz', '.fmr').split('/')[-1]
        # print(new_fmr_filename)
        # print(old_fmr_filename)
        # with open(old_fmr_filename, 'r') as f:
        #     fmr_data = f.read()
        # fmr_filename = file.split('/')[-1]
        # fmr_data = fmr_data.replace(old_fmr_filename.split('.')[0],
        #                             new_fmr_filename.split('.')[0])
        # new_fmr_file = open(new_fmr_filename, 'w')
        # new_fmr_file.write(fmr_data)
        # new_fmr_file.close()


if args.input_dir:
    convert_dir(args.input_dir)
elif args.file:
    convert_file(args.file)
