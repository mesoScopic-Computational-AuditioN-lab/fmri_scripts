#!/home/mahdi/anaconda3/bin/python
""" Converts Nifti to vmr. """

import sys
import argparse
import pickle as pkl
from glob import glob

import numpy as np
import bvbabel as bv
import nibabel as nb

from pprint import pprint

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
parser.add_argument('-s',
                    '--shape',
                    dest='shape',
                    type=str,
                    help='Data Shape.',
                    required=False)
parser.add_argument('-r',
                    '--header',
                    dest='header',
                    type=str,
                    help='VMR Header File.',
                    required=False)
args = parser.parse_args()

output_dir = args.output_dir


def convert_file(file, header=None):
    print('converting file to vmr...')
    if header is not None:
        try:
            with open(header.replace('.nii.gz', '.pkl'), 'rb') as f:
                header = pkl.load(f)
        except Exception as e:
            raise ValueError(e)
    else:
        try:
            print('Using default header...')
            with open(file.replace('.nii.gz', '.pkl'), 'rb') as f:
                header = pkl.load(f)
        except FileNotFoundError:
            sys.stderr.write(f'Error: Did not find header "{header}", skipping!\n')
            print('You may want to use the --header flag.')
            return -1
        except Exception as e:
            print(e)
            return -1
    nifti_data = nb.load(file).get_fdata()
    output_filename = file.split('/')[-1].replace('.nii.gz', '.vmr')
    x, y, z = nifti_data.shape
    # print(x, y, z)
    header['DimX'] = z
    header['DimY'] = x
    header['DimZ'] = y
    # pprint(header)
    bv.vmr.write_vmr(output_filename,
                     header,
                     nifti_data.astype(np.uint8))


def convert_dir(input_dir, header=None):
    for file in glob(input_dir + '*.nii*'):
        print('found: %s' % file)
        print('converting file to vmr...')
        try:
            with open(file.replace('.nii.gz', '.pkl'), 'rb') as f:
                header = pkl.load(f)
        except FileNotFoundError:
            sys.stderr.write('Error: Did not find header, skipping!\n')
            continue
        except Exception as e:
            print(e)
            continue
        nifti_data = nb.load(file).get_fdata()
        output_filename = output_dir + '/' + \
            file.split('/')[-1].replace('.nii.gz', '.vmr')
        x, y, z = nifti_data.shape
        header['DimX'] = x
        header['DimY'] = y
        header['DimZ'] = z
        # if parse_args.shape is not None:

        bv.vmr.write_vmr(output_filename,
                         header,
                         nifti_data.astype(np.uint8))


if args.input_dir:
    convert_dir(args.input_dir, args.header)
elif args.file:
    convert_file(args.file, args.header)
