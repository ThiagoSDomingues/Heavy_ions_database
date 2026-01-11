### Author: OptimusThi

"""
Script to plot that from HEP data csv files.  
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Experimental data files
EXPERIMENTAL_DATA = {
    7: {  # Centrality index 7 = 50-60%
        'file': 'experimental_data/differential_radial_flow/HEPData-ins2907010-v1-Figure_4a_cent7.csv',
        'label': '50-60%',
        'color': 'black',
        'marker': 'o'
    },
    8: {  # Centrality index 8 = 60-70%
        'file': 'experimental_data/differential_radial_flow/HEPData-ins2907010-v1-Figure_4a_cent8.csv',
        'label': '60-70%',
        'color': 'black',
        'marker': 's'
    }
}

# =============================================================================
# LOAD DATA
# =============================================================================

def load_experimental_data(filepath):
    """Load experimental data from CSV file"""
    if not Path(filepath).exists():
        print(f"Warning: Experimental data file '{filepath}' not found!")
        return None
    
    # Load CSV, skipping comment lines
    data = pd.read_csv(filepath, comment='#')
    
    # Rename columns for easier handling
    data.columns = ['pT', 'v0', 'stat_plus', 'stat_minus', 'sys_plus', 'sys_minus']
    
    # Calculate symmetric errors (absolute values)
    stat_err = np.abs(data['stat_plus'])
    sys_err = np.abs(data['sys_plus'])
    
    # Total error (quadrature sum of stat + sys)
    total_err = np.sqrt(stat_err**2 + sys_err**2)
    
    return {
        'pT': data['pT'].values,
        'v0': data['v0'].values,
        'stat_err': stat_err.values,
        'sys_err': sys_err.values,
        'total_err': total_err.values
    }

# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Check if centrality index is valid
    if CENTRALITY_INDEX not in EXPERIMENTAL_DATA:
        print(f"Error: Centrality index {CENTRALITY_INDEX} not found in EXPERIMENTAL_DATA!")
        print(f"Available centralities: {list(EXPERIMENTAL_DATA.keys())}")
        exit(1)
    
    cent_info = EXPERIMENTAL_DATA[CENTRALITY_INDEX]
    
    # Load experimental data
    print(f"Loading experimental data for {cent_info['label']}...")
    exp_data = load_experimental_data(cent_info['file'])
    if exp_data is not None:
        print(f"  ✓ Loaded {len(exp_data['pT'])} experimental points")
