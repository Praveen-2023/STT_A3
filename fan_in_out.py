import json

# Load the JSON file
with open('dependencies.json', 'r') as file:
    data = json.load(file)

# Initialize dictionaries to store fan-in and fan-out
fan_in = {}
fan_out = {}

# Calculate fan-out (number of imports)
for module, details in data.items():
    fan_out[module] = len(details.get('imports', []))

# Calculate fan-in (number of imported_by)
for module, details in data.items():
    imported_by = details.get('imported_by', [])
    for importer in imported_by:
        fan_in[importer] = fan_in.get(importer, 0) + 1

# Print results in a table format
print("Module\t\tFan-In\tFan-Out")
print("-" * 30)
for module in data.keys():
    print(f"{module[:20]:20}\t{fan_in.get(module, 0)}\t{fan_out.get(module, 0)}")

# Optional: Save to a file for report
with open('fan_analysis.txt', 'w') as f:
    f.write("Module\t\tFan-In\tFan-Out\n")
    f.write("-" * 30 + "\n")
    for module in data.keys():
        f.write(f"{module[:20]:20}\t{fan_in.get(module, 0)}\t{fan_out.get(module, 0)}\n")