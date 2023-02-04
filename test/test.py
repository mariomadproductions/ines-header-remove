#!/usr/bin/env python3
import argparse
from pathlib import Path
import subprocess
import logging
from hashlib import sha256
import sys

logging.basicConfig(level=logging.INFO)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('script_path')
    return parser.parse_args()


def get_sha256(file):
    calculated_sha256 = sha256()
    while True:
        data = file.read(65536)
        if not data:
            break
        calculated_sha256.update(data)

    output_sha256 = calculated_sha256.hexdigest()

    return output_sha256

def run_script(script_path, input_file_path):
    logging.info('Running script')
    subprocess.run([script_path, input_file_path], check=True)
    
def check_nes_files(input_file_path, output_file_path, expected_file_attributes):
    logging.info('Checking NES files')  
    
    file_attributes = {
        'input_file': {'size': None,
                       'sha256': None},
        'output_file': {'size': None,
                        'sha256': None}
                        }
    
    file_attributes['input_file']['size'] = input_file_path.stat().st_size
    file_attributes['output_file']['size'] = output_file_path.stat().st_size
    
    with open(input_file_path, 'rb') as input_file, open(output_file_path, 'rb') as output_file:
        file_attributes['input_file']['sha256'] = get_sha256(input_file)
        file_attributes['output_file']['sha256'] = get_sha256(output_file)

    if file_attributes != expected_file_attributes:
        raise ValueError('Expected file attributes don\'t match actual file attributes\n'\
                        f'Expected: {expected_file_attributes}\n'\
                        f'Actual: {file_attributes}')

def remove_output_file(output_file_path):
    logging.info('Removing output file')
    output_file_path.unlink()

def main():
    args = get_args()
    error_raised = False

    input_file_path = Path('rom.nes')
    output_file_path = Path('rom.unh')
    script_path = args.script_path
    expected_file_attributes = {
        'input_file': {'size': 32,
                       'sha256': '2ade7d35c7f4c23b5c687ab291da2af7'\
                                 'ff4e51512c3122cbc670d630a55cbc5d'},
        'output_file': {'size': 16,
                        'sha256': '5ac6a5945f16500911219129984ba8b3'\
                                  '87a06f24fe383ce4e81a73294065461b'},
        }

    run_script(script_path, input_file_path)

    try:
        check_nes_files(input_file_path, output_file_path, expected_file_attributes)
    except ValueError as e:
        logging.error(e)
        error_raised = True

    remove_output_file(output_file_path)
    
    if error_raised == True:
        sys.exit(1)

if __name__ == '__main__':
    main()
