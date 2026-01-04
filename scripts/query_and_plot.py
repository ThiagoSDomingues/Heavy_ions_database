#!/usr/bin/env python3
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def connect_to_database(db_path="experimental_data.db"):
    """Connect to the SQLite database."""
    return sqlite3.connect(db_path)

def query_observables(cursor, observable_name):
    """Query data for a specific observable from the database."""
    cursor.execute('''
        SELECT centrality_bins, value, error, reference
        FROM experimental_results
        JOIN observables ON experimental_results.observable_id = observables.observable_id
        WHERE observables.observable_name = ?
    ''', (observable_name,))
    result = cursor.fetchone()
    if result:
        centrality_bins = np.array(json.loads(result[0])) 
        values = np.array(json.loads(result[1]))          
        errors = np.array(json.loads(result[2]))     
        reference = result[3]
        return centrality_bins, values, errors, reference
    else:
        raise ValueError(f"No data found for observable: {observable_name}")

def plot_integrated_observable(centrality_bins, values, errors, observable_name, reference):
    """Plot an integrated observable."""
    centrality_mid = [(low + high) / 2 for low, high in centrality_bins]
    plt.errorbar(centrality_mid, values, yerr=errors, fmt='o', capsize=3, label=observable_name, color='blue')
    plt.xlabel("Centrality (%)")
    plt.ylabel(observable_name)
    plt.title(f"{observable_name} vs Centrality")
#    plt.suptitle(f"Reference: {reference}", fontsize=10, style='italic')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_differential_observable(pt_bins, values, errors, observable_name, reference):
    """Plot a pT-differential observable."""
    pt_mid = [(low + high) / 2 for low, high in pt_bins]
    for i, (centrality_bin, val, err) in enumerate(zip(centrality_bins, values, errors)):
        plt.errorbar(pt_mid, val, yerr=err, fmt='o', capsize=3, label=f"Centrality {centrality_bin}")
    plt.xlabel("pT (GeV/c)")
    plt.ylabel(observable_name)
    plt.title(f"{observable_name} vs pT")
#    plt.suptitle(f"Reference: {reference}", fontsize=10, style='italic')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
#def plot_calc_vs_exp_data()
        

if __name__ == "__main__":
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        # Example: Query and plot an integrated observable
        observable_name = "mean_pT_pion"
        centrality_bins, values, errors, reference = query_observables(cursor, observable_name)
        plot_integrated_observable(centrality_bins, values, errors, observable_name, reference)

        # Example: Query and plot a pT-differential observable
        # Replace the below variables with actual data from the database when available
        pt_bins = [(0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0), (1.0, 1.2)]
        values = [[0.12, 0.11, 0.10, 0.09, 0.08]]
        errors = [[0.01, 0.009, 0.008, 0.007, 0.006]]
        reference = "arXiv:1609.06629"
        plot_differential_observable(pt_bins, values, errors, "v2_pion_pT", reference)

    except ValueError as e:
        print(e)

    conn.close()
    
    
