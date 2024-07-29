### generate_lib.py
# Author: Nathaniel Tanglin
#
# This file provides helper methods for the generation .ipynb files.

import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

# Gets the path from the current folder ('src') to the data directory.
path = os.path.join(os.pardir, os.pardir, 'data', 'raw')

# Stores a list of the data file names from the projectedOutput folder.
# Sort by simulation number where the randomized case gets placed second.
data_files = sorted(os.listdir(path), key = lambda val: (float(val.replace('sysSim_', '').replace('_randomO.csv', '')) + 0.5) if '_randomO' in val else float(val.replace('sysSim_', '').replace('.csv', '')))

def csv_2_data(filepath):
    '''
    Processes a .csv file such that the header and data are returned.
    The data is formatted such that each entry of the returned data array is a column represented by a numpy array. (i.e. data = [[column 1 data...], [column 2 data...], [column 3 data...] etc.])
    The header is a list of the header string names and is in order. (i.e. header = ['Time', 'Stellar mass', 'Stellar radius' ect.])
    '''

    # Captures the data.
    file = open(filepath)
    raw_data = list(csv.reader(file))
    file.close()
    
    # Extracts the header and relevant data.
    header = raw_data[0]
    data = np.array(raw_data[1:]).T
    
    return (header, data)

def data_2_csv(header, data, savepath):
    '''
    Opposite of csv_2_data. Given a header and data structure, saves data as a .csv file at the given savepath.
    
    Params:
    - header: The header to be used for the saved .csv

    - data: The data to be saved. Must be a list of numpy arrays (numpy.array), with each numpy array being a column.
            The indices must correspond to those of the header list.

    - savepath: The path to save the file at.
    '''

    with open(savepath, 'w', encoding = 'utf-8') as file:
        file.write(header)
        
        trans_data = data.T

        for row in trans_data:
            file.write(row)

def clean_data(data, scan = False):
    '''
    Cleans a data set of any outliers beyond 4-quartile deviations.
    Runs recursively until all outliers have been removed from the data.
    '''

    ndata = np.array(data)
    median = np.nanmedian(ndata)
    
    q1 = np.nanpercentile(ndata, 25)
    q3 = np.nanpercentile(ndata, 75)
    iqr = q3 - q1

    if str(iqr) == 'nan':
        raise Exception('nan value for iqr!')
 
    # Calculate Quartile Deviation
    qd = iqr / 2.0

    # Try lowering 
    max_err = (4.0 * qd)

    dirty = (abs(median - ndata) > max_err)

    if len(ndata[dirty]) > 0:
        if scan:
            output = '''Cleaning scan:
            Median: {med}
            Quartile deviation: {qd}
            Max error: {err}
            Cleaning range: {low}-{high}
            Spikes: {spikes}
            '''.format(qd = qd, err = max_err, med = median, spikes = list(ndata[dirty]), low = median - max_err, high = median + max_err)

            print(output)

        ndata[dirty] = np.nan

        ndata = clean_data(ndata)

    return ndata

def n_planet_prob(n):
    '''
    Helper function to return the header name for n-Planet multiplicity probabilities.
    These headers for the .csv data files are labeled as '1 Planets', '2 Planets', ... '9 Planets'
    Example use: n_planet_prob(1) returns '1 Planets', n_planet_prob(2) returns '2 Planets' etc.
    '''

    return str(n) + ' Planets'

# Gleans the relevant data from the chosen data file. This function calculates the expectation value
# and time values and returns them. It also returns the max planets in the system so this information
# can be included in the plots. 
def get_data(filepath, skip_failed_systems = False):
    try:
        # Extracts the header and data from the selected .csv file
        (header, data) = csv_2_data(filepath)

        # Finds the column index for the 'Time' column
        time_column = header.index('Time')

        endtime = data[time_column][-1].astype(float)

        if skip_failed_systems and endtime < 1e6:
            return None

        # Sets the initial planet header.
        planets = 1
        planets_header = n_planet_prob(planets)
        
        # Sets the first expectation value.
        exp_values = planets * data[header.index(planets_header)].astype(float)

        # Loops until there are no more MTP columns.
        while n_planet_prob(planets + 1) in header:
            # Integrates the loop forwards.
            planets += 1
            planets_header = n_planet_prob(planets)

            multiplicity_column = header.index(planets_header)

            exp_values += planets * data[multiplicity_column].astype(float)        

        # Cleans the data for return.
        (x, y) = (np.array(data[time_column]).astype(float), clean_data(exp_values))

        # Returns the data. Note that the expected values are cleaned of spikes using the 'clean_data' method.
        return {
            'axes': {
                'x': x,
                'y': y
            },
            'max_planets': planets
        }
    except FileNotFoundError as e:
        print(e)

        return {
            'axes': {
                'x': np.array([]),
                'y': np.array([])
            },
            'max_planets': 0
        }