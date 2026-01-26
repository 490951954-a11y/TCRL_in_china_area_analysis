# -*- coding: utf-8 -*-
"""
TRV Analysis Main Program
Main entry point for TRV data parsing and analysis
"""

import os
from trv_parser import TRVParser
from analysis_utils import print_analysis_results, print_trv_example

def main():
    """
    Main function to demonstrate the parser
    """
    # File path - update this to your actual file path
    file_path = "../data/trv_19802024.csv"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        print("Please place your TRV CSV file in the 'data' directory and update the file_path variable")
        return
    
    # Create parser instance
    parser = TRVParser()
    
    # Parse the file
    print("Parsing TRV CSV file...")
    data_blocks = parser.parse_file(file_path)
    
    if not data_blocks:
        print("No data was parsed. Exiting.")
        return
    
    # Analyze the dataset
    analysis = parser.analyze_dataset()
    print_analysis_results(analysis)
    
    # Print an example TRV
    print_trv_example(data_blocks)
    
    # Export options
    print("\n" + "=" * 60)
    print("EXPORT OPTIONS")
    print("=" * 60)
    
    export_choice = input("\nDo you want to export the data? (y/n): ").strip().lower()
    
    if export_choice == 'y':
        print("\nExport formats available:")
        print("1. JSON (preserves all original data)")
        print("2. CSV (simplified format for analysis)")
        
        format_choice = input("\nSelect export format (1 or 2): ").strip()
        
        if format_choice == '1':
            output_file = "../data/trv_parsed.json"
            parser.export_to_json(output_file)
        elif format_choice == '2':
            output_file = "../data/trv_parsed.csv"
            parser.export_to_csv(output_file)
        else:
            print("Invalid choice. Export cancelled.")
    
    print("\nData parsing complete.")

if __name__ == "__main__":
    main()