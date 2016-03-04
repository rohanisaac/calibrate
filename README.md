# calibrate


Calibrate Raman signal (relative wavenumber (1/cm)) using Neon line spectrum. Reference data from CRC Handbook of Chemistry and Physics [1]

Note: Could easily be generalized to other data and other line sources.

Note: Since only care about peak position, ignore all backgrounds in line spectrum of Neon



Requires
--------

+ Python 2.7, numpy, scipy
+ spectra
	- requires lmfit

Usage
-----

	import sys
	sys.path.append('spectra')
	sys.path.append('calibrate') # make sure python can find all the libraries
	import calibrate as cal

	neon_file = "/path/to/neon.txt"
	data_file = "/path/to/data.txt"

	calobj = cal.Calibrate(neon_file,data_file,532.04)
	calobj.write_file("/path/to/calibrated_file.txt")

Todo
----

1. Use lmfit for linear fit instead of scipy fit. 

References
----------

CRC Handbook of Chemistry and Physics, 95th Edition. http://www.hbcpnetbase.com/ (Section 10: Atomic, Molecular, and Optical Physics -> Line Spectra of the Elements)
