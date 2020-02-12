#!/usr/bin/python3.7

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# bluebin.py                                                                  #
#                                                                             #
# Will Harris 2020                                                            #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Classes                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class InvalidArgumentException(Exception):
    pass

class IncorrectArgumentCountException(Exception):
    pass
        

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Functions                                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def parse_args():
    if len(sys.argv) < 3:
        raise IncorrectArgumentCountException('Too few arguments were provided!')
    elif len(sys.argv) > 3:
        raise IncorrectArgumentCountException('Too many arguments were provided!')
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if not os.path.isfile(input_file):
        raise InvalidArgumentException('The input file provided does not exist!')
    return input_file, output_file

def show_help():
    print('\nUsage: python3 bluebin.py [INPUT FILE] [OUTPUT FILE]\n')

def is_code(line):
    return line.startswith('    ') or line.startswith('\t')

def is_lid(line):
    return not is_code(line) and line.strip().startswith('[') and line.strip().endswith(']')

def lid_name(line):
    return line[1:-1].strip()

def create_component(name):
    return {'name': name, 'properties': {}, 'content': ''}

def is_property(line):
    prev = ''
    for c in line:
        if c == ':' and prev != '\\':
            return True
    return False

def parse_property(line):
    return list(map(lambda s: s.strip(), line.split(':', 1)))

def identify_components(in_str):
    components = [create_component('__root__')]
    reading_properties = False
    for line in in_str.splitlines():
        if is_lid(line):
            components.append(create_component(lid_name(line)))
            reading_properties = True
        elif reading_properties and is_property(line):
            key, value = parse_property(line)
            components[-1]['properties'][key] = value
        elif line.strip() == '':
            reading_properties = False
        else:
            reading_properties = False
            components[-1]['content'] += line + '\n'
    return components

def bluebin(in_str):
    components = identify_components(in_str)
    print(components)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Main                                                                        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':
    try:
        input_file, output_file = parse_args()
        with open(input_file, 'r') as f:
            bluebin(f.read())
    except Exception as e:
        print('\nERROR: ' + str(e))
        show_help()


