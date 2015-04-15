"""
Calibrate class
-------------
Calibrate data from Raman spectra using Neon data and spectra class

@author: Rohan Isaac
"""

import os, sys
sys.path.append('spectra')
import spectra
import numpy as np
from itertools import izip
from scipy import stats	# for linear fit

from helper_functions import *


class Calibrate:
	""" Calibrates data, for details see constructor """
	
	def __init__(self, *args):
		"""
		Creates a calibrated data object
		"""
		pass
		
		
	def find_neon(self, x, tolerance=10):
		"""Find the closest neon peak within the given tolerance
		
		Arguments
		---------
		x (float):
			Peak in spectrum in 1/cm
		tolerance (float)
			Tolerance in 1/cm (default 10)
			
		Return
		------
		peak_pos (float)
			Peak that is closest (0 if not found)
		"""
		neon_data_nm = np.genfromtxt("neon_data.txt")
		neon_data = [wl2wn(i) for i in neon_data_nm]
		#print neon_data
		
		peak_diff = 10.0**6 #start large and make smaller
		closest_peak = 0.0
		for i in neon_data:
			if peak_diff > abs(i-x):
				peak_diff = abs(i-x)
				closest_peak = i
				
		# check within tolerance
		if peak_diff < tolerance:
			return closest_peak
		else:
			return 0
			
			
