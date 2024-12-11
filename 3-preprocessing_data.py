#!/usr/bin/env python3

import argparse
from pathlib import Path
import subprocess

from common import HEIC2HEVCRunner
from parameters import single_iterator, second_iterator, get_single_file_name, get_second_file_name, get_single_265_name, get_second_265_name, get_single_265_name2, get_second_265_name2, get_single_265_data, get_second_265_data, get_single_265_data_L, get_second_265_data_L, get_single_265_data_C, get_second_265_data_C, get_single_265_data_D, get_second_265_data_D, get_single_265_data_P, get_second_265_data_P, get_single_265, get_second_265, get_single_combined_data, get_second_combined_data, get_single_265_data_Q, get_second_265_data_Q

from parameters import (single_iterator, second_iterator, triple_iterator, 
                        get_single_file_name, get_second_file_name, get_triple_file_name, 
                        get_single_265_name, get_second_265_name, get_triple_265_name, 
                        get_single_265_name2, get_second_265_name2, get_triple_265_name2, 
                        get_single_265_data, get_second_265_data, get_triple_265_data, 
                        get_single_265_data_L, get_second_265_data_L, get_triple_265_data_L, 
                        get_single_265_data_C, get_second_265_data_C, get_triple_265_data_C, 
                        get_single_265_data_D, get_second_265_data_D, get_triple_265_data_D, 
                        get_single_265_data_P, get_second_265_data_P, get_triple_265_data_P, 
                        get_single_265, get_second_265, get_triple_265,
                        get_single_combined_data, get_second_combined_data, get_triple_combined_data,
                        get_single_265_data_Q, get_second_265_data_Q, get_triple_265_data_Q)

import tempfile
import shutil
import numpy as np
import csv
import pandas as pd
import re

def get_parser():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-heic', '--heic2hevc-path', type=Path, default='.')
    parser.add_argument('-i', '--input-path', type=Path, default='.')
    parser.add_argument('-o', '--output-path', type=Path, default='.')
    
    subparsers = parser.add_subparsers(title='command', dest='command', required=True)

    run_single_parser = subparsers.add_parser('run-single')
    run_single_parser.add_argument('index', type=int)
    
    run_second_parser = subparsers.add_parser('run-second')
    run_second_parser.add_argument('index', type=int)
    
    run_second_parser = subparsers.add_parser('run-triple')
    run_second_parser.add_argument('index', type=int)

    return parser


