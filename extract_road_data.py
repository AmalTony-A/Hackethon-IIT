#!/usr/bin/env python3
"""Extract complete road data from HTML file and convert to JSON"""

import json
import re
from pathlib import Path

# Read the HTML file
html_file = Path(r"c:\Users\acer\Downloads\complete road data.html")
content = html_file.read_text(encoding='utf-8')

# Extract the JavaScript const ROADS array
# Find the start and end of the array
start_match = re.search(r'const\s+ROADS\s*=\s*\[', content)
if not start_match:
    print("Error: Could not find ROADS array in HTML")
    exit(1)

# Find the matching closing bracket
start_pos = start_match.end() - 1  # Position of the opening bracket
bracket_count = 0
end_pos = start_pos

for i in range(start_pos, len(content)):
    if content[i] == '[':
        bracket_count += 1
    elif content[i] == ']':
        bracket_count -= 1
        if bracket_count == 0:
            end_pos = i + 1
            break

# Extract the array content
array_str = content[start_pos:end_pos]

# Convert JavaScript object notation to JSON
# Replace single quotes with double quotes (carefully)
json_str = array_str
# Handle JavaScript object properties - convert unquoted keys to quoted
json_str = re.sub(r'(\w+):', r'"\1":', json_str)
# Convert single quotes to double quotes for strings
json_str = json_str.replace("'", '"')

# Parse as JSON
try:
    roads_data = json.loads(json_str)
    print(f"✓ Successfully extracted {len(roads_data)} roads")
    
    # Save to JSON file
    output_file = Path(r"d:\hackathon new\roadwatch_ai\backend\app\data\complete_road_data.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(roads_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved to {output_file}")
    
    # Print stats
    nh_count = sum(1 for r in roads_data if r['type'] == 'NH')
    sh_count = sum(1 for r in roads_data if r['type'] == 'SH')
    mdr_count = sum(1 for r in roads_data if r['type'] == 'MDR')
    total_km = sum(r['length'] for r in roads_data)
    
    print(f"\nStats:")
    print(f"  National Highways (NH): {nh_count}")
    print(f"  State Highways (SH): {sh_count}")
    print(f"  Major District Roads (MDR): {mdr_count}")
    print(f"  Total km: {total_km:.1f}")
    
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    print(f"First 500 chars of extracted array:")
    print(json_str[:500])
    exit(1)
