### Author: OptimusThi
#!/usr/bin/env python3
"""
Script to populate heavy-ion collisions database.
"""

import os
import sqlite3
import numpy as np
import pandas as pd

# Configure the database path and data folder
db_path = 'hic_experimental_data.db'
data_folder = 'HIC_experimental_data-master/Pb-Pb-2760/ALICE'  # Adjust this path
# data_folder = 'HIC_experimental_data-master/'f{collision_system}'/f'{collaboration}'

# Define CSV path
#csv_directory = 'path/to/HEPData_csv_files/'
#file_path = 'path/to/HEPData_csv_file.csv'


# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ensure the table exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS experimental_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        system TEXT NOT NULL,
        collaboration TEXT NOT NULL,
        observable TEXT NOT NULL,
        centrality_low REAL NOT NULL,
        centrality_high REAL NOT NULL,
        centrality_mid REAL NOT NULL,
        value REAL NOT NULL,
        error REAL NOT NULL,
        reference TEXT
    );
''')

# Function to insert data into the table
def insert_data(system, collaboration, observable, data, reference):
    """
    Inserts data into the experimental_data table.
       
    Parameters:
    - system (str): Collision system, e.g., 'Pb-Pb-2760'.
    - collaboration (str): Experiment, e.g., 'ALICE'.
    - observable (str): Observable, e.g., 'mean_pT_pion'.
    - data (np.ndarray): Array containing columns: cent_low, cent_high, cent_mid, value, error.
    - reference (str): Reference of the data (e.g., DOI or arXiv).
    """
    for row in data:
        cent_low, cent_high, cent_mid, val, err = row[:5]
        cursor.execute('''
            INSERT INTO experimental_data (system, collaboration, observable, centrality_low, centrality_high,
                                           centrality_mid, value, error, reference)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (system, collaboration, observable, cent_low, cent_high, cent_mid, val, err, reference))
    conn.commit()

# Loop over each file in the data folder
for filename in os.listdir(data_folder):
    if filename.endswith('.dat'):
        file_path = os.path.join(data_folder, filename)
        observable_name = filename.replace('.dat', '')  # e.g., 'mean_pT_pion'

        # Load the data, skipping comments (header lines starting with #)
        data = np.loadtxt(file_path, comments="#")

        # Extract the reference from the header
        with open(file_path, 'r') as f:
            header = [line for line in f if line.startswith('#')]
            reference = header[0].strip('#').strip() if header else ''

        # Insert data into the database
        insert_data('Pb-Pb-2760', 'ALICE', observable_name, data, reference)

# Close the database connection
conn.close()

### From a csv file ### 

# Test 1: Check if the file can be loaded and preview data
def test_load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully!")
        print(data.head())
        return data
    except Exception as e:
        print("Error loading CSV:", e)
        return None

# Test 2: Check if expected columns are present in the file
def test_check_columns(data, expected_columns):
    missing_columns = [col for col in expected_columns if col not in data.columns]
    if not missing_columns:
        print("All expected columns are present!")
    else:
        print(f"Missing columns: {missing_columns}")
        
# Test 3: Check data types of each column
def test_check_data_types(data, column_types):
    for column, expected_type in column_types.items():
        if column in data.columns:
            actual_type = data[column].dtype
            print(f"Column: {column}, Expected: {expected_type}, Actual: {actual_type}")
            if actual_type != expected_type:
                print(f"Warning: Type mismatch in column {column}!")
        else:
            print(f"Column {column} is missing!")              

# Example tests
#data = test_load_csv(file_path)
#if data is not None:
#    expected_columns = ['cent_low', 'cent_high', 'val', 'err', 'reference']
#    test_check_columns(data, expected_columns)
#    column_types = {'cent_low': 'float64', 'cent_high': 'float64', 'val': 'float64', 'err': 'float64'}
#    test_check_data_types(data, column_types)

# Function to map CSV files to database schema and insert data
def populate_database_from_csv(file_path, system, collaboration, observable, reference=None):
    """
    Populate database from a CSV file with data in a structured format.

    Parameters:
    - file_path (str): Path to the CSV file.
    - system (str): Collision system, e.g., 'Pb-Pb-2760'.
    - collaboration (str): Experimental collaboration, e.g., 'ALICE'.
    - observable (str): Observable type, e.g., 'mean_pT_pion'.
    - reference (str): Reference for the data (optional).
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Load CSV file
    data = pd.read_csv(file_path)
    
    # Check for expected columns in data
    expected_columns = ['cent_low', 'cent_high', 'val', 'err']
    for col in expected_columns:
        if col not in data.columns:
            raise ValueError(f"Expected column '{col}' not found in CSV file.")
    
    # Prepare data for insertion
    for _, row in data.iterrows():
        cent_low = row['cent_low']
        cent_high = row['cent_high']
        cent_mid = (cent_low + cent_high) / 2.0
        value = row['val']
        error = row['err']
        
        # Insert data into the database
        cursor.execute("""
            INSERT INTO experimental_results (system, collaboration, observable, centrality_low, centrality_high, centrality_mid, value, error, reference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (system, collaboration, observable, cent_low, cent_high, cent_mid, value, error, reference))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print(f"Data from {file_path} inserted successfully.")

### Next Steps:
# - Configure the database path and data folder
# - Add (loop over) other directories: Au-Au-200,...
# - Populating the database using csv files from HEPData
# - Add a more flexible 
#   - Add other types of observables: pT-differential 
#   - Add latex labels for each observable
# - Verify results: test running a query
### 
