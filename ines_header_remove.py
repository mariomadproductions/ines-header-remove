#!/usr/bin/env python3
import argparse
from pathlib import Path
import shutil

def get_args():
    parser = argparse.ArgumentParser(description='Create .unh equivalents of'\
                                     '.nes files. Processes files in directory '
                                     'if one is specified.')
    parser.add_argument('--recursive', action='store_true')
    parser.add_argument('input_path')
    return parser.parse_args()

def is_rom_headered(file_path):
    file_len = file_path.stat().st_size
    with open(file_path, 'rb') as file:
        first_4_bytes = file.read(0x4)

    if first_4_bytes == b'NES\x1a':
        return True
    else:
        return False

def mk_unheadered_copy(file_path, file_path_unh):
    with open(file_path, 'rb') as input_file,\
         open(file_path_unh, 'xb') as output_file:
        input_file.seek(0x16)
        for chunk in iter(lambda: input_file.read(16384), b''):
            output_file.write(chunk)

def process_dir(input_path, recursive):
    if recursive == True:
        glob_str = '*.nes'
    else:
        glob_str = '**/*.nes'

    for file_path in input_path.glob(glob_str):
        process_file(file_path)

def process_file(file_path):
    file_path_unh = file_path.with_suffix('.unh')
    if is_rom_headered(file_path):
        try:
            mk_unheadered_copy(file_path, file_path_unh)
            print(f'{file_path}: created {file_path_unh}')
        except FileExistsError:
            print(f'{file_path}: unheadered copy already exists at {file_path_unh}')
    else: 
        print(f'{file_path}: already unheadered')

def main():
    args = get_args()
    input_path = Path(args.input_path)

    if input_path.is_dir():
        if args.recursive:
            process_dir(input_path, True)
        else:
            process_dir(input_path, False)
    else:
        if args.recursive:
            print('Only directories can be recursed')
        else:
            process_file(input_path)

if __name__ == '__main__':
    main()
