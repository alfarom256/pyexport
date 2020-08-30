import yaml
import argparse
import os
import glob
from stat import *
import pe

CONFIG_FLAT_DIRS = "flat_directories"
CONFIG_SINGLE_FILES = "files"
CONFIG_RECURSIVE_DIRS = "recurse_directories"
DLL_CONST = "*.dll"

def main():

    files_to_load = []

    parser = argparse.ArgumentParser(description="Export parsing!")
    parser.add_argument("-o", dest="output_dir", help="Directory where the export text files will be stored", required=True)
    parser.add_argument("-c", dest="config", help="Use a provided yaml config file", required=False, default=None)
    args = parser.parse_args()

    if not str(args.output_dir).endswith(os.sep):
        args.output_dir += os.sep

    try:
        out_st = os.stat(args.output_dir)
    
        if not S_ISDIR(out_st.st_mode):
            print("Provided destination is not a valid directory!")
            exit(0)

    except FileNotFoundError:
            print("Provided destination is not a valid directory!")
            exit(0)
       

    # parse the provided/default yaml config
    cfg_file = "directories.yaml"
    if args.config is not None:
        cfg_file = args.config
    parsed = parse_cfg(cfg_file)
    file_list = process_cfg(parsed)
    for f in file_list:
        local_fname = f.split(os.sep)[::-1][0]+".exports"
        with open(args.output_dir + local_fname, 'w+') as f_handle:
            print("Writing: " + args.output_dir + local_fname)
            f_handle.write(f + '\n')
            exports = pe.get_exports_from_file(f)
            if exports is None:
                continue
            for e in exports:
                f_handle.write( ' '.join([str(x) for x in e]) + '\n' )
    print("Files written")


def process_cfg(parsed_config):
    file_list = []
    if CONFIG_SINGLE_FILES in parsed_config.keys():
        print("Adding single file: ")
        for f in parsed_config[CONFIG_SINGLE_FILES]:
            print(f)
            file_list.append(f)
    if CONFIG_FLAT_DIRS in parsed_config.keys():
        print("Adding from flat directories...")
        for d in parsed_config[CONFIG_FLAT_DIRS]:
            f_tmp = glob.glob(d+DLL_CONST)
            for f in f_tmp:
                print(f)
                file_list.append(f)
    
    if CONFIG_RECURSIVE_DIRS in parsed_config.keys():
        print("Adding from flat directories...")
        for d in parsed_config[CONFIG_RECURSIVE_DIRS]:
            if(not str(d).strip().endswith(os.sep)):
                d += os.sep
            f_tmp = glob.glob(d+DLL_CONST, recursive=True)
            for f in f_tmp:
                print(f)
                file_list.append(f)
    
    return file_list



def parse_cfg(cfg_file):
    try:
        with open(cfg_file) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except Exception as ex:
        print("Fatal exception parsing config: " + str(ex))
        exit(0)

if __name__ == "__main__":
    main()