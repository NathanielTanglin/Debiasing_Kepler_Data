import os
from copy import copy

# Creates the path to the data directory.
_path = os.path.join(os.pardir, os.pardir, 'data')

# Finds all the files in the data directory and sorts them by system number, with the randomly oriented systems after the aligned systems.
system_names = sorted(os.listdir(_path), key = lambda val: (float(val.replace('sysSim_', '').replace('_randomO.csv', '')) + 0.5) if '_randomO' in val else float(val.replace('sysSim_', '').replace('.csv', '')))

# A list of unstable systems found by hand using the find_high_variations(...) method in the data generation scripts.
unstable_systems = [
    'sysSim_138_randomO.csv',
    'sysSim_744_randomO.csv',
    'sysSim_230_randomO.csv',
    'sysSim_357_randomO.csv',
    'sysSim_88.csv',
    'sysSim_579.csv',
    'sysSim_984.csv',
    'sysSim_165.csv',
    'sysSim_790.csv',
    'sysSim_709.csv'
]

stable_system_names = copy(system_names)

# Backwards iteration. Loop removes unstable systems from the data files list.
for idx in range(len(stable_system_names)-1, -1, -1):
    # Gets the specific file.
    filename = stable_system_names[idx]

    # Removes the file from the data if its an unstable system.
    if filename in unstable_systems:
        stable_system_names.pop(idx)
