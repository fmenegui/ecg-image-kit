python gen_ecg_images_from_data_batch.py -i /home/fdias/Documents/gitlab/gen_data_cinc24/dataset/ptbxl_sample/00000 -o /home/fdias/Documents/gitlab/gen_data_cinc24/output --store_text_bounding_box --store_config --bbox --augment -noise 40 --hw_text -n 4 --x_offset 30 --y_offset 20 --wrinkles -ca 45 --random_dc 0.5 --random_grid_present 0.8 --random_add_header 0.5 -r 200 --random_grid_color --fully_random -se 10 --num_columns 2 --full_mode None

/home/fdias/Documents/gitlab/gen_data_cinc24/output



# lead only
python gen_ecg_images_from_data_batch.py -i /home/fdias/Documents/gitlab/gen_data_cinc24/dataset/ptbxl_sample/00000 -o /home/fdias/Documents/gitlab/gen_data_cinc24/output --deterministic_lead --random_dc 0.0 --random_grid_present 0.0 --random_add_header 0.0 -r 200 -se 10 --num_columns 2 --full_mode None 




# background only
python gen_ecg_images_from_data_batch.py -i /home/fdias/Documents/gitlab/gen_data_cinc24/dataset/ptbxl_sample/00000 -o /home/fdias/Documents/gitlab/gen_data_cinc24/output --store_text_bounding_box --store_config --bbox --augment -noise 40 --hw_text -n 4 --x_offset 30 --y_offset 20 --wrinkles -ca 45 --random_dc 0.0 --random_grid_present 1.0 --random_add_header 0.5 -r 200 --random_grid_color --fully_random -se 10 --num_columns 2 --full_mode None --background_only




python gen_ecg_images_from_data_batch.py -i /home/fdias/Documents/gitlab/gen_data_cinc24/dataset/ptbxl_sample/00000 -o /home/fdias/Documents/gitlab/gen_data_cinc24/output --random_dc 1.0 --random_grid_present 1.0 --random_add_header 0.0 -r 200 -se 10 --num_columns 2 --full_mode 'I,II' 
-i /home/fdias/Documents/gitlab/gen_data_cinc24/dataset/ptbxl_sample/00000 -o /home/fdias/Documents/gitlab/gen_data_cinc24/output --random_dc 1.0 --random_grid_present 1.0 --random_add_header 0.0 -r 200 -se 10 --num_columns 2 --full_mode 'I,II' 


-i /home/fdias/Documents/gitlab/gen_data_cinc24/dataset/ptbxl_sample/00000 -o /home/fdias/Documents/gitlab/gen_data_cinc24/output --random_dc 1.0 --random_grid_present 1.0 --random_add_header 0.0 -r 200 -se 10 --num_columns 2 --full_mode 'I' 




---
python gen_ecg_images_from_data_batch.py -i /home/fdias/Documents/gitlab/gen_data_cinc24/dataset/ptbxl_sample/00000 -o /home/fdias/Documents/gitlab/gen_data_cinc24/output --random_dc 1.0 --random_grid_present 1.0 --random_add_header 0.0 -r 200 -se 10 --num_columns 4 --full_mode 'I,II'
python gen_ecg_images_from_data_batch.py -i /home/fdias/Documents/gitlab/gen_data_cinc24/dataset/ptbxl_sample/00000 -o /home/fdias/Documents/gitlab/gen_data_cinc24/output --random_dc 1.0 --random_grid_present 1.0 --random_add_header 0.0 -r 200 -se 10 --num_columns 4 --full_mode 'V1,V6'