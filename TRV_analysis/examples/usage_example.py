# -*- coding: utf-8 -*-
"""
TRV Parser Usage Example
Demonstrates basic usage of the TRVParser class
"""

import sys
sys.path.append('../src')

from trv_parser import TRVParser
from analysis_utils import print_analysis_results, print_trv_example

def example_usage():
    # Initialize parser
    parser = TRVParser()
    
    # Parse data file
    data_file = "../data/trv_19802024.csv"
    data_blocks = parser.parse_file(data_file)
    
    if not data_blocks:
        print("Failed to parse data file")
        return
    
    # 1. Basic analysis
    analysis = parser.analyze_dataset()
    print_analysis_results(analysis)
    
    # 2. Get TRV by name
    print("\n" + "=" * 60)
    print("SEARCH BY NAME")
    print("=" * 60)
    katrina_trvs = parser.get_trv_by_name("Katrina")
    if katrina_trvs:
        print(f"Found {len(katrina_trvs)} TRV records for Katrina")
        print_trv_example(katrina_trvs)
    else:
        print("No TRV records found for Katrina")
    
    # 3. Get TRV by year
    print("\n" + "=" * 60)
    print("SEARCH BY YEAR (2005)")
    print("=" * 60)
    year_2005_trvs = parser.get_trv_by_year("2005")
    print(f"Found {len(year_2005_trvs)} TRV records for 2005")
    
    # 4. Export data
    print("\n" + "=" * 60)
    print("EXPORTING DATA")
    print("=" * 60)
    parser.export_to_json("../data/trv_2005.json")
    parser.export_to_csv("../data/trv_2005.csv")

if __name__ == "__main__":
    example_usage()