def main(args):

    if args.command == 'run-single':
        all_params = list(single_iterator())
        file_name, QP1, CTU, PRESET = all_params[args.index]

        input_file_name = get_single_265_data(file_name, QP1, CTU, PRESET)
        input_path = args.input_path / input_file_name

        output_file_name = get_single_combined_data(file_name, QP1, CTU, PRESET)
        output_path = args.output_path / output_file_name
                
        # read .npz file
        data = np.load(input_path)
        depth_data = data['depth']
        pu_data = data['pu']
        luminance_data = data['luminance']
        chroma_data = data['chroma']
        qp_data = data['qp']
        
        # count data for luminance and chroma
        depth_counts = np.bincount(depth_data)
        pu_counts = np.bincount(pu_data)
        luminance_counts = np.bincount(luminance_data)
        chroma_counts = np.bincount(chroma_data)
        qp_counts = np.bincount(qp_data)
        
        # extend the luminance_counts to 51
        depth_counts_extended = np.zeros(52, dtype=int)
        depth_counts_extended[:len(depth_counts)] = depth_counts
        
        pu_counts_extended = np.zeros(52, dtype=int)
        pu_counts_extended[:len(pu_counts)] = pu_counts
        
        luminance_counts_extended = np.zeros(52, dtype=int)
        luminance_counts_extended[:len(luminance_counts)] = luminance_counts
        
        chroma_counts_extended = np.zeros(52, dtype=int)
        chroma_counts_extended[:len(chroma_counts)] = chroma_counts
        
        # convert the data and counts to DataFrame
        depth_df = pd.DataFrame({'depth_value': np.arange(len(depth_counts_extended)), 'depth_counts': depth_counts_extended})
        pu_df = pd.DataFrame({'pu_value': np.arange(len(pu_counts_extended)), 'pu_counts': pu_counts_extended})
        luminance_df = pd.DataFrame({'luminance_value': np.arange(len(luminance_counts_extended)), 'luminance_counts': luminance_counts_extended})
        chroma_df = pd.DataFrame({'chroma_value': np.arange(len(chroma_counts_extended)), 'chroma_counts': chroma_counts_extended})
        qp_df = pd.DataFrame({'qp_value': np.arange(len(qp_counts)), 'qp_counts': qp_counts})

        # merge 2 DataFrames into single DataFrame
        combined_df = pd.concat([depth_df[['depth_value', 'depth_counts']],
                                 pu_df[['pu_value', 'pu_counts']],
                                 luminance_df[['luminance_value', 'luminance_counts']], 
                                 chroma_df[['chroma_value','chroma_counts']], 
                                 qp_df[['qp_value','qp_counts']]], axis=1)
        
        # write the DataFrame to csv
        # combined_csv_file_name = f'{extracted_name}.csv'
        combined_df.to_csv(output_path, index=False)

        print('Done')


    elif args.command == 'run-second':
        all_params = list(second_iterator())
        file_name, QP1, QP2, CTU, PRESET = all_params[args.index]
        
        input_file_name = get_second_265_data(file_name, QP1, QP2, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
                
        output_file_name = get_second_combined_data(file_name, QP1, QP2, CTU, PRESET)
        output_path = args.output_path / output_file_name

        # read .npz file
        data = np.load(input_path)
        depth_data = data['depth']
        pu_data = data['pu']
        luminance_data = data['luminance']
        chroma_data = data['chroma']
        qp_data = data['qp']

        # count data for luminance and chroma
        depth_counts = np.bincount(depth_data)
        pu_counts = np.bincount(pu_data)
        luminance_counts = np.bincount(luminance_data)
        chroma_counts = np.bincount(chroma_data)
        qp_counts = np.bincount(qp_data)

        # extend the luminance_counts to 36
        depth_counts_extended = np.zeros(52, dtype=int)
        depth_counts_extended[:len(depth_counts)] = depth_counts

        pu_counts_extended = np.zeros(52, dtype=int)
        pu_counts_extended[:len(pu_counts)] = pu_counts

        luminance_counts_extended = np.zeros(52, dtype=int)
        luminance_counts_extended[:len(luminance_counts)] = luminance_counts

        chroma_counts_extended = np.zeros(52, dtype=int)
        chroma_counts_extended[:len(chroma_counts)] = chroma_counts

        # convert the data and counts to DataFrame            
        depth_df = pd.DataFrame({'depth_value': np.arange(len(depth_counts_extended)), 'depth_counts': depth_counts_extended})
        pu_df = pd.DataFrame({'pu_value': np.arange(len(pu_counts_extended)), 'pu_counts': pu_counts_extended})
        luminance_df = pd.DataFrame({'luminance_value': np.arange(len(luminance_counts_extended)), 'luminance_counts': luminance_counts_extended})
        chroma_df = pd.DataFrame({'chroma_value': np.arange(len(chroma_counts_extended)), 'chroma_counts': chroma_counts_extended})
        qp_df = pd.DataFrame({'qp_value': np.arange(len(qp_counts)), 'qp_counts': qp_counts})

        # merge 2 DataFrames into single DataFrame
        combined_df = pd.concat([depth_df[['depth_value', 'depth_counts']],
                                 pu_df[['pu_value', 'pu_counts']],
                                 luminance_df[['luminance_value', 'luminance_counts']], 
                                 chroma_df[['chroma_value','chroma_counts']], 
                                 qp_df[['qp_value','qp_counts']]], axis=1)

        # write the DataFrame to csv
        # combined_csv_file_name = f'{extracted_name}.csv'
        combined_df.to_csv(output_path, index=False)

        print('Done')

        
        
        
#         if QP1 == QP2:
#             output_file_name = get_second_combined_data(file_name, QP1, QP2, CTU, PRESET)
#             output_path = args.output_path / output_file_name
            
#             # read .npz file
#             data = np.load(input_path)
#             depth_data = data['depth']
#             pu_data = data['pu']
#             luminance_data = data['luminance']
#             chroma_data = data['chroma']
#             qp_data = data['qp']
        
#             # count data for luminance and chroma
#             depth_counts = np.bincount(depth_data)
#             pu_counts = np.bincount(pu_data)
#             luminance_counts = np.bincount(luminance_data)
#             chroma_counts = np.bincount(chroma_data)
#             qp_counts = np.bincount(qp_data)
        
#             # extend the luminance_counts to 36
#             depth_counts_extended = np.zeros(52, dtype=int)
#             depth_counts_extended[:len(depth_counts)] = depth_counts
        
#             pu_counts_extended = np.zeros(52, dtype=int)
#             pu_counts_extended[:len(pu_counts)] = pu_counts
        
#             luminance_counts_extended = np.zeros(52, dtype=int)
#             luminance_counts_extended[:len(luminance_counts)] = luminance_counts
        
#             chroma_counts_extended = np.zeros(52, dtype=int)
#             chroma_counts_extended[:len(chroma_counts)] = chroma_counts
            
#             # convert the data and counts to DataFrame            
#             depth_df = pd.DataFrame({'depth_value': np.arange(len(depth_counts_extended)), 'depth_counts': depth_counts_extended})
#             pu_df = pd.DataFrame({'pu_value': np.arange(len(pu_counts_extended)), 'pu_counts': pu_counts_extended})
#             luminance_df = pd.DataFrame({'luminance_value': np.arange(len(luminance_counts_extended)), 'luminance_counts': luminance_counts_extended})
#             chroma_df = pd.DataFrame({'chroma_value': np.arange(len(chroma_counts_extended)), 'chroma_counts': chroma_counts_extended})
#             qp_df = pd.DataFrame({'qp_value': np.arange(len(qp_counts)), 'qp_counts': qp_counts})

#             # merge 2 DataFrames into single DataFrame
#             combined_df = pd.concat([depth_df[['depth_value', 'depth_counts']],
#                                      pu_df[['pu_value', 'pu_counts']],
#                                      luminance_df[['luminance_value', 'luminance_counts']], 
#                                      chroma_df[['chroma_value','chroma_counts']], 
#                                      qp_df[['qp_value','qp_counts']]], axis=1)
        
#             # write the DataFrame to csv
#             # combined_csv_file_name = f'{extracted_name}.csv'
#             combined_df.to_csv(output_path, index=False)

#             print('Done')
                
#         else:
#             print("skip")
    
            
    elif args.command == 'run-triple':
        all_params = list(triple_iterator())
        file_name, QP1, QP2, QP3, CTU, PRESET = all_params[args.index]
        
        input_file_name = get_triple_265_data(file_name, QP1, QP2, QP3, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
        
        if QP1 < QP2:
            output_file_name = get_triple_combined_data(file_name, QP1, QP2, QP3, CTU, PRESET)
            output_path = args.output_path / output_file_name
            
            # read .npz file
            data = np.load(input_path)
            depth_data = data['depth']
            pu_data = data['pu']
            luminance_data = data['luminance']
            chroma_data = data['chroma']
            qp_data = data['qp']
        
            # count data for luminance and chroma
            depth_counts = np.bincount(depth_data)
            pu_counts = np.bincount(pu_data)
            luminance_counts = np.bincount(luminance_data)
            chroma_counts = np.bincount(chroma_data)
            qp_counts = np.bincount(qp_data)
        
            # extend the luminance_counts to 36
            depth_counts_extended = np.zeros(52, dtype=int)
            depth_counts_extended[:len(depth_counts)] = depth_counts
        
            pu_counts_extended = np.zeros(52, dtype=int)
            pu_counts_extended[:len(pu_counts)] = pu_counts
        
            luminance_counts_extended = np.zeros(52, dtype=int)
            luminance_counts_extended[:len(luminance_counts)] = luminance_counts
        
            chroma_counts_extended = np.zeros(52, dtype=int)
            chroma_counts_extended[:len(chroma_counts)] = chroma_counts
            
            # convert the data and counts to DataFrame            
            depth_df = pd.DataFrame({'depth_value': np.arange(len(depth_counts_extended)), 'depth_counts': depth_counts_extended})
            pu_df = pd.DataFrame({'pu_value': np.arange(len(pu_counts_extended)), 'pu_counts': pu_counts_extended})
            luminance_df = pd.DataFrame({'luminance_value': np.arange(len(luminance_counts_extended)), 'luminance_counts': luminance_counts_extended})
            chroma_df = pd.DataFrame({'chroma_value': np.arange(len(chroma_counts_extended)), 'chroma_counts': chroma_counts_extended})
            qp_df = pd.DataFrame({'qp_value': np.arange(len(qp_counts)), 'qp_counts': qp_counts})

            # merge 2 DataFrames into single DataFrame
            combined_df = pd.concat([depth_df[['depth_value', 'depth_counts']],
                                     pu_df[['pu_value', 'pu_counts']],
                                     luminance_df[['luminance_value', 'luminance_counts']], 
                                     chroma_df[['chroma_value','chroma_counts']], 
                                     qp_df[['qp_value','qp_counts']]], axis=1)
        
            # write the DataFrame to csv
            # combined_csv_file_name = f'{extracted_name}.csv'
            combined_df.to_csv(output_path, index=False)

            print('Done')
            
            
        else:
            print("skip")
            

if __name__ == '__main__':
    parser = get_parser()
    main(parser.parse_args())
