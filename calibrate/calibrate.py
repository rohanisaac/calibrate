"""
Calibrate class
-------------
Calibrate data from Raman spectra using Neon data and spectra class, see help file for details

@author: Rohan Isaac
"""

import os
import sys
import numpy as np
from itertools import izip
from scipy import stats  # for linear fit
from helper_functions import *
sys.path.append('spectra')
import spectra


class Calibrate:
    """ Calibrates data, for details see constructor """

    def __init__(self, *args):
        """
        Creates a calibrated data object

        calobj = calibrate.Calibrate(neon_file, data_file, laser_wavelength)

        Arguments
        ---------
        neon_file, data_file (strings)
                paths of neon calibration and data file to calibrate
        laser_wavelength (double)
                wavelength of raman laser in nm

        Usage
        -----
        sys.path.append('spectra')
        sys.path.append('calibrate')
        import calibrate as cal

        neon_file = "/path/to/neon.txt"
        data_file = "/path/to/data.txt"

        cal.Calibrate(neon_file,data_file)
        """

        if len(args) != 3:
            print "Not enough arguments"
            return

        else:
            neon_fil = args[0]
            data_fil = args[1]
            self.laser = args[2]

        print "Loading neon file..."
        # load file, put into spectra, find peaks and fit
        neon_dat = np.genfromtxt(neon_fil, delimiter='\t')
        self.data_dat = np.genfromtxt(data_fil, delimiter='\t')
        S = spectra.Spectra(neon_dat[:, 0], neon_dat[:, 1])
        # S.find_peaks(limit=4)

        print "Fitting neon data..."
        S.find_peaks()
        S.build_model()
        S.fit_data()

        # conglomerate
        pos_data_s = S.model.parameters_as_csv(selection="pos", witherrors=False).split('\n')
        pos_data = np.array([i.split(',')[2] for i in pos_data_s], dtype='double')

        print "Using peaks at: ", pos_data

        # convert to absolute wavenumber
        data_fit_wn = wl2wn(self.laser) - pos_data
        data_exp_wn = np.array([self.find_neon(i) for i in data_fit_wn])

        # mask out data that doesn't match with any reference data
        dmask = (data_exp_wn == 0)
        xx = [d for d, s in izip(data_fit_wn, dmask) if not s]
        yy = [d for d, s in izip(data_exp_wn, dmask) if not s]

        print "Fitting \n%s vs. \n%s" % (xx, yy)

        if len(xx) < 2:
            print "Not enough peaks found to calibrate"
            return
        elif len(xx) == 2:
            print "Not enough values to get any error estimates"

        # fit linear
        self.slope, \
			self.intercept, \
			self.r_value, \
			self.p_value,
			self.std_err = stats.linregress(xx, yy)
        print "Slope: %s, Intercept: %s" % (self.slope, self.intercept)

        return

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
        # print neon_data

        peak_diff = 10.0**6  # start large and make smaller
        closest_peak = 0.0
        for i in neon_data:
            if peak_diff > abs(i - x):
                peak_diff = abs(i - x)
                closest_peak = i

        # check within tolerance
        if peak_diff < tolerance:
            return closest_peak
        else:
            return 0

    def write_file(self, filename):
        """Write a file with the corrected output

        Arguments
        ---------
        filename (string)
                Path to file
        """

        # if folder doesn't exist
        fdir = os.path.dirname(os.path.abspath(filename))
        if not os.path.exists(fdir):
            print "Creating directory"
            os.makedirs(fdir)

        xdat = np.array(self.data_dat[:, 0])
        ydat = np.array(self.data_dat[:, 1])

        xdat_abs = wl2wn(self.laser) - xdat
        xdat_abs_c = self.slope * xdat_abs + self.intercept
        xdat_c = wl2wn(self.laser) - xdat_abs_c

        with open(filename, 'a') as outfile:
            for x, y in izip(xdat_c, ydat):
                outfile.write("{}\t{}\n".format(x, y))
