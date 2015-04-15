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
		# load file, put into spectra, find peaks and fit
		dat = np.genfromtxt(data_dir + i, delimiter='\t')
		S = spectra.Spectra(dat[:,0],dat[:,1])
		# S.find_peaks(limit=4)
		S.find_peaks()
		S.build_model()
		S.fit_data()
		
		# output results as txt, convert to numpy array
		data_strs = S.model.parameters_as_csv(selection="pos",witherrors=False).split('\n')
		data_a = np.array([i.split(',')[2] for i in data_strs],dtype='double')
		print data_a
		
		# convert to absolute wavenumber
		data_abs = wl2wn(532.04) - data_a
		data_exp = np.array([find_neon(i) for i in data_abs])
		
		print data_abs
		print data_exp
		
		dmask = (data_exp == 0)
		#xx = compress(data_abs, mask_here)
		#yy = compress(data_exp, mask_here)
		print dmask
		xx = [d for d, s in izip(data_abs, dmask) if not s]
		yy = [d for d, s in izip(data_exp, dmask) if not s]
		
		print xx
		print yy
		
		if np.count_nonzero(data_exp) < len(data_exp):
			print "Did not find matching neon peaks"
			print "len:", len(data_exp)
		else:
			print "Found matching neon peaks"
		
		if len(xx) == 2:
			print "Not enought values to get any error estimates"
			
		if len(xx) > 1:
			slope, intercept, r_value, p_value, std_err = stats.linregress(xx,yy)
			print "~~~~ Slope, intercept", slope, intercept
		
		
		#plot
		plt.figure(count)
		plt.plot(dat[:,0],dat[:,1],'r-')
		#count += 1
		
		
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

