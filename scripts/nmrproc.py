########################################################
#
# Script to apply standard processing functions to NMR
# data. Follows similar conventions to NMRPipe. Refer 
# to README for specific instructions on how to use file 
# to process data.
#
# AJ Adkins, June 2021
# Skidmore Computational Biophysics Lab
########################################################

import sys
import os
import argparse
import nmrglue as ng

def proc_from_params(in_file, out_file, param_file):
    dic, data = ng.pipe.read(in_file)
    procprm_file = open(str(param_file))  # Reads in the nmr processing parameter file
    lines = [line for line in procprm_file.readlines() if line.strip()]  # Creates list of lines in the file

    for l in lines:  # Iterates through lines in the file
        parameters = ''
        line = l.split()  # Creates a list of the individual words in the line (splitting by whitespace)

        for s in line:  # If a word in the line starts with "/", it adds the following word to the list of parameters
            if s.startswith('/') and line.index(s) + 1 < len(line):
                try:
                    float(line[line.index(s) + 1])
                    parameters += ', %s=%s' % (str(s[1:]), str(line[line.index(s) + 1]))
                except ValueError:
                    parameters += ', %s=True' % (str(s[1:]))
            elif s.startswith('/'):
                parameters += ', %s=True' % (str(s[1:]))
        try:
            dic, data = eval('ng.pipe_proc.%s(dic, data %s)' % (line[0].lower(), parameters))
            # Evaluates an expression that applies the appropriate processing command with its parameters
        except AttributeError:
            print('Error: Unknown function "%s" on line %s' % (line[0], lines.index(l) + 1))
        except TypeError:
            print('Error: Unknown parameter found in "%s" on line %s' % (parameters[2:], lines.index(l) + 1))
        except NameError:
            pass

    ng.pipe.write(out_file, dic, data, overwrite=True)  # Writes the processed data to a file with the name
    # specified as the output file in the procprm.in file

def generate_2d():
    f = open('process_2d.in', 'w')
    f.write('''SP /off 0.5 /end 1.00 /pow 1 /c 1.0
ZF /auto                               
FT /auto                      
PS /p0 0.00 /p1 0.00      
TP
SP /off 0.5 /end 1.00 /pow 1 /c 1.0
ZF /auto
FT /auto                         
PS /p0 0 /p1 0''')
    f.close()

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', action='store')
    parser.add_argument('-o', action='store')
    parser.add_argument('-p', action='store')
    parser.add_argument('-gen', action='store')
    #parser.add_argument('-f', action='store')

    args = parser.parse_args()

    in_file = args.i
    out_file = args.o
    param_file = args.p
    generate = args.gen

    if in_file and not os.path.exists(in_file):
        print('The specified file or path does not exist')
        sys.exit()

    if param_file and not os.path.exists(param_file):
        print('The specified file or path does not exist')
        sys.exit()

    if in_file and not generate:
        proc_from_params(in_file, out_file, param_file)

    if generate == 'basic-2d':
        generate_2d()

if __name__ == '__main__':
    if sys.argv[1].lower() == 'generate_2d':
        generate_2d()
    else:
        main()
