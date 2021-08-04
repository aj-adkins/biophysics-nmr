########################################################
#
# Script to convert 2d NMR data from the bruker 
# format to NMRPipe. 
# 
# AJ Adkins, June 2021
# Skidmore Computational Biophysics Lab
########################################################


import os
import sys
import argparse
import nmrglue as ng
import warnings

warnings.filterwarnings("ignore")

def main():

	parser = argparse.ArgumentParser()

	parser.add_argument('-i', action='store', type=str, required=True, help='Bruker filepath')
	parser.add_argument('-o', action='store', type=str, required=True, help='NMRPipe file name')

	args = parser.parse_args()

	in_file = args.i
	out_file = args.o

	if not os.path.exists(in_file):
		print('The specified file or path does not exist')
		sys.exit()

	bdic, bdata = ng.bruker.read(in_file)
	C = ng.convert.converter()
	C.from_bruker(bdic, bdata)
	ng.pipe.write(out_file, *C.to_pipe(), overwrite=True)

	print('NMRPipe file successfully created')

if __name__ == '__main__':
	main()