#!/bin/bash
OTHER_ARGS="--store_text_bounding_box --store_config --bbox --augment -rot 40 -noise 40 --hw_text -n 4 --x_offset 30 --y_offset 20 --wrinkles -ca 45 --random_dc 0.5 --random_grid_present 0.95 --random_add_header 0.5 --random_resolution -r 200 --random_grid_color --fully_random -se 10"

BASE_PATH="/mnt/experiments1/felipe.dias/raw/physionet.org/files/challenge-2021/1.0.3/training"
SAVE_DIR="/mnt/experiments1/felipe.dias/IMG_CINC_CHALLENGE_2021/NOISE4X3"

FOLDERS=("chapman_shaoxing" "cpsc_2018" "cpsc_2018_extra" "georgia" "ningbo")


for folder in "${FOLDERS[@]}"; do

    SUBFOLDERS=$(find "$BASE_PATH/$folder" -mindepth 1 -maxdepth 1 -type d)

    for subfolder in $SUBFOLDERS; do
        subfolder_name=$(basename "$subfolder")
        output_dir="$SAVE_DIR/$folder/$subfolder_name"
        mkdir -p "$output_dir"

        JOB_FILE="slurm_job_${folder}_${subfolder_name}.sh"
        cat << EOF > $JOB_FILE
#!/bin/bash
#SBATCH --job-name=img_${folder}_${subfolder}
#SBATCH --time=7-00:00:00  # Adjust based on expected runtime
#SBATCH --mem=10240
#SBATCH --partition=dark
#SBATCH --nodelist=darkside3

mp_dir="tmp_$$_$(date +%Y%m%d_%H%M%S)_$RANDOM"
mkdir -p "$tmp_dir"
cd "$tmp_dir"
echo "Created temporary working directory."
git clone -b fmenegui-change https://github.com/fmenegui/ecg-image-kit.git
cd ecg-image-kit/codes/ecg-image-generator
python gen_ecg_images_from_data_batch.py -i "$subfolder" -o "$output_dir" $OTHER_ARGS
EOF


    sbatch $JOB_FILE
done
done

