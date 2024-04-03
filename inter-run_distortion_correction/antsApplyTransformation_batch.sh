#!/bin/bash

set -m
# Non Linear Coregistration (Syn, by ANTs)

if [ $# -lt 2 ]; then
    echo "Usage: $0 <REFERENCE_VOLUME_FILENAME> <INPUT_VOLUME_LIST_FILENAME>"
    exit 1
fi

# define the function to be run in batch/parallel
function call_antsApplyTransformation {
  # input filename
  input_volume_filename="${dataPath}/${1}"

  # output filename
  output_volume_filename=$(basename ${input_volume_filename} )
  input_volume_filename_stripped=$(sed 's/\.nii\.gz//g' <<< $output_volume_filename)
  output_volume_filename="${outfld}/${input_volume_filename_stripped}_transformed.nii.gz"

  # transform filename
  warp_transformation_filename=${dataPath}/registrations/${input_volume_filename_stripped}_1vol_registered_1Warp.nii.gz
  affine_transformation_filename=${dataPath}/registrations/${input_volume_filename_stripped}_1vol_registered_0GenericAffine.mat

  if [ ! -f ${warp_transformation_filename} ] || [ ! -f ${warp_transformation_filename} ]
  then
  	echo "WARNING, transformation files not found, exiting!"
  	exit -1
  fi

  # actual start of code
  antsApplyTransforms -d 3 -e 3 -i ${input_volume_filename} \
		    		  -o ${output_volume_filename} \
				      -r ${REFERENCE_VOLUME_FILENAME} \
				      -t ${warp_transformation_filename} \
				      -t ${affine_transformation_filename}
}

# start of code
REFERENCE_VOLUME_FILENAME="$1"
INPUT_VOLUME_LIST_FILENAME="$2"


echo -e "Using reference volume: \t$(basename $REFERENCE_VOLUME_FILENAME)"

dataPath=$(dirname $REFERENCE_VOLUME_FILENAME)
myITK=${dataPath}

outfld=${dataPath}/transformations
mkdir -p ${outfld}
cd ${outfld}

# Call batch/parallel loop
while read line; do
	echo -e "Transforming source volume: \t$(basename $line)" | tee -a ${dataPath}/transformation_report.txt
	{ time call_antsApplyTransformation $line ; } 2>&1 | tee -a ${dataPath}/transformation_report.txt
	echo -e "\n\nFinished processing ${line}!\n\n" | tee -a ${dataPath}/transformation_report.txt
done <$INPUT_VOLUME_LIST_FILENAME

echo "All operations are completed!"


