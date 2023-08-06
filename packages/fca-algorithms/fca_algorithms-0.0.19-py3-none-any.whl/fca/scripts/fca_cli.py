#!/usr/bin/env python

import os
import argparse
import csv


INVALID_FILETYPE_MSG = "Error: Invalid file format. {} must be a .txt file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path {} does not exist."
MANDATORY_ARGUMENTS_MSG = "Either -c or -k params should be specified"
  
  
def validate_file(file_name):
    '''
    validate file name and path.
    '''
    if not valid_path(file_name):
        print(INVALID_PATH_MSG.format(file_name))
        quit()
    elif not valid_filetype(file_name):
        print(INVALID_FILETYPE_MSG.format(file_name))
        quit()
    return
      
def valid_filetype(file_name):
    # validate file type
    return file_name.endswith('.csv')
  
def valid_path(path):
    # validate file path
    return os.path.exists(path)


def main():
    # create a parser object
    parser = argparse.ArgumentParser(description = "FCA cli")
    
    # add argument
    parser.add_argument("-c", "--context", type=str, nargs='?',
                        metavar="context_name",
                        help="Formal context csv file.")
    
    parser.add_argument("-k", "--contexts", type=str, nargs='*',
                        metavar="context_names",
                        help="Formal contexts csv files from the relational context family.")
    
    parser.add_argument("-r", "--relations", type=str, nargs='*',
                        metavar="relation_file_names",
                        help="Relation csv filename in case of RCA. Name is expected to be r_0_3.csv for example if its a "
                             "relation between objects of the contexts 0 and 3 respectively")
    
    # parse the arguments from standard input
    args = parser.parse_args()

    if args.contexts:
        K, R = parse_rca(args)
        print(f'### RCA parsed {K}, {R}')
    elif args.context:
        K = parse_fca(args)
        print(f'### FCA parsed {K}')
    else:
        print(MANDATORY_ARGUMENTS_MSG)
        exit(1)


def parse_rca(args):
    contexts = []
    for ctx_name in args.contexts:
        contexts.append(import_context(ctx_name))
    
    relations = []
    for relation_name in args.relations:
        relations.append(import_relation(relation_name, contexts))
    
    return contexts, relations


def parse_fca(args):
    return import_context(args.context)


def import_context(filename):
    O = []
    A = []
    I = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        loading_attributes = True
        for row in reader:
            if loading_attributes:
                for attr in row[1:]:
                    A.append(attr)
                loading_attributes = False
            else:
                O.append(row[0])
                I.append([])
                for attr_i in row[1:]:
                    I.append(len(attr_i) != 0)
    return O, A, I


def import_relation(filename, contexts):
    contexts_indexes = [int(idx) for idx in filename.split('_')[1:]]
    R = dimension(contexts, contexts_indexes, 0)
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            to_process = len(row) - 1
            current = R[0]
            while to_process > 0:
                i = len(row) - to_process
                current = current[int(row[i])]
                to_process -= 1
            current.add(int(row[-1]))  # this should be a set
    return R
            

def dimension(contexts, contexts_indexes, i):
    if i == len(contexts_indexes[i].O) - 1:
        return set()
    return [dimension(contexts, contexts_indexes, i+1) for _ in range(len(contexts_indexes[i].O))]


if __name__ == "__main__":
    main()
