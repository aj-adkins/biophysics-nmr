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
import nmrglue as ng


def nmr_proc(procprm):
    procprm_file = open(str(procprm))  # Reads in the nmr processing parameter file
    lines = [line for line in procprm_file.readlines() if line.strip()]  # Creates list of lines in the file

    for l in lines:  # Iterates through lines in the file
        parameters = ''
        line = l.split()  # Creates a list of the individual words in the line (splitting by whitespace)
        if line[0].startswith('/in'):  # Checks for the command /in and assigns the following filename as the input
            in_file = line[-1]
            try:
                dic, data = ng.pipe.read(in_file)  # Extracts the nmr data from the input file
            except IOError:
                print('Error: Unrecognized file.')

        elif line[0].startswith('/out'):  # Checks for the command /out and assigns the following filename as the output
            out_file = line[-1]

        else:  # After getting the input and output files, the script deals with the commands
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
    f.write('''/in test.fid                                    
SP /off 0.5 /end 1.00 /pow 1 /c 1.0
ZF /auto                               
FT /auto                      
PS /p0 0.00 /p1 0.00      
TP
SP /off 0.5 /end 1.00 /pow 1 /c 1.0
ZF /auto
FT /auto                         
PS /p0 0 /p1 0                                  
/out test.ft2
    ''')
    f.close()



if __name__ == '__main__':
    if sys.argv[1].lower() == 'generate_2d':
        generate_2d()
    else:
        nmr_proc(sys.argv[1])
