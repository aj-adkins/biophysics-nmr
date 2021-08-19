# biophysics-nmr


Description
-----------
A set of scripts and software written in Python to process and plot 2-dimensional NMR data.

The conversion and processing scripts require the installation of the following dependencies:
* [Python 3](https://www.python.org/downloads/)
* [Numpy](https://numpy.org/install/)
* [NMRGlue](https://nmrglue.readthedocs.io/en/latest/install.html)

The interactive visualization software requires the additional packages:
* [PyQt5](https://pypi.org/project/PyQt5/)
* [PyQtGraph](https://www.pyqtgraph.org/)

The jupyter notebook outlining the plotting of NMR data requires the packages:
* [Matplotlib](https://matplotlib.org/stable/users/installing.html)
* [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/index.html)

Conversion
----------
There are two command line scripts that are able to convert NMR data from the Varian and Bruker data formats into NMRPipe. 

#### Varian
The varian.py conversion script is able to convert data that is acquired with both the complex encoding and the rance-kay/echo anti-echo encoding. The scripts make use of command line flags to specify the specific parameters:
* -i specifies the input varian directory. 
* -o specifies the desired name of the output file.
* -acq specifies the acquisition mode, which can be either 'complex' or 'rance-kay'. It is complex by default. 
* -nuc specifies the nucleus in the indirect dimension if rance-kay is selected. It can be either 'N', 'C', or 'H'. 
For example, the following command can be used to convert standard complex data:
```
python varian.py -i test_varian.fid -o test_pipe.fid 
```
And for rance-kay conversion:
```
python varian.py -i test_varian.fid -o test_pipe.fid -acq rance-kay -nuc N
```

#### Bruker
The bruker.py script operates in the same way as the varian script:
```
python bruker.py -i test_bruker.fid -o test_pipe.fid
```
Working with different acquisition modes for Bruker data will be implemented in the future.

Processing
---------
To apply standard processing functions, the script nmrproc.py can be used. 
* -i specifies the input file to be processed.
* -o specifies the processed output file.
* -p specifies the parameter file, which must be created by the user.

#### Parameter File
To apply processing functions to the data, a parameter file must be passed as an argument to the python script. This file should just be a plain text file, and similar to NMRPipe, each line will declare a function to be applied. The line should begin with the name of the function. Then, additional parameters can be specified by leading the name of the parameter with a slash, with the value following after. For example, a phase shift would like this:
```
PS /p0 -90.00 /p1 180.00
```
In this case, PS is the function name for a phase shift, and the zero order phase is shifted by -90 degrees, and the first order phase shifted by 180. 
Some funtions take boolean parameters which don't require values, such region extraction:
```
EXT /sw /left
```
As many functions as required can be specified in the parameter file, which can then be passed into the script using the -p flag.
As the script is built using NMRGlue, a full list of functions and their parameters can be found in the [NMRGlue documentation](https://nmrglue.readthedocs.io/en/latest/reference/pipe_proc.html). The syntax must follow the format specified above, so the documentation should only be used as reference.

The ability to apply individual functions straight from the command line will be implemented in the future. 

Visualization
---

Included in the 'jupyter' folder is a jupyter notebook which details plotting NMR data using matplotlib, including identifying peaks and obtaining one-dimensional slices. 

In the 'visualize' folder, Main.py can be run to launch the interactive NMR software included in this project. 
