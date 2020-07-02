#!/usr/bin/env python

'''
Performs regular expression substition via pattern searching and matching. The text is then replaced with input either
an input string, or strings read from an existing file.
'''

# Import packages/modules
import re
import os
import sys

# Import packages/modules for argument parsing
import argparse

# Define functions

def read_file(file):
    '''
    Opens the (text) file, reads its contents, and stores those contents in a list of strings. Should the input
    file not exist, then the text is assumed to be a string and is returned instead.

    Arguments:
        file (str, file): Input file or string
    Returns:
        lines (list): List of strings of the file contents
    '''

    if os.path.exists(file) and os.path.isfile(file):
        with open(file, "r") as file:
            lines = file.readlines()
            file.close()
    elif os.path.exists(file) and os.path.isdir(file):
        lines = file
    else:
        lines = file
    return lines


def regex_replace(pattern, file, repl_list):
    '''
    Uses input pattern for a regEx search. If the pattern is matched in the
    input file, the pattern is replaced with the contents in the 'replace list'
    (repl_list) argument.

    Arguments:
        pattern (str): Pattern to be searched and matched
        file (file): Input file that is read and searched
        repl_list (list): List of contents that replaces matched pattern
    Returns:
        new_lines (list): New list of file contents that has replaced the regEx matched pattern
    '''

    regexp = re.compile(f"{pattern}")
    new_lines = list()
    with open(file, "r") as f:
        for line in f:
            match = regexp.match(line)
            if match:
                new_lines.extend(repl_list)
            else:
                new_lines.append(line)
        f.close()
    return new_lines


def write_file(out_file, text_list):
    '''
    Writes output file provided the file contents as a list, and some output file.

    N.B.: Output file is overwritten should it already exist.

    Arguments:
        out_file (file): Output file name and path.
        text_list (list): File contents stored as a list.
    Returns:
        out_file (file): Written output file.
    '''

    with open(out_file, "w") as file:
        file.writelines(text_list)
        file.close()
    return out_file


def reg_ex_sub(in_file, info_file, pattern, out_file):
    '''
    REgular EXpression SUBstitution is performed via a regEx search, match, and substituion of text from some other
    file.

    Arguments:
        in_file (file): Input file to be searched
        info_file (file): File that contains text to replace pattern matched regEx
        pattern (str): Pattern to be searched and matched
        out_file (file): Output file to be written to
    Returns:
        out_file (file): Output file with text from info_file replacing the matched pattern in in_file
    '''

    info = read_file(file=info_file)
    line_sub = regex_replace(pattern=pattern, file=in_file, repl_list=info)
    out_file = write_file(out_file=out_file, text_list=line_sub)
    return out_file


def reg_ex_file(file, out_file, list_1, list_2):
    '''
    REgular EXpression FILE is a wrapper function for REgular EXpression SUBstitution.

    N.B.: list_1 and list_2 must be the same length. Otherwise, this functions throughs an error.

    Arguments:
        file (file): Input file to be searched
        out_file (file): Output file to be written to
        list_1 (list): List of patterns to be matched
        list_2 (list): List of file paths to files that contain text to replace matched patterns.
    Returns:
        out_file (file): Output file with text from info_file replacing the matched pattern in file
    '''

    if len(list_1) == len(list_2) and len(list_1) > 1:
        for i, idx in enumerate(list_1):
            pattern = list_1[i]
            info_file = list_2[i]
            # out_tmp = out_file[:-4] + ".tmp.txt"
            out_tmp = out_file
            if i == 0:
                out_tmp = reg_ex_sub(in_file=file, info_file=info_file, pattern=pattern, out_file=out_tmp)
            elif i != len(list_1):
                out_tmp = reg_ex_sub(in_file=out_tmp, info_file=info_file, pattern=pattern, out_file=out_tmp)
            elif i == len(list_1):
                out_file = reg_ex_sub(in_file=out_tmp, info_file=info_file, pattern=pattern, out_file=out_file)
                # os.remove(out_tmp)
    elif len(list_1) == len(list_2) and len(list_1) == 1:
        out_file = reg_ex_sub(in_file=file, info_file=list_2[0], pattern=list_1[0], out_file=out_file)
    elif len(list_1) != len(list_2):
        print("")
        print("The number of paired inputs must match. Exiting.")
        print("")
        sys.exit(1)
    return out_file

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="Performs regular expression substition via pattern searching and matching. \
                                                The text is then replaced with input either an input string, or strings read \
                                                from an existing file. The command line options specified here are repeatable, \
                                                and also must be  matched (i.e. the first input must match the first pattern specified).")

    # Parse Arguments
    # Required Arguments
    reqoptions = parser.add_argument_group('Required arguments')
    reqoptions.add_argument('-f', '-file', '--file',
                            type=str,
                            dest="file",
                            metavar="FILE",
                            required=True,
                            help="Input file to be searched.")
    reqoptions.add_argument('-o', '-out', '--output-file',
                            type=str,
                            dest="out",
                            metavar="FILE",
                            required=True,
                            help="Output file to be written.")
    reqoptions.add_argument('-p', '--pattern',
                            type=str,
                            dest="pattern",
                            metavar="STR",
                            required=True,
                            action='append',
                            # nargs='+',
                            help="String/pattern to be searched for in the input file. NOTE: does not work well for non-isolated strings. Use bash's sed for such cases.")
    reqoptions.add_argument('-r', '--replace',
                            type=str,
                            dest="replace",
                            metavar="STR or FILE",
                            required=True,
                            action='append',
                            # nargs='+',
                            help="String or file containing strings used to replace matched pattern in the input file.")

    args = parser.parse_args()

    # Print help message in the case
    # of no arguments
    try:
        args = parser.parse_args()
    except SystemExit as err:
        if err.code == 2:
            parser.print_help()

    # print(args)
    args.out = reg_ex_file(file=args.file, out_file=args.out, list_1=args.pattern, list_2=args.replace)