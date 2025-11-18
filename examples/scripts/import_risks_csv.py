#!/usr/bin/env python3
"""
Import risks from CSV file

CSV Format:
    title,description,probability,impact,category,treatment
    Data loss,Server failure,3,5,availability,mitigate
    Phishing,Email attack,4,4,confidentiality,mitigate

Usage:
    python import_risks_csv.py risks.csv
"""

import csv
import sys
import subprocess
from pathlib import Path

def import_risks_from_csv(csv_file):
    """Import risks from CSV file"""
    
    if not Path(csv_file).exists():
        print(f"Error: File {csv_file} not found")
        sys.exit(1)
    
    print(f"Importing risks from {csv_file}...")
    print("=" * 50)
    
    success_count = 0
    error_count = 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            try:
                # Build command
                cmd = [
                    'iso27001', 'risks', 'add',
                    '--title', row['title'],
                    '--description', row['description'],
                    '--probability', row['probability'],
                    '--impact', row['impact'],
                    '--category', row['category']
                ]
                
                if row.get('treatment'):
                    cmd.extend(['--treatment', row['treatment']])
                
                if row.get('controls'):
                    cmd.extend(['--controls', row['controls']])
                
                # Execute command
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                print(f"✓ {row['title']}")
                success_count += 1
                
            except subprocess.CalledProcessError as e:
                print(f"✗ {row['title']}: {e.stderr.strip()}")
                error_count += 1
            except KeyError as e:
                print(f"✗ Missing column: {e}")
                error_count += 1
    
    print("\n" + "=" * 50)
    print(f"Import completed:")
    print(f"  ✓ Success: {success_count}")
    print(f"  ✗ Errors:  {error_count}")
    
    return success_count, error_count

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python import_risks_csv.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    success, errors = import_risks_from_csv(csv_file)
    
    # Exit with error code if any errors
    sys.exit(1 if errors > 0 else 0)
