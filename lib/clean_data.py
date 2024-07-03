import numpy as np

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