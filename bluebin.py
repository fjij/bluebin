#!/usr/bin/python3.7

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# bluebin.py                                                                  #
#                                                                             #
# Will Harris 2020                                                            #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import os
import re

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
    return re.search(r'^( {0,3}\[(\w| )*\] *)$', line) is not None

def lid_name(line):
    return line.strip()[1:-1].strip()

def create_component(name):
    return {'name': name, 'properties': {}, 'content': ''}

def is_property(line):
    return re.search(r'^((\w| )*(\s)*:.*)', line) is not None

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

def csub_name(csub):
    return csub.group(1).split(']')[0][1:].strip()

def csub_args(csub):
    if csub.group(3) is None:
        return None, None
    full_str = csub.group(3).strip()[1:-1] + ','
    arg_strs = []
    start = 0
    in_qts = False
    for x in range(len(full_str)):
        c = full_str[x] 
        if c == '"':
            in_qts = not in_qts
        if not in_qts and c == ',':
            arg_strs.append(full_str[start:x])
            start = x + 1
    pos_args = []
    kw_args = {}
    for arg_str in arg_strs:
        in_qts = False
        kw_arg = False
        name = ''
        value = arg_str.strip()
        for x in range(len(arg_str)):
            c = arg_str[x] 
            if c == '"':
                in_qts = not in_qts
            if not in_qts and c == ':':
                kw_arg = True
                name = arg_str[:x].strip()
                value = arg_str[x+1:].strip()
                break
        if '"' in value:
            value = value[1:-1]
        if kw_arg:
            kw_args[name] = value
        else:
            pos_args.append(value)
    return pos_args, kw_args

def find_component(name, components):
    for x in range(len(components)):
        if components[x]['name'] == name:
            return components[x], components[x+1:]
    return None, None

def replace_csubs(line, other_components):
    start_at = 0
    while True:
        csub = re.search(r'%(\[(\w| )*\](\s*\(\s*(((\w| )*:){0,1}\s*(".*"|(\w| )*))(\s*,\s*(((\w| )*:){0,1}\s*(".*"|(\w| )*)))*\s*\)){0,1})', line[start_at:])
        if csub is None:
            break
        a, b = csub.span()
        a += start_at
        b += start_at
        c, c_nexts = find_component(csub_name(csub), other_components)
        if c is not None:
            pos_args, kw_args = csub_args(csub)
            print(pos_args, kw_args)
            content = render_component(c, c_nexts)
            line = line[:a] + content + line [b:]
        start_at = b
    return line

def render_line(line, component, other_components):
    if is_code(line):
        return line
    line = replace_csubs(line, other_components)
    return line

def render_component(component, other_components):
    return '\n'.join(list(render_line(line, component, other_components) for line in component['content'].splitlines()))
    

def bluebin(in_str):
    components = identify_components(in_str)
    print(components)
    print(render_component(components[0], components[1:]))

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


