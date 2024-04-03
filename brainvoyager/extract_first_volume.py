#!/home/mahdi/anaconda3/bin/python
""" Extracts first volume from nifti. """

import numpy as np
import argparse

import nibabel as nb

parser = argparse.ArgumentParser()

parser.add_argument('-f',
                    '--filename',
                    dest='filename',
                    type=str,
                    help='File name.',
                    required=True)

args = parser.parse_args()


def extract_volume(filename):
    data = nb.load(filename).get_fdata()
    data_1vol = data[..., 1]
    data_1vol = np.expand_dims(data_1vol, -1)

    new_filename = filename.replace('.nii', '_1vol.nii')
    img = nb.Nifti1Image(data_1vol, np.eye(4))
    nb.save(img, new_filename)
    print(f'File saved as {new_filename}')


if args.filename:
    extract_volume(args.filename)
