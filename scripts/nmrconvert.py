########################################################
#
# Script to convert 2d NMR data from the varian/agilent 
# format to NMRPipe. It is also able to convert data 
# aquired with the rance-kay/echo enti-echo quadrature. 
# 
# AJ Adkins, June 2021
# Skidmore Computational Biophysics Lab
########################################################

import os
import sys
import warnings
import numpy as np
import nmrglue as ng

NUCLEUS_RATIO = {'H':1.0,'N':0.101329118,'C':0.251449530}
NUCLEUS_FRQ_NAME = {'H':'sfrq','N':'dfrq2','C':'dfrq'}

def get_h2o_ppm(temperature):
    '''Return the water position in ppm in function of the temperature.'''

    return -0.009552 * temperature + 5.011718

def get_carrier_position_ppm(carrier_h, frq_h, frq_x, nucleus):    
    '''Return the carrier position in ppm in function of the temperature
    and the nucleus type.'''
    
    nu0_h = frq_h * 1e6 / (1.0 + carrier_h * 1e-6)
    nu0_x = NUCLEUS_RATIO[nucleus] * nu0_h
    car_x = (frq_x * 1e6 - nu0_x) / nu0_x * 1e6
    
    return car_x

def prompt_with_default(prompt, default):
    '''Input with a prompt and a default value.'''
    
    val = input('{} [{}]: '.format(prompt, default)).strip()
    
    return val or default

def reshuffle_rance_kay(data):
	'''Reshuffles the data according to the rance-kay scheme'''

	shuffled = np.empty(data.shape, data.dtype)
	dataP, dataN = data[0::2], data[1::2]
	shuffled[0::2] = dataP - dataN
	shuffled[1::2] = -1j * (dataP + dataN)

	return shuffled

def main():
	exp_dir = prompt_with_default('Enter experiment directory', './')
	acq_mode = prompt_with_default('Enter indirect acquisition mode ([C]omplex,[R]ance-Kay)', 'C')
	acq_mode = 'Complex' if acq_mode == 'C' else 'Rance-Kay'
	if acq_mode == 'Rance-Kay':
		nucleus_x = prompt_with_default('Enter indirect dimension nucleus (H,N,C)', 'N')
	out_file = input('Enter NMRPipe file name: ')
	if not out_file.endswith('.fid'):
		out_file += '.fid'


	# Read in files
	vdic, vdata = ng.varian.read(exp_dir, torder='f', as_2d=True)
	procpar_file = os.path.join(exp_dir, 'procpar')
	procpar_dic = ng.fileio.varian.read_procpar(procpar_file)


	# Conversion
	C = ng.convert.converter()

	if acq_mode == 'Rance-Kay':

		# Reshuffle data
		shuffled_data = reshuffle_rance_kay(vdata)

		# Direct dimension parameters
		sw = float(procpar_dic['sw']['values'][0])
		n1 = float(procpar_dic['np']['values'][0])
		temp = float(procpar_dic['temp']['values'][0])
		sfrq = float(procpar_dic['sfrq']['values'][0])
		x_car = float(get_h2o_ppm(float(temp)))

		# Indirect dimension parameters
		n0 = float(procpar_dic['ni']['values'][0])
		sw1 = float(procpar_dic['sw1']['values'][0])
		dfrq = float(procpar_dic[NUCLEUS_FRQ_NAME['N']]['values'][0])
		y_car = float(get_carrier_position_ppm(float(x_car), float(sfrq), float(dfrq), 'N'))

		# Convert to nmrpipe
		C.from_varian(vdic, shuffled_data)
		dic, data = C.to_pipe()

		# Update appropriate nmrpipe parameters
		dic['FDF2SW'] = sw
		dic['FDF2CAR'] = x_car
		dic['FDF2OBS'] = sfrq

		dic['FDF1SW'] = sw1
		dic['FDF1CAR'] = y_car
		dic['FDF1OBS'] = dfrq

		# Write file
		ng.pipe.write(out_file, dic, data, overwrite=True)

	else:
		C.from_varian(vdic, vdata)
		ng.pipe.write(out_file, *C.to_pipe(), overwrite=True)

warnings.filterwarnings("ignore")

if __name__ == '__main__':
	main()