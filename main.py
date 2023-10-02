from rdkit import Chem
from rdkit.Chem import Descriptors
import random
import csv
import string

# Load data from 'file.csv'
with open('file.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

# Close the file automatically using a 'with' statement

initial_pop = [''.join(x) for x in data]

def calculate_properties(smiles):
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return None, None, None, None  # Handle invalid SMILES strings
    logp = Descriptors.MolLogP(m)
    weight = Descriptors.ExactMolWt(m)
    donors = Descriptors.NumHDonors(m)
    acceptors = Descriptors.NumHAcceptors(m)
    return logp, weight, donors, acceptors

# Initialize lists for properties
logp_values = []
weight_values = []
donors_values = []
acceptors_values = []

# Calculate properties and store them in separate lists
for x in initial_pop:
    logp, weight, donors, acceptors = calculate_properties(x)
    if logp is not None:
        logp_values.append(logp)
    if weight is not None:
        weight_values.append(weight)
    if donors is not None:
        donors_values.append(donors)
    if acceptors is not None:
        acceptors_values.append(acceptors)

# Check if properties meet criteria
total = []
if sum(1 for logp in logp_values if logp <= 5) >= 1:
    total.append(1)
if sum(1 for weight in weight_values if weight <= 500) >= 1:
    total.append(1)
if sum(1 for donors in donors_values if donors <= 5) >= 1:
    total.append(1)
if sum(1 for acceptors in acceptors_values if acceptors <= 10) >= 1:
    total.append(1)

# Initialize lists for splitting and recombining
first = []
second = []
parents = []
p1 = []

# Split initial_pop strings and create parents
for i in range(50):
    x = random.choice(initial_pop)
    split_index = len(x) // 2
    first.append(x[:split_index])
    second.append(x[split_index:])
    tot = second + first
    parents.append(random.choice(tot) + random.choice(tot))

# Choose a random parent
f = random.choice(parents)

def mutate(individual):
    mutate_random = random.choice(f)
    return f.replace(mutate_random, random.choice(string.ascii_letters), 1)

# Mutate the randomly chosen parent
mutated_f = mutate(f)

# Replace parents containing 'f' with the mutated version
for idx, item in enumerate(parents):
    if f in item:
        parents[idx] = mutated_f

# Initialize a list for valid SMILES
p1 = []

# Convert parents to valid molecules and store them
for item in parents:
    parents_item = Chem.MolFromSmiles(item)
    if parents_item  is not None:
        p1.append(item)

# Print the valid SMILES
print(p1)

