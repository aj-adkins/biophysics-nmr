biophysics-nmr
-------------
-------------

Description
-----------
A set of scripts and software written in Python to process and plot 2-dimensional NMR data.

The conversion and processing scripts require the installation of the following dependencies:
* [Python 3](https://www.python.org/downloads/)
* [Numpy](https://numpy.org/install/)
* [NMRGlue](https://nmrglue.readthedocs.io/en/latest/install.html)

The interactive visualization software requires the additional dependencies:
* [PyQt5](https://pypi.org/project/PyQt5/)
* [PyQtGraph](https://www.pyqtgraph.org/)

The jupyter notebook outlining the plotting of NMR data requires the dependencies:
* [Matplotlib](https://matplotlib.org/stable/users/installing.html)
* [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/index.html)

Conversion
----------
There are two command line scripts that are able to convert NMR data from the Varian and Bruker data formats into NMRPipe. 

#### Varian
The varian.py conversion script is able to convert data that is acquired with both the complex encoding and the rance-kay encoding. The scripts make use of command line flags to specify the specific parameters:
* -i specifies the input varian directory. 
* -o specifies the desired name of the output file.
* -acq specifies the acquisition mode, which can be either 'complex' or 'rance-kay'. It is complex by default. 
* -nuc specifies the nucleus in the indirect dimension if rance-kay is selected. It can be either 'N', 'C', or 'H'. 
For example, the following command can be used to convert standard complex data:
'''
python varian.py -i test_varian.fid -o test_pipe.fid 
'''
And for rance-kay conversion:
'''
python varian.py -i test_varian.fid -o test_pipe.fid -acq rance-kay -nuc N
'''

#### Bruker
The bruker.py script operates in the same way as the varian script:
'''
python bruker.py -i test_bruker.fid -o test_pipe.fid
'''
