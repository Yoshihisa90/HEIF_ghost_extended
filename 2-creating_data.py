#!/usr/bin/env python3

import argparse
from pathlib import Path
import subprocess
import numpy as np
from common import TAppDecRunner
from tempfile import TemporaryDirectory
import shutil
import os
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
                        get_single_265_data_Q, get_second_265_data_Q, get_triple_265_data_Q)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tappdec-path', type=Path, default='.')
    parser.add_argument('-i', '--input-path', type=Path, default='.')
    parser.add_argument('-o', '--output-path', type=Path, default='.')
    
    subparsers = parser.add_subparsers(title='command', dest='command', required=True)

    run_single_parser = subparsers.add_parser('run-single')
    run_single_parser.add_argument('index', type=int)
    
    run_second_parser = subparsers.add_parser('run-second')
    run_second_parser.add_argument('index', type=int)
    
    run_triple_parser = subparsers.add_parser('run-triple')
    run_triple_parser.add_argument('index', type=int)

    return parser


def run_heic2hevc(args, params, input_path, input_path2):
    heic2hevc = TAppDecRunner(args.tappdec_path)

    with TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        
        if args.command == 'run-single':
            temp_path = temp_dir / get_single_265(*params)
            
            if os.path.exists(input_path):
                heic2hevc.run(input_path, temp_path)
                map_names = {
                'depth': get_single_265_data_D(*params),
                'pu': get_single_265_data_P(*params),
                'luminance': get_single_265_data_L(*params),
                'chroma': get_single_265_data_C(*params),
                'qp': get_single_265_data_Q(*params),
                }
            
            else:
                heic2hevc.run(input_path2, temp_path)
                map_names = {
                'depth': get_single_265_data_D(*params),
                'pu': get_single_265_data_P(*params),
                'luminance': get_single_265_data_L(*params),
                'chroma': get_single_265_data_C(*params),
                'qp': get_single_265_data_Q(*params),
                }

            results = {}
            for map_name, file_name in map_names.items():
                with (temp_dir/file_name).open('rb') as stream:
 
                    data = np.fromfile(stream, np.uint8)
                    results[map_name] = data
                    
            output_path = args.output_path / get_single_265_data(*params)
            with output_path.open('wb') as stream:
                np.savez_compressed(stream, **results)
        
        elif args.command == 'run-second':
            temp_path = temp_dir / get_second_265(*params)
            
            
            if os.path.exists(input_path):
                heic2hevc.run(input_path, temp_path)
                map_names = {
                'depth': get_second_265_data_D(*params),
                'pu': get_second_265_data_P(*params), 
                'luminance': get_second_265_data_L(*params),
                'chroma': get_second_265_data_C(*params),
                'qp': get_second_265_data_Q(*params),
                }
            else:
                heic2hevc.run(input_path2, temp_path)
                map_names = {
                'depth': get_second_265_data_D(*params),
                'pu': get_second_265_data_P(*params),
                'luminance': get_second_265_data_L(*params),
                'chroma': get_second_265_data_C(*params),
                'qp': get_second_265_data_Q(*params),
                }

            results = {}

            for map_name, file_name in map_names.items():
                with (temp_dir/file_name).open('rb') as stream:
                    data = np.fromfile(stream, np.uint8)
                    results[map_name] = data

            output_path = args.output_path / get_second_265_data(*params)
            with output_path.open('wb') as stream:
                np.savez_compressed(stream, **results)
            
            if params[1] < params[2]:
                if os.path.exists(input_path):
                    heic2hevc.run(input_path, temp_path)
                    map_names = {
                    'depth': get_second_265_data_D(*params),
                    'pu': get_second_265_data_P(*params), 
                    'luminance': get_second_265_data_L(*params),
                    'chroma': get_second_265_data_C(*params),
                    'qp': get_second_265_data_Q(*params),
                    }
                else:
                    heic2hevc.run(input_path2, temp_path)
                    map_names = {
                    'depth': get_second_265_data_D(*params),
                    'pu': get_second_265_data_P(*params),
                    'luminance': get_second_265_data_L(*params),
                    'chroma': get_second_265_data_C(*params),
                    'qp': get_second_265_data_Q(*params),
                    }

                results = {}

                for map_name, file_name in map_names.items():
                    with (temp_dir/file_name).open('rb') as stream:
                        data = np.fromfile(stream, np.uint8)
                        results[map_name] = data

                output_path = args.output_path / get_second_265_data(*params)
                with output_path.open('wb') as stream:
                    np.savez_compressed(stream, **results)
                    
        elif args.command == 'run-triple':
            temp_path = temp_dir / get_triple_265(*params)
            # print("temp_path:", temp_path)
            
            if params[1] < params[2] == params[3]:
                if os.path.exists(input_path):
                    heic2hevc.run(input_path, temp_path)
                    map_names = {
                    'depth': get_triple_265_data_D(*params),
                    'pu': get_triple_265_data_P(*params), 
                    'luminance': get_triple_265_data_L(*params),
                    'chroma': get_triple_265_data_C(*params),
                    'qp': get_triple_265_data_Q(*params),
                    }
                else:
                    heic2hevc.run(input_path2, temp_path)
                    map_names = {
                    'depth': get_triple_265_data_D(*params),
                    'pu': get_triple_265_data_P(*params),
                    'luminance': get_triple_265_data_L(*params),
                    'chroma': get_triple_265_data_C(*params),
                    'qp': get_triple_265_data_Q(*params),
                    }

                results = {}

                for map_name, file_name in map_names.items():
                    with (temp_dir/file_name).open('rb') as stream:
                        data = np.fromfile(stream, np.uint8)
                        results[map_name] = data

                output_path = args.output_path / get_triple_265_data(*params)
                with output_path.open('wb') as stream:
                    np.savez_compressed(stream, **results)


