#!/usr/bin/env python3

import argparse
from pathlib import Path
import subprocess
from common import HEIC2HEVCRunner
from parameters import single_iterator, second_iterator, triple_iterator, get_single_file_name, get_second_file_name, get_triple_file_name, get_single_265_name, get_second_265_name, get_triple_265_name, get_single_csv_name, get_second_csv_name, get_triple_csv_name

import tempfile
import shutil

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-heic', '--heic2hevc-path', type=Path, default='.')
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


def main(args):

    if args.command == 'run-single':
        all_params = list(single_iterator())
        file_name, QP1, CTU, PRESET = all_params[args.index]

        input_file_name = get_single_file_name(file_name, QP1, CTU, PRESET)
        input_path = args.input_path / input_file_name

        output_file_name = get_single_265_name(file_name, QP1, CTU, PRESET)
        output_csv_name = get_single_csv_name(file_name, QP1, CTU, PRESET)
        output_path = args.output_path / output_file_name
        output_csv_path = args.output_path / output_csv_name

        heic2hevc = HEIC2HEVCRunner(args.heic2hevc_path)
        # frequency = EXTRACT_Frequency(args.heic2hevc_path)
        heic2hevc.run(input_path, output_path)
        # frequency.run(input_path, output_csv_path)
        
        
    elif args.command == 'run-second':
        all_params = list(second_iterator())
        file_name, QP1, QP2, CTU, PRESET = all_params[args.index]
        
        input_file_name = get_second_file_name(file_name, QP1, QP2, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
        output_file_name = get_second_265_name(file_name, QP1, QP2, CTU, PRESET)
        output_csv_name = get_second_csv_name(file_name, QP1, QP2, CTU, PRESET)
        output_path = args.output_path / output_file_name
        output_csv_path = args.output_path / output_csv_name

        heic2hevc = HEIC2HEVCRunner(args.heic2hevc_path)
        #frequency = EXTRACT_Frequency(args.heic2hevc_path)
        heic2hevc.run(input_path, output_path)
        #frequency.run(input_path, output_csv_path)
        
        if QP1 < QP2:
            output_file_name = get_second_265_name(file_name, QP1, QP2, CTU, PRESET)
            output_csv_name = get_second_csv_name(file_name, QP1, QP2, CTU, PRESET)
            output_path = args.output_path / output_file_name
            output_csv_path = args.output_path / output_csv_name

            heic2hevc = HEIC2HEVCRunner(args.heic2hevc_path)
            #frequency = EXTRACT_Frequency(args.heic2hevc_path)
            heic2hevc.run(input_path, output_path)
            #frequency.run(input_path, output_csv_path)
            
        else:
            print("skip")
            
            
    elif args.command == 'run-triple':
        all_params = list(triple_iterator())
        file_name, QP1, QP2, QP3, CTU, PRESET = all_params[args.index]
        
        input_file_name = get_triple_file_name(file_name, QP1, QP2, QP3, CTU, PRESET)
        input_path = args.input_path / input_file_name
        
        
        if QP1 < QP2 == QP3:
            output_file_name = get_triple_265_name(file_name, QP1, QP2, QP3, CTU, PRESET)
            output_csv_name = get_triple_csv_name(file_name, QP1, QP2, QP3, CTU, PRESET)
            output_path = args.output_path / output_file_name
            output_csv_path = args.output_path / output_csv_name

            heic2hevc = HEIC2HEVCRunner(args.heic2hevc_path)
            #frequency = EXTRACT_Frequency(args.heic2hevc_path)
            heic2hevc.run(input_path, output_path)
            #frequency.run(input_path, output_csv_path)
            
        else:
            print("skip")
            

if __name__ == '__main__':
    parser = get_parser()
    main(parser.parse_args())
