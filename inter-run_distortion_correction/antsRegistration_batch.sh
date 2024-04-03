#!/bin/bash
# Non Linear Coregistration (Syn, by ANTs)

if [ $# -lt 2 ]; then
    echo "Usage: $0 <TARGET_VOLUME_FILENAME> <SOURCE_VOLUME_LIST_FILENAME>"
    exit 1
fi

# define the function to be run in batch/parallel
function call_antsRegistration {
  source_volume_filename="${dataPath}/${1}"
  filename="${source_volume_filename%.*}" # get the filename without extension
  filename=$(basename $filename)

  # actual start of code
	antsRegistration \
	 --verbose 0 \
	 --dimensionality 3 \
	 --float 1 \
	 --output [${outfld}/${filename}_registered_, \
	 		   ${outfld}/${filename}_Warped.nii.gz, \
	 		   ${outfld}/${filename}_InverseWarped.nii.gz] \
	 --interpolation BSpline[5] \
	 --use-histogram-matching 0 \
	 --winsorize-image-intensities [0.005,0.995] \
	 --transform Rigid[0.05] \
	 --metric MI[${TARGET_VOLUME_FILENAME},${source_volume_filename},0.7,32,Regular,0.1] \
	 --convergence [1000x500,1e-6,10] \
	 --shrink-factors 4x2 \
	 --smoothing-sigmas 1x0vox \
	 --transform Affine[0.1] \
	 --metric MI[${TARGET_VOLUME_FILENAME},${source_volume_filename},0.7,32,Regular,0.1] \
	 --convergence [1000x500,1e-6,10] \
	 --shrink-factors 4x2 \
	 --smoothing-sigmas 1x0vox \
	 --transform SyN[0.1,2,0] \
	 --metric CC[${TARGET_VOLUME_FILENAME},${source_volume_filename},1,2] \
	 --convergence [500x100,1e-6,10] \
	 --shrink-factors 2x1 \
	 --smoothing-sigmas 1x0vox
}

# start of code
TARGET_VOLUME_FILENAME="$1"
SOURCE_VOLUME_LIST_FILENAME="$2"


echo -e "Using target volume: \t\t$(basename $TARGET_VOLUME_FILENAME)" | tee -a report.txt
dataPath=$(dirname $TARGET_VOLUME_FILENAME)
myITK=${dataPath}

outfld=${dataPath}/registrations
mkdir -p ${outfld}
cd ${outfld}

# Call batch/parallel loop
while read line; do
  echo -e "Registering source volume: \t$(basename $line)" | tee -a ${dataPath}/report.txt
	{ time call_antsRegistration $line ; } 2>&1 | tee -a ${dataPath}/report.txt
	echo -e "\n\nFinished processing ${line}!\n\n" | tee -a ${dataPath}/report.txt
done <$SOURCE_VOLUME_LIST_FILENAME

echo "All operations are completed!"