def main(args):

    if args.command == 'run-single':
        all_params = list(single_iterator())
        # file_name, QP1, CTU, PRESET = all_params[args.index]
        params = all_params[args.index]

        # input_file_name = get_single_265_name(file_name, QP1, CTU, PRESET)
        input_file_name = get_single_265_name(*params)
        input_path = args.input_path / input_file_name
        
        # input_file_name2 = get_single_265_name2(file_name, QP1, CTU, PRESET)
        input_file_name2 = get_single_265_name2(*params)
        input_path2 = args.input_path / input_file_name2
        
        run_heic2hevc(args, params, input_path, input_path2)
           
        # output_file_name = get_single_265_data(file_name, QP1, CTU, PRESET)
        # output_path = args.output_path / output_file_name
        # heic2hevc = TAppDecRunner(args.tappdec_path)
        # heic2hevc.run(input_path, output_path)
        # heic2hevc.run(input_path2, output_path)
        
        
    elif args.command == 'run-second':
        all_params = list(second_iterator())
        # file_name, QP1, QP2, CTU, PRESET = all_params[args.index]
        params = all_params[args.index]
        
        # input_file_name = get_second_265_name(file_name, QP1, QP2, CTU, PRESET)
        input_file_name = get_second_265_name(*params)
        input_path = args.input_path / input_file_name
        
        # input_file_name2 = get_second_265_name2(file_name, QP1, QP2, CTU, PRESET)
        input_file_name2 = get_second_265_name2(*params)
        input_path2 = args.input_path / input_file_name2
        
        run_heic2hevc(args, params, input_path, input_path2)


    elif args.command == 'run-triple':
        all_params = list(triple_iterator())
        # file_name, QP1, QP2, CTU, PRESET = all_params[args.index]
        params = all_params[args.index]
        
        # input_file_name = get_second_265_name(file_name, QP1, QP2, CTU, PRESET)
        input_file_name = get_triple_265_name(*params)
        input_path = args.input_path / input_file_name
        
        # input_file_name2 = get_second_265_name2(file_name, QP1, QP2, CTU, PRESET)
        input_file_name2 = get_triple_265_name2(*params)
        input_path2 = args.input_path / input_file_name2
        
        run_heic2hevc(args, params, input_path, input_path2)
            

if __name__ == '__main__':
    parser = get_parser()
    main(parser.parse_args())
