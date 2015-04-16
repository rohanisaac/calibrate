# calibrate
Calibrate Raman signal with Neon peaks, could easily be generalized to other data and other line sources. 

Note: Since only care about peak position, ignore all backgrounds in line spectrum of Neon

Requires
--------

+ Python 2.7, numpy, scipy
+ spectra
	- requires peak-o-mat
		
Usage
-----

	sys.path.append('spectra') 
	sys.path.append('calibrate') # make sure python can find all the libraries
	import calibrate as cal

	neon_file = "/path/to/neon.txt"
	data_file = "/path/to/data.txt"

	calobj = cal.Calibrate(neon_file,data_file,532.04)
	calobj.write_file("/path/to/calibrated_file.txt")