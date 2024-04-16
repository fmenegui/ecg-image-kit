#!/usr/bin/env python
# Load libraries.
import os, sys, argparse
import json
import numpy as np
from scipy.io import savemat, loadmat
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from TemplateFiles.generate_template import generate_template
from math import ceil 
from helper_functions import get_adc_gains,get_frequency,get_leads,load_recording,load_header,find_files, truncate_signal, create_signal_dictionary, samples_to_volts, standardize_leads, write_wfdb_file
from ecg_plot import ecg_plot
import wfdb
from PIL import Image, ImageDraw, ImageFont
from random import randint
import random

def get_format(n_cols):
    lst = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
    n_elements_per_col = len(lst) // n_cols
    cols = [lst[i:i+n_elements_per_col] for i in range(0, len(lst), n_elements_per_col)]
    return cols

# format_4_by_3 = [["I", "II", "III"], ["aVR", "aVL", "aVF", "AVR", "AVL", "AVF"], ["V1", "V2", "V3"], ["V4", "V5", "V6"]]

def find_lead_col_position(lead, format):
    for idx, col in enumerate(format):
        if lead in col:
            return idx
    


# Run script.
def get_paper_ecg(input_file,header_file,output_directory, seed, add_dc_pulse,add_bw,show_grid,add_print, start_index = -1, store_configs=False, store_text_bbox=True,key='val',resolution=100,units='inches',papersize='',add_lead_names=True,pad_inches=1,template_file=os.path.join('TemplateFiles','TextFile1.txt'),font_type=os.path.join('Fonts','Times_New_Roman.ttf'),standard_colours=5,full_mode='II',bbox = False, columns=-1, background_only=False, leads_only=False):

    # Extract a reduced-lead set from each pair of full-lead header and recording files.
    full_header_file = header_file
    full_recording_file = input_file
    full_header = load_header(full_header_file)
    full_leads = get_leads(full_header)
    num_full_leads = len(full_leads)

    # Update the header file
    full_lines = full_header.split('\n')

    # For the first line, update the number of leads.
    entries = full_lines[0].split()

    head, tail = os.path.split(full_header_file)

    output_header_file = os.path.join(output_directory, tail)
    with open(output_header_file, 'w') as f:
            f.write('\n'.join(full_lines))

    #Load the full-lead recording file, extract the lead data, and save the reduced-lead recording file.
    recording = load_recording(full_recording_file, full_header,key)
           
    # Get values from header
    rate = get_frequency(full_header)
    adc = get_adc_gains(full_header,full_leads)
    full_leads = standardize_leads(full_leads)
    full_mode = list(map(lambda x:x.split()[0], full_mode.split(',')))
    full_mode_list = full_mode
    print(full_mode_list)
    full_mode = full_mode[0] if len(full_mode)==1 else full_mode
    print(full_mode_list)
    if(len(full_leads)==2):
        full_mode = 'None'
        gen_m = 2
        if(columns==-1):
            columns = 1
    elif(len(full_leads)==12):
        gen_m = 12
        if full_mode not in full_leads and columns!=1:
            full_mode = full_leads[0]
        else:
            full_mode = full_mode
        if(columns==-1):
            columns = 4
    else:
        gen_m = len(full_leads)
        columns = 4
        full_mode = 'None'

    format_4_by_3 = get_format(columns)
    template_name = 'custom_template.png'

    if(recording.shape[0]>recording.shape[1]):
       recording = np.transpose(recording)

    record_dict = create_signal_dictionary(recording,full_leads)
   
    gain_index = 0
    center_function = lambda x: x - x.mean()

    ecg_frame = []
    end_flag = False
    start = 0
    lead_length_in_seconds = 10.0/columns
    abs_lead_step = 10.0

    segmented_ecg_data = {}
    del full_mode
    
    print(full_mode_list)

    if start_index != -1:
        start = start_index
        #do something
        frame = {}
        gain_index = 0
        for key in record_dict:
            for full_mode in full_mode_list:
                gain_index = 0
                if(len(record_dict[key][start:])<int(rate*abs_lead_step)):
                    end_flag = True
                    nanArray = np.empty(len(record_dict[key][start:]))
                    nanArray[:] = np.nan
                    if(full_mode!='None' and key==full_mode):
                        if 'full'+full_mode not in segmented_ecg_data.keys():
                            segmented_ecg_data['full'+full_mode] = nanArray.tolist()
                        else:
                            segmented_ecg_data['full'+full_mode] = segmented_ecg_data['full'+full_mode] + nanArray.tolist()
                    if(key!='full'+full_mode):
                        if key not in segmented_ecg_data.keys():
                            segmented_ecg_data[key] = nanArray.tolist()
                        else:
                            segmented_ecg_data[key] = segmented_ecg_data[key] + nanArray.tolist()
                else:
                    shilftedStart = start
                    shilftedStart = start + find_lead_col_position(key, format_4_by_3)*int(rate*lead_length_in_seconds)
                    end = shilftedStart + int(rate*lead_length_in_seconds)

                    if(key!='full'+full_mode):
                        frame[key] = samples_to_volts(record_dict[key][shilftedStart:end],adc[gain_index])
                        frame[key] = center_function(frame[key])
                        
                        nanArray = np.empty((int(shilftedStart - start)))
                        nanArray[:] = np.nan
                        if key not in format_4_by_3[0]:
                            if key not in segmented_ecg_data.keys():
                                segmented_ecg_data[key] = nanArray.tolist()
                            else:
                                segmented_ecg_data[key] = segmented_ecg_data[key] + nanArray.tolist()
                        if key not in segmented_ecg_data.keys():
                            segmented_ecg_data[key] = frame[key].tolist()
                        else:
                            segmented_ecg_data[key] = segmented_ecg_data[key] + frame[key].tolist()

                        nanArray = np.empty((int(abs_lead_step*rate - (end - shilftedStart) - (shilftedStart - start))))
                        nanArray[:] = np.nan
                        segmented_ecg_data[key] = segmented_ecg_data[key] + nanArray.tolist()
                    if(full_mode!='None' and key==full_mode):
                        if(len(record_dict[key][start:])>int(rate*10)):
                            frame['full'+full_mode] = samples_to_volts(record_dict[key][start:(start+int(rate)*10)],adc[gain_index])
                            frame['full'+full_mode] = center_function(frame['full'+full_mode])
                            if 'full'+full_mode not in segmented_ecg_data.keys():
                                segmented_ecg_data['full'+full_mode] = frame['full'+full_mode].tolist()
                            else:
                                segmented_ecg_data['full'+full_mode] = segmented_ecg_data['full'+full_mode] + frame['full'+full_mode].tolist()
                        else:
                            frame['full'+full_mode] = samples_to_volts(record_dict[key][start:],adc[gain_index])
                            frame['full'+full_mode] = center_function(frame['full'+full_mode])
                            if 'full'+full_mode not in segmented_ecg_data.keys():
                                segmented_ecg_data['full'+full_mode] = frame['full'+full_mode].tolist()
                            else:
                                segmented_ecg_data['full'+full_mode] = segmented_ecg_data['full'+full_mode] + frame['full'+full_mode].tolist()
                    gain_index += 1
            ecg_frame.append(frame)

    else:
        while(end_flag==False):
            # To do : Incorporate column and ful_mode info
            frame = {}
            gain_index = 0
            
            for key in record_dict:
                for full_mode in full_mode_list:
                    gain_index = 0
                    if(len(record_dict[key][start:])<int(rate*abs_lead_step)):
                        end_flag = True
                        nanArray = np.empty(len(record_dict[key][start:]))
                        nanArray[:] = np.nan
                        if(full_mode!='None' and key==full_mode):
                            if 'full'+full_mode not in segmented_ecg_data.keys():
                                segmented_ecg_data['full'+full_mode] = nanArray.tolist()
                            else:
                                segmented_ecg_data['full'+full_mode] = segmented_ecg_data['full'+full_mode] + nanArray.tolist()
                        if(key!='full'+full_mode):
                            if key not in segmented_ecg_data.keys():
                                segmented_ecg_data[key] = nanArray.tolist()
                            else:
                                segmented_ecg_data[key] = segmented_ecg_data[key] + nanArray.tolist()
                    else:
                        shilftedStart = start
                        shilftedStart = start + find_lead_col_position(key, format_4_by_3)*int(rate*lead_length_in_seconds)
                        end = shilftedStart + int(rate*lead_length_in_seconds)
                        
                        if(key!='full'+full_mode):
                            frame[key] = samples_to_volts(record_dict[key][shilftedStart:end],adc[gain_index])
                            frame[key] = center_function(frame[key])
                            
                            nanArray = np.empty((int(shilftedStart - start)))
                            nanArray[:] = np.nan
                            if key not in format_4_by_3[0]:
                                if key not in segmented_ecg_data.keys():
                                    segmented_ecg_data[key] = nanArray.tolist()
                                else:
                                    segmented_ecg_data[key] = segmented_ecg_data[key] + nanArray.tolist()
                            if key not in segmented_ecg_data.keys():
                                segmented_ecg_data[key] = frame[key].tolist()
                            else:
                                segmented_ecg_data[key] = segmented_ecg_data[key] + frame[key].tolist()

                            nanArray = np.empty((int(abs_lead_step*rate - (end - shilftedStart) - (shilftedStart - start))))
                            nanArray[:] = np.nan
                            segmented_ecg_data[key] = segmented_ecg_data[key] + nanArray.tolist()
                        if(full_mode!='None' and key==full_mode):
                            if(len(record_dict[key][start:])>int(rate*10)):
                                frame['full'+full_mode] = samples_to_volts(record_dict[key][start:(start+int(rate)*10)],adc[gain_index])
                                frame['full'+full_mode] = center_function(frame['full'+full_mode])
                                if 'full'+full_mode not in segmented_ecg_data.keys():
                                    segmented_ecg_data['full'+full_mode] = frame['full'+full_mode].tolist()
                                else:
                                    segmented_ecg_data['full'+full_mode] = segmented_ecg_data['full'+full_mode] + frame['full'+full_mode].tolist()
                            else:
                                frame['full'+full_mode] = samples_to_volts(record_dict[key][start:],adc[gain_index])
                                frame['full'+full_mode] = center_function(frame['full'+full_mode])
                                if 'full'+full_mode not in segmented_ecg_data.keys():
                                    segmented_ecg_data['full'+full_mode] = frame['full'+full_mode].tolist()
                                else:
                                    segmented_ecg_data['full'+full_mode] = segmented_ecg_data['full'+full_mode] + frame['full'+full_mode].tolist()
                        gain_index += 1
            if(end_flag==False):
                ecg_frame.append(frame)
                start = start + int(rate*abs_lead_step)
    outfile_array = []
    
    name, ext = os.path.splitext(full_header_file)
    # write_wfdb_file(segmented_ecg_data, name, rate, header_file, output_directory, full_mode_list)

    for i in range(len(ecg_frame)):
        
        # if no leads
        if background_only:
            for k in ecg_frame[i].keys(): ecg_frame[i][k][:] = np.nan
        
        dc = add_dc_pulse.rvs()
        bw = add_bw.rvs()
        grid = show_grid.rvs()
        print_txt = add_print.rvs()

        json_dict = {}
        grid_colour = 'colour'
        if(bw):
            grid_colour = 'bw'

        rec_file = name + '-' + str(i)
        
        print('ecg_plot: ', full_mode_list)
        x_grid,y_grid = ecg_plot(ecg_frame[i],full_header_file=full_header_file, style=grid_colour, sample_rate = rate,columns=columns,rec_file_name = rec_file, output_dir = output_directory, resolution = resolution, pad_inches = pad_inches, lead_index=full_leads, full_mode = full_mode_list, store_text_bbox = store_text_bbox, show_lead_name=add_lead_names,show_dc_pulse=dc,papersize=papersize,show_grid=(grid),standard_colours=standard_colours,bbox=bbox, print_txt=print_txt, leads_only=leads_only)

        rec_head, rec_tail = os.path.split(rec_file)

        json_dict["x_grid"] = x_grid
        json_dict["y_grid"] = y_grid
        if store_text_bbox:
            json_dict["text_bounding_box_file"] = os.path.join(output_directory, 'text_bounding_box', rec_tail + '.txt')
        else:
            json_dict["text_bounding_box_file"] = ""
        if bbox:
            json_dict["lead_bounding_box_file"] = os.path.join(output_directory, 'lead_bounding_box', rec_tail + '.txt')
        else:
            json_dict["lead_bounding_box_file"] = ""

        outfile = os.path.join(output_directory,rec_tail+'.png')
        
        json_object = json.dumps(json_dict, indent=4)
 
        # Writing to sample.json
        if store_configs:
            with open(os.path.join(output_directory,rec_tail+'.json'), "w") as f:
                f.write(json_object)

        outfile_array.append(outfile)

    return outfile_array
