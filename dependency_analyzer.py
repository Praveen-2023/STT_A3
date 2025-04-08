import json

# Load the JSON file
with open('dependencies.json', 'r') as file:
    data = json.load(file)

# Function to detect cycles using DFS
def has_cycle(graph, node, visited, path_visited):
    visited.add(node)
    path_visited.add(node)
    # Debug: Print the type and content of graph.get(node, {})
    node_data = graph.get(node, {})
    print(f"Node: {node}, Type: {type(node_data)}, Content: {node_data}")
    imports = node_data.get('imports', [])
    for neighbor in imports:
        if neighbor not in visited:
            if has_cycle(graph, neighbor, visited, path_visited):
                return True
        elif neighbor in path_visited:
            return True
    path_visited.remove(node)
    return False

# Analyze dependencies
highly_coupled = []
cycles = []
max_depth = 0

# Use the original data dictionary for analysis
graph = data  # Directly use the loaded JSON data

# Find highly coupled modules (top 5 by fan-out)
fan_out = {module: len(details.get('imports', [])) for module, details in data.items()}
sorted_by_fanout = sorted(fan_out.items(), key=lambda x: x[1], reverse=True)
highly_coupled = sorted_by_fanout[:5]

# Detect cycles
visited = set()
path_visited = set()
for module in data:
    if module not in visited:
        if has_cycle(graph, module, visited, path_visited):
            cycles.append(module)

# Estimate depth using bacon values (simplified)
depths = {module: details.get('bacon', 0) for module, details in data.items()}
max_depth = max(depths.values()) if depths else 0

# Output results
print("Highly Coupled Modules (Top 5 by Fan-Out):")
for module, count in highly_coupled:
    print(f"{module}: {count} dependencies")

print("\nCyclic Dependencies Detected:")
print(cycles if cycles else "None detected")

print(f"\nMaximum Dependency Depth: {max_depth}")

# Save to a file for report
with open('dependency_analysis.txt', 'w') as f:
    f.write("Highly Coupled Modules (Top 5 by Fan-Out):\n")
    for module, count in highly_coupled:
        f.write(f"{module}: {count} dependencies\n")
    f.write("\nCyclic Dependencies Detected:\n")
    f.write(str(cycles if cycles else "None detected") + "\n")
    f.write(f"\nMaximum Dependency Depth: {max_depth}\n")