--store_text_bounding_box --store_config --bbox --augment -rot 40 -noise 40 --hw_text -n 4 --x_offset 30 --y_offset 20 --wrinkles -ca 45 --random_dc 0.5 --random_grid_present 0.9 --random_add_header 0.5 --random_resolution -r 200 --random_grid_color --fully_random -se 10


python gen_ecg_images_from_data_batch.py -i /mnt/experiments1/felipe.dias/raw/physionet.org/files/challenge-2021/1.0.3/training/chapman_shaoxing/g1 -o data_test --store_text_bounding_box --store_config --bbox --augment -rot 40 -noise 40 --hw_text -n 4 --x_offset 30 --y_offset 20 --wrinkles -ca 45 --random_dc 0.5 --random_grid_present 0.9 --random_add_header 0.5 --random_resolution -r 200 --random_grid_color --fully_random -se 10


python gen_ecg_images_from_data_batch.py -i /mnt/experiments1/felipe.dias/DATASETS/cinc2021/Ningbo/WFDB_Ningbo -o data_test

python gen_ecg_images_from_data_batch.py -i /mnt/experiments1/felipe.dias/DATASETS/cinc2021/CPSC2018/WFDB_CPSC2018 -o data_test

python gen_ecg_images_from_data_batch.py -i /mnt/experiments1/felipe.dias/DATASETS/cinc2021/Ga/WFDB_Ga -o data_test



# PTB-XL Challenge 2024
python gen_ecg_images_from_data_batch.py -i /mnt/experiments2/felipe.dias/CINC_CHALLENGE_2024/physionet.org/files/ptb-xl/1.0.3/records100 -o data_test --store_text_bounding_box --store_config --bbox --augment -rot 40 -noise 40 --hw_text -n 4 --x_offset 30 --y_offset 20 --wrinkles -ca 45 --random_dc 0.5 --random_grid_present 0.9 --random_add_header 0.5 --random_resolution -r 200 --random_grid_color --fully_random -se 10

# PTB-XL Challenge 2021
python gen_ecg_images_from_data_batch.py -i /mnt/experiments1/felipe.dias/raw/physionet.org/files/challenge-2021/1.0.3/training/ptb-xl/g1 -o data_test --store_text_bounding_box --store_config --bbox --augment -rot 40 -noise 40 --hw_text -n 4 --x_offset 30 --y_offset 20 --wrinkles -ca 45 --random_dc 0.5 --random_grid_present 0.9 --random_add_header 0.5 --random_resolution -r 200 --random_grid_color --fully_random -se 10