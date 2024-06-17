import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

# Gets the path from the current folder ('src') to the data director ('projectOutput').
path = os.path.join(os.pardir, 'data')

# Stores a list of the data file names from the projectedOutput folder.
# Sort by simulation number where the randomized case gets placed second.
data_files = sorted(os.listdir(path), key = lambda val: (float(val.replace('sysSim_', '').replace('_randomO.csv', '')) + 0.5) if '_randomO' in val else float(val.replace('sysSim_', '').replace('.csv', '')))

# Processes a .csv file such that the header and data are returned. The data is formatted
# such that each entry of the returned data array is a column represented by a numpy array. (i.e. data = [[column 1 data...], [column 2 data...], [column 3 data...] etc.])
# The header is a list of the header string names and is in order. (i.e. header = ['Time', 'Stellar mass', 'Stellar radius' ect.])
def csv_2_data(filepath):
    # Captures the data.
    file = open(filepath)
    raw_data = list(csv.reader(file))
    file.close()
    
    # Extracts the header and relevant data.
    header = raw_data[0]
    data = np.array(raw_data[1:]).T
    
    return (header, data)

# Cleans a data set of any outliers greater than 15-sigma, and runs recursively until all outliers
# have been removed from the data.
def clean_data(data):
    ndata = np.array(data)
    median = np.nanmedian(ndata)
    
    q1 = np.nanpercentile(ndata, 25)
    q3 = np.nanpercentile(ndata, 75)
    iqr = q3 - q1

    if str(iqr) == 'nan':
        raise Exception('nan value for iqr!')
 
    # Calculate Quartile Deviation
    qd = iqr / 2.0

    max_err = (15.0 * qd)

    dirty = (abs(median - ndata) > max_err)

    if len(ndata[dirty]) > 0:
        ndata[dirty] = np.nan

        ndata = clean_data(ndata)

    return ndata

# Helper function to return the header name for n-Planet multiplicity probabilities.
# These headers for the .csv data files are labeled as '1 Planets', '2 Planets', ... '9 Planets'
# Example use: n_planet_prob(1) returns '1 Planets', n_planet_prob(2) returns '2 Planets' etc.
def n_planet_prob(n):
    return str(n) + ' Planets'

# Gleans the relevant data from the chosen data file. This function calculates the expectation value
# and time values and returns them. It also returns the max planets in the system so this information
# can be included in the plots. 
def get_data(filepath, skip_failed_systems = False):
    # Extracts the header and data from the selected .csv file
    (header, data) = csv_2_data(filepath)

    # Finds the column index for the 'Time' column
    time_column = header.index('Time')

    if skip_failed_systems and data[time_column][-1].astype(float) < 1e6:
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