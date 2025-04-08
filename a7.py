import csv

# Function to parse LCOM CSV file
def parse_lcom_csv(file_path):
    lcom_data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV file has no headers. Check the file format.")
        
        for row in reader:
            try:
                package_name = row['Package Name'].strip()
                type_name = row['Type Name'].strip()
                if not package_name or not type_name:
                    continue  # Skip rows with empty package or type names
                class_name = f"{package_name}.{type_name}"  # Fully qualified class name
                metrics = {
                    'LCOM1': float(row['LCOM1']) if row['LCOM1'] and row['LCOM1'].strip() else 0.0,
                    'LCOM2': float(row['LCOM2']) if row['LCOM2'] and row['LCOM2'].strip() else 0.0,
                    'LCOM3': float(row['LCOM3']) if row['LCOM3'] and row['LCOM3'].strip() else 0.0,
                    'LCOM4': float(row['LCOM4']) if row['LCOM4'] and row['LCOM4'].strip() else 0.0,
                    'LCOM5': float(row['LCOM5']) if row['LCOM5'] and row['LCOM5'].strip() else 0.0,
                    'YALCOM': float(row['YALCOM']) if row['YALCOM'] and row['YALCOM'].strip() else 0.0
                }
                lcom_data.append((class_name, metrics))
            except KeyError as e:
                print(f"Warning: Missing expected column {e} for row {row}. Skipping this row.")
            except ValueError as e:
                print(f"Warning: Invalid data for class {class_name}: {e}. Skipping this row.")
    return lcom_data

# Function to save top LCOM classes to CSV
def save_lcom_table_csv(classes_data, output_file, num_classes=5):
    # Sort by LCOM1 in descending order and take top N
    sorted_data = sorted(classes_data, key=lambda x: x[1].get('LCOM1', 0.0), reverse=True)[:num_classes]
    table_data = []
    for class_name, metrics in sorted_data:
        row = {
            'Java Code': class_name,
            'LCOM1': metrics.get('LCOM1', 0.0),
            'LCOM2': metrics.get('LCOM2', 0.0),
            'LCOM3': metrics.get('LCOM3', 0.0),
            'LCOM4': metrics.get('LCOM4', 0.0),
            'LCOM5': metrics.get('LCOM5', 0.0),
            'YALCOM': metrics.get('YALCOM', 0.0)
        }
        table_data.append(row)
    
    if table_data:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Java Code', 'LCOM1', 'LCOM2', 'LCOM3', 'LCOM4', 'LCOM5', 'YALCOM']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(table_data)
        print(f"Top LCOM classes saved to {output_file}")
    else:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            f.write("No data available for top LCOM classes.")
        print("No data available. Output file created with note.")

# Main execution
if __name__ == "__main__":
    # Specify the path to your CSV file
    csv_file = 'TypeMetrics.csv'  # Adjust path if needed
    output_file = 'lcom_activity7_table.csv'  # Output CSV file
    try:
        # Parse the LCOM CSV
        lcom_data = parse_lcom_csv(csv_file)
        if not lcom_data:
            print("No valid LCOM data found. Check the CSV file format or content.")
        else:
            # Save top LCOM classes to CSV
            save_lcom_table_csv(lcom_data, output_file)

    except FileNotFoundError:
        print(f"Error: The file {csv_file} was not found. Ensure the path is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")