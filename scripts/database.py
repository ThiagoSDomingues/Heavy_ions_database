### Author: OptimusThi
#!/usr/bin/env python3
import numpy as np
import sqlite3
import json

### To build a generic and flexible database
# for storing heavy-ion collisions experimental data ### 

### Step 1. Define the database schema and 
# organize the observables systematically ### 

### Dictionary: outline the structure of the database
# and the key components for each observable ###

database_schema = {
    "collision_systems": {
        "system_id": "Unique identifier for the collision system",
        "projectile": "Projectile type (e.g., Pb, Au)",
        "target": "Target type (e.g., Pb, Au)",
        "sqrt_s": "Center-of-mass energy (GeV)",
    },
    "collaborations": {
        "collaboration_id": "Unique identifier for the collaboration",
        "collaboration_name": "Name of the experimental collaboration (e.g., ALICE, CMS)",
    },
    "observables": {
        "observable_id": "Unique identifier for the observable",
        "observable_name": "Name of the observable (e.g., mean_pT, dNch/deta, v22)",
    },
    "experimental_results": {
        "result_id": "Unique identifier for the result",
        "system_id": "Link to the collision system",
        "collaboration_id": "Link to the collaboration",
        "observable_id": "Link to the observable",
        "centrality_bins": "List of centrality bins (e.g., 0-5, 5-10%)",
        "value": "Measured value of the observable (1D array for centrality bins)",
        "error": "Error associated with each value",
        "reference": "Citation for the result (e.g., arXiv ID)",
        "trigger_info": "Trigger and centrality selection details for the analysis"
    },
    "kinematic_cuts": {
        "cut_id": "Unique identifier for the cut",
        "result_id": "Link to the experimental result",
        "eta_min": "Minimum pseudorapidity",
        "eta_max": "Maximum pseudorapidity",
        "pt_min": "Minimum transverse momentum",
        "pt_max": "Maximum transverse momentum",
        "y_min": "Minimum rapidity",
        "y_max": "Maximum rapidity",
    },
}

# Define centrality bins for ALICE and STAR experiments
ALICE_cent_bins = np.array( [ [0,5],[5,10],[10,20],[20,30],[30,40],[40,50],[50,60],[60,70],[70,80] ] ) # 9 centrality classes.
STAR_cent_bins = np.array( [ [0,5],[5,10],[10,20],[20,30],[30,40],[40,50],[50,60],[60,70],[70,80] ] ) # 9 centrality classes.

#Charged particle multiplicity observable (class instance)
# ABS(ETARAP) < 0.5
# Collision system: Pb-Pb
# sqrts/NUCLEON: 2760.0 GeV 

### Generic class for all observables
# Each observable has specific inputs. The Observable class must account for all common inputs.
# Base Class Handling: common atrributes: collision system, collaboration, other metadata... should be managed centrally
###
# Base Observable Class
class Observable:
    """Base class for all observables."""
    required_params = []  # List to be overridden by subclasses

    def __init__(self, name, short_name, collision_system, collaboration, reference, centrality_bins, values, errors, trigger_info, **kwargs):
        self.name = name  
        self.short_name = short_name  
        self.collision_system = collision_system  
        self.collaboration = collaboration  
        self.reference = reference  
        self.centrality_bins = centrality_bins  
        self.values = values  
        self.errors = errors  
        self.trigger_info = trigger_info  

        # Set required parameters dynamically
        for param in self.required_params:
            if param in kwargs:
                setattr(self, param, kwargs[param])
            else:
                raise ValueError(f"Missing required parameter: {param} for {self.__class__.__name__}")

    @classmethod
    def get_required_params(cls):
        """Return list of required parameters for this observable."""
        return cls.required_params        

# Specific Observable Classes
class Multiplicity(Observable):
    required_params = ['particle_type', 'rapidity_range', 'pT_range']

class MeanPT(Observable):
    required_params = ['particle_type', 'rapidity_range', 'pT_range']

class IntegratedVn2(Observable):
    required_params = ['harmonic_n', 'rapidity_range', 'pT_range']

class IntegratedVn4(Observable):
    required_params = ['harmonic_n', 'rapidity_range', 'pT_range']    

class PtDifferentialVn2(Observable):
    required_params = ['harmonic_n', 'rapidity_range', 'pT_bins']

class PtDifferentialVn4(Observable):
    required_params = ['harmonic_n', 'rapidity_range', 'pT_bins']

class TransverseEnergy(Observable):
    required_params = ['particle_type', 'rapidity_range', 'pT_range']
    
class PTFluc(Observable):
    required_params = ['particle_type', 'rapidity_range', 'pT_range']    
                
    
### Usage Examples: instantiation using keyword arguments for observable-specific parameters
# 1. ALICE Collaboration Pb-Pb Charged Particle Multiplicity

alice_ch_mult = Multiplicity(
    name="Charged-particle multiplicity",
    short_name="dNch_deta",
    collision_system="Pb-Pb-2760",
    collaboration="ALICE",
    reference={
        "arXiv": "arxiv:1012.1657",
        "doi": "10.1103/PhysRevLett.106.032301",
        "title": "Centrality dependence of the charged-particle multiplicity density at mid-rapidity in Pb-Pb collisions at $\sqrt{s_{NN}}=2.76$ TeV",        
    },
    centrality_bins=ALICE_cent_bins,
    values=np.array([1601, 1294, 966, 649, 426, 261, 149, 76, 35]), 
    errors=np.array([60, 49, 37, 23, 15, 9, 6, 4, 2]),
    trigger_info={
        "Trigger": "VZERO and SPD detectors",
        "Centrality Selection": "VOM amplitude
    }
    particle_type="charged",
    rapidity_range=[-0.5, 0.5],
    pT_range=[0.2, 5.0]
)
# 2.STAR Collaboration Au-Au Identified Pion Multiplicity
star_pion_mult = Multiplicity(
    name="Identified pion multiplicity",
    short_name="dNch_deta_pion",
    collision_system="Au-Au-200",
    collaboration="STAR",
    reference={
        "arXiv": "arXiv:0808.2041",
        "doi": "10.1103/PhysRevC.79.034909",
        "title": "Systematic Measurements of Identified Particle Spectra in $p p, d^+$ Au and Au+Au Collisions from STAR",        
    },
    centrality_bins=STAR_cent_bins,
    values=np.array([...]),  # Replace with real data 
    errors=np.array([...]),
    trigger_info={
        "Trigger": "BBC and TOF detectors",
        "Centrality Selection": "Charged particle multiplicity"
    },
    particle_type="pion",
    rapidity_range=[-1.0, 1.0],
    pT_range=[0.2, 3.0]
    
# 3. ALICE Integrated v_2{2} Pb-Pb:

alice_v2_int = IntegratedVn2(
    name="Elliptic flow coefficient v2{2}",
    short_name="v22",
    collision_system="Pb-Pb-2760",
    collaboration="ALICE",
    reference={
        "arXiv": "arXiv:1105.3865",
        "doi": "10.1103/PhysRevLett.107.032301",
        "title": "Higher harmonic anisotropic flow measurements of charged particles in Pb-Pb collisions at √sNN=2.76 TeV"
    },
    centrality_bins=ALICE_cent_bins,
    values=np.array([...]),  # Replace with real data
    errors=np.array([...]),
    trigger_info={
        "Trigger": "TPC and VZERO detectors",
        "Centrality Selection": "VZERO amplitude"
    },
    harmonic_n=2,
    rapidity_range=[-0.8, 0.8],
    pT_range=[0.2, 5.0]
)

# 4. STAR pT-differential v_3{2} Au-Au:

#star_v32 = PtDifferentialVn2(
#    name="Two-particle correlations triangular flow",
#    short_name="v32",
#    collision_system="Au-Au-200",
#    collaboration="STAR",
#    reference={
#        "arXiv": "arxiv:1012.1657",
#        "doi": "10.1103/PhysRevLett.106.032301",
#        "title": "Centrality dependence of the charged-particle multiplicity density at mid-rapidity in Pb-Pb collisions at $\sqrt{s_{NN}}=2.76$ TeV",        
#    },
#    centrality_bins=STAR_cent_bins,
#    values=np.array([1601, 1294, 966, 649, 426, 261, 149, 76, 35]), 
#    errors=np.array([60, 49, 37, 23, 15, 9, 6, 4, 2]),
#    trigger_info={
#        "Trigger": "VZERO and SPD detectors",
#        "Centrality Selection": "ZDC"
#    }
#    particle_type="pions"
#    harmonic_n=3
#    rapidity_range=[-0.5, 0.5],
#    pT_range=[0.2, 5.0]
#)
   
###

### Querying Requirements
# Get parameters needed for Multiplicity measurements
#print("Multiplicity require:", Multiplicity.get_required_params())

# Get parameters needed for FlowHarmonics
#print("Flow harmonics require:", FlowHarmonics.get_required_params())

###

-------------------------- Function to plot observables -------------------

# Example Plot Function
def plot_observable(observable, xlabel="Centrality (%)", ylabel=None):
    plt.figure(figsize=(6,5))
    centrality_mid = [(b[0] + b[1]) / 2 for b in observable.centrality_bins]
    
    plt.errorbar(centrality_mid, observable.values, yerr=observable.errors, fmt='o', capsize=4, label=observable.name, color='blue')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel if ylabel else observable.short_name)
    plt.title(f"{observable.name}")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

# Plot Examples
#plot_observable(alice_ch_mult, ylabel=r"$dN_{ch}/d\eta$")
#plot_observable(alice_ch_mult, ylabel=r"$dN_{ch}/d\eta$")
#plot_observable(alice_ch_mult, ylabel=r"$dN_{ch}/d\eta$")

----------------------------------------------------------

### Step 3: Functions to populate and query the database ###

def populate_database():
    conn = sqlite3.connect("experimental_data.db")
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS systems (
            system_id INTEGER PRIMARY KEY,
            system_name TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collaborations (
            collaboration_id INTEGER PRIMARY KEY,
            collaboration_name TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS observables (
            observable_id INTEGER PRIMARY KEY,
            observable_name TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experimental_results (
            result_id INTEGER PRIMARY KEY,
            system_id INTEGER,
            collaboration_id INTEGER,
            observable_id INTEGER,
            centrality_bins TEXT,
            value TEXT,
            error TEXT,
            reference TEXT,
            FOREIGN KEY (system_id) REFERENCES systems(system_id),
            FOREIGN KEY (collaboration_id) REFERENCES collaborations(collaboration_id),
            FOREIGN KEY (observable_id) REFERENCES observables(observable_id)
        )
    ''')

    # Insert default system and collaboration if they don't exist
    cursor.execute('''
        INSERT OR IGNORE INTO systems (system_id, system_name)
        VALUES (1, 'Pb-Pb-2760')
    ''')
    cursor.execute('''
        INSERT OR IGNORE INTO collaborations (collaboration_id, collaboration_name)
        VALUES (1, 'ALICE')
    ''')

    # Insert Integrated Observable Data
    def insert_integrated_observable_data(obs):
        cursor.execute('''
            INSERT INTO observables (observable_name)
            VALUES (?)
        ''', (obs.short_name,))
        cursor.execute('''
            SELECT observable_id FROM observables WHERE observable_name = ?
        ''', (obs.short_name,))
        observable_id = cursor.fetchone()[0]

        cursor.execute('''
            INSERT INTO experimental_results (
                system_id, collaboration_id, observable_id, centrality_bins, value, error, reference
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            1,  # Using the default system_id
            1,  # Using the default collaboration_id
            observable_id,
            json.dumps(obs.centrality_bins.tolist()),
            json.dumps(obs.values.tolist()),
            json.dumps(obs.errors.tolist()),
            str(obs.reference)
        ))

    # Assuming dNch_deta is defined and has the required attributes
    insert_integrated_observable_data(dNch_deta)
    
    # Insert Differential Observable Data
    # def insert_differential_observable_data(obs):

    conn.commit()
    conn.close()

populate_database()
