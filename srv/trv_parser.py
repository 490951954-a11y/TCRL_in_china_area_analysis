# -*- coding: utf-8 -*-
"""
TRV (Tropical Cyclone Residual Vortex) CSV File Parser
Core parsing logic for TRV tracking data
"""

import csv
from collections import namedtuple
import json
from typing import List, Dict, Any

# Data structure for header information
HeaderData = namedtuple('HeaderData', [
    'flag',           # '66666' - indicates best track data
    'intl_code',      # International ID (last 2 digits of year + 2-digit number)
    'record_count',   # Number of track records
    'sequence_num',   # Original TC sequence number
    'china_code',     # Chinese TC number
    'stop_reason',    # Reason for stopping tracking (0-3)
    'name',           # English name of the TC
    'start_date'      # Start tracking date (YYYYMMDD)
])

# Data structure for track information
TrackData = namedtuple('TrackData', [
    'time',           # Timestamp (YYYYMMDDHH)
    'lat',            # Latitude (0.1°N)
    'lon',            # Longitude (0.1°E)
    'stream_func',    # 850hPa stream function (10⁴m²/s)
    'vorticity',      # 850hPa vorticity (10⁻⁵s⁻¹)
    'velocity'        # 850hPa velocity (0.1m/s)
])

class TRVParser:
    """Parser for TRV CSV files"""
    
    def __init__(self):
        """Initialize the parser"""
        self.data_blocks = []  # List of parsed data blocks
        
    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse TRV format CSV file
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            List of data blocks, each containing header and track data
        """
        self.data_blocks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
        
        i = 0
        line_count = len(lines)
        
        while i < line_count:
            line = lines[i].strip()
            
            # Check if this is a header line (starts with '66666')
            if line.startswith('66666'):
                # Parse header data
                header_fields = line.split(',')
                
                if len(header_fields) != 8:
                    print(f"Warning: Line {i+1} has incorrect number of header fields: {len(header_fields)}")
                    i += 1
                    continue
                
                try:
                    # Create HeaderData object
                    header = HeaderData(
                        flag=header_fields[0],
                        intl_code=header_fields[1],
                        record_count=int(header_fields[2]),
                        sequence_num=header_fields[3],
                        china_code=header_fields[4],
                        stop_reason=int(header_fields[5]),
                        name=header_fields[6],
                        start_date=header_fields[7]
                    )
                except ValueError as e:
                    print(f"Warning: Error parsing header at line {i+1}: {e}")
                    i += 1
                    continue
                
                i += 1  # Move to next line
                
                # Parse track data for this TC
                track_data = []
                expected_records = header.record_count
                actual_records = 0
                
                # Read track records
                while actual_records < expected_records and i < line_count:
                    # Check if next line is a new header
                    if lines[i].strip().startswith('66666'):
                        break
                    
                    track_fields = lines[i].strip().split(',')
                    
                    if len(track_fields) != 6:
                        print(f"Warning: Line {i+1} has incorrect number of track fields: {len(track_fields)}")
                        i += 1
                        continue
                    
                    try:
                        # Create TrackData object
                        track = TrackData(
                            time=track_fields[0],
                            lat=int(track_fields[1]),
                            lon=int(track_fields[2]),
                            stream_func=int(track_fields[3]),
                            vorticity=int(track_fields[4]),
                            velocity=int(track_fields[5])
                        )
                        track_data.append(track)
                        actual_records += 1
                    except ValueError as e:
                        print(f"Warning: Error parsing track data at line {i+1}: {e}")
                    
                    i += 1
                
                # Check if we got all expected records
                if actual_records != expected_records:
                    print(f"Warning: {header.name} ({header.start_date}) "
                          f"expected {expected_records} records, got {actual_records}")
                
                # Store the complete data block
                self.data_blocks.append({
                    'header': header,
                    'track': track_data
                })
            else:
                # Skip lines that don't start with '66666' (shouldn't happen in valid files)
                i += 1
        
        print(f"Successfully parsed {len(self.data_blocks)} TC residual vortex blocks")
        return self.data_blocks
    
    def analyze_dataset(self) -> Dict[str, Any]:
        """
        Analyze the parsed dataset
        
        Returns:
            Dictionary containing analysis results
        """
        if not self.data_blocks:
            print("No data to analyze. Please parse a file first.")
            return {}
        
        analysis = {
            'total_blocks': len(self.data_blocks),
            'year_counts': {},
            # 新增按时长统计的字段
            'year_counts_by_duration': {
                '6h': {},   # 时长≥6小时的残涡
                '12h': {},  # 时长≥12小时的残涡
                '24h': {}   # 时长≥24小时的残涡
            },
            'stop_reason_counts': {},
            'track_length_stats': {},
            'years_covered': []
        }
        
        # Statistics for stop reasons
        stop_reason_labels = {
            0: 'No vortex feature',
            1: 'Vortex merger',
            2: 'Vortex weakening/splitting',
            3: 'Moved out of boundary'
        }
        
        # Initialize counts
        for reason_id, reason_label in stop_reason_labels.items():
            analysis['stop_reason_counts'][reason_label] = 0
        
        # Track length statistics
        track_lengths = []
        
        # Process each data block
        for block in self.data_blocks:
            header = block['header']
            track = block['track']
            track_length = len(track)  # 轨迹点数 = 时长（小时），因为时间分辨率1小时
            
            # Extract year from start date
            year = header.start_date[:4]
            
            # 基础年度计数
            analysis['year_counts'][year] = analysis['year_counts'].get(year, 0) + 1
            
            # 按时长统计年度计数
            # 6小时（≥6个轨迹点）
            if track_length >= 7:
                analysis['year_counts_by_duration']['6h'][year] = analysis['year_counts_by_duration']['6h'].get(year, 0) + 1
            # 12小时（≥12个轨迹点）
            if track_length >= 13:
                analysis['year_counts_by_duration']['12h'][year] = analysis['year_counts_by_duration']['12h'].get(year, 0) + 1
            # 24小时（≥24个轨迹点）
            if track_length >= 25:
                analysis['year_counts_by_duration']['24h'][year] = analysis['year_counts_by_duration']['24h'].get(year, 0) + 1
            
            # Count stop reasons
            reason_label = stop_reason_labels.get(header.stop_reason, 'Unknown')
            analysis['stop_reason_counts'][reason_label] += 1
            
            # Record track length
            track_lengths.append(track_length)
        
        # Calculate track length statistics
        if track_lengths:
            analysis['track_length_stats'] = {
                'min': min(track_lengths),
                'max': max(track_lengths),
                'mean': sum(track_lengths) / len(track_lengths),
                'total_points': sum(track_lengths)
            }
        
        # Get years covered
        analysis['years_covered'] = sorted(analysis['year_counts'].keys())
        
        # 补全所有年份的时长统计（确保每个年份都有记录，没有则为0）
        for year in analysis['years_covered']:
            for duration in ['6h', '12h', '24h']:
                if year not in analysis['year_counts_by_duration'][duration]:
                    analysis['year_counts_by_duration'][duration][year] = 0
        
        return analysis
    
    def get_trv_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Get all TRV residual lows with a specific name
        
        Args:
            name: TRV name to search for
            
        Returns:
            List of matching TRV data blocks
        """
        return [block for block in self.data_blocks if block['header'].name.lower() == name.lower()]
    
    def get_trv_by_year(self, year: str) -> List[Dict[str, Any]]:
        """
        Get all TRV residual lows from a specific year
        
        Args:
            year: Year to search for (YYYY format)
            
        Returns:
            List of matching TRV data blocks
        """
        return [block for block in self.data_blocks if block['header'].start_date.startswith(year)]
    
    def export_to_json(self, output_file: str) -> bool:
        """
        Export parsed data to JSON format
        
        Args:
            output_file: Path to output JSON file
            
        Returns:
            True if successful, False otherwise
        """
        if not self.data_blocks:
            print("No data to export. Please parse a file first.")
            return False
        
        try:
            # Convert to serializable format
            serializable_data = []
            for block in self.data_blocks:
                block_dict = {
                    'header': block['header']._asdict(),
                    'track': [t._asdict() for t in block['track']]
                }
                serializable_data.append(block_dict)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, ensure_ascii=False, indent=2)
            
            print(f"Data exported to {output_file}")
            return True
            
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    def export_to_csv(self, output_file: str) -> bool:
        """
        Export parsed data to simplified CSV format
        
        Args:
            output_file: Path to output CSV file
            
        Returns:
            True if successful, False otherwise
        """
        if not self.data_blocks:
            print("No data to export. Please parse a file first.")
            return False
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'TRV_Name', 'Start_Date', 'China_Code', 'Stop_Reason',
                    'Time', 'Latitude', 'Longitude', 
                    'Stream_Function', 'Vorticity', 'Velocity'
                ])
                
                # Write data
                for block in self.data_blocks:
                    header = block['header']
                    for track in block['track']:
                        writer.writerow([
                            header.name,
                            header.start_date,
                            header.china_code,
                            header.stop_reason,
                            track.time,
                            track.lat / 10.0,  # Convert to degrees
                            track.lon / 10.0,  # Convert to degrees
                            track.stream_func,
                            track.vorticity,
                            track.velocity / 10.0  # Convert to m/s
                        ])
            
            print(f"Data exported to {output_file}")
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False