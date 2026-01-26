# -*- coding: utf-8 -*-
"""
TRV Analysis Utility Functions
Helper functions for printing analysis results and examples
"""

from typing import Dict, Any, List

def print_analysis_results(analysis: Dict[str, Any]):
    """
    Print analysis results in a formatted way
    
    Args:
        analysis: Analysis results dictionary
    """
    print("\n" + "=" * 80)
    print("DATASET ANALYSIS RESULTS")
    print("=" * 80)
    
    print(f"\nTotal TRV residual vortices: {analysis['total_blocks']}")
    print(f"Total track points: {analysis['track_length_stats']['total_points']}")
    
    print(f"\nAverage points per track: {analysis['track_length_stats']['mean']:.1f}")
    print(f"Min points per track: {analysis['track_length_stats']['min']}")
    print(f"Max points per track: {analysis['track_length_stats']['max']}")
    
    print(f"\nYears covered: {len(analysis['years_covered'])} years")
    print(f"From {analysis['years_covered'][0]} to {analysis['years_covered'][-1]}")
    
    print("\n" + "-" * 60)
    print("Yearly distribution (total and by duration)")
    print("-" * 60)
    # 打印年度统计表头
    print(f"{'Year':<6} {'Total':<6} {'≥6h':<6} {'≥12h':<6} {'≥24h':<6}")
    print("-" * 60)
    for year in sorted(analysis['year_counts'].keys()):
        total = analysis['year_counts'][year]
        six_h = analysis['year_counts_by_duration']['6h'][year]
        twelve_h = analysis['year_counts_by_duration']['12h'][year]
        twentyfour_h = analysis['year_counts_by_duration']['24h'][year]
        print(f"{year:<6} {total:<6} {six_h:<6} {twelve_h:<6} {twentyfour_h:<6}")
    
    print("\n" + "-" * 60)
    print("Stop reason distribution")
    print("-" * 60)
    for reason, count in sorted(analysis['stop_reason_counts'].items()):
        print(f"  {reason}: {count} TRVs")
    
    # 打印时长统计汇总
    print("\n" + "-" * 60)
    print("Overall duration statistics")
    print("-" * 60)
    total_6h = sum(analysis['year_counts_by_duration']['6h'].values())
    total_12h = sum(analysis['year_counts_by_duration']['12h'].values())
    total_24h = sum(analysis['year_counts_by_duration']['24h'].values())
    print(f"Total residual vortices ≥6 hours: {total_6h} ({total_6h/analysis['total_blocks']*100:.1f}%)")
    print(f"Total residual vortices ≥12 hours: {total_12h} ({total_12h/analysis['total_blocks']*100:.1f}%)")
    print(f"Total residual vortices ≥24 hours: {total_24h} ({total_24h/analysis['total_blocks']*100:.1f}%)")


def print_trv_example(data_blocks: List[Dict[str, Any]], index: int = 0):
    """
    Print example TRV residual vortex data
    
    Args:
        data_blocks: List of data blocks
        index: Index of the TRV to display (default: 0)
    """
    if not data_blocks:
        print("No data available")
        return
    
    if index >= len(data_blocks):
        print(f"Index {index} out of range. Max index: {len(data_blocks)-1}")
        return
    
    block = data_blocks[index]
    header = block['header']
    track_length = len(block['track'])
    
    print("\n" + "=" * 60)
    print(f"EXAMPLE TRV RESIDUAL VORTEX DATA (Index: {index})")
    print("=" * 60)
    
    print(f"\nBasic Information:")
    print(f"  Name: {header.name}")
    print(f"  International Code: {header.intl_code}")
    print(f"  Chinese Code: {header.china_code}")
    print(f"  Start Date: {header.start_date}")
    print(f"  Track Points: {header.record_count} (actual: {track_length})")
    print(f"  Duration: {track_length} hours")  # 新增时长显示
    print(f"  Meets ≥6h: {'Yes' if track_length >=6 else 'No'}")
    print(f"  Meets ≥12h: {'Yes' if track_length >=12 else 'No'}")
    print(f"  Meets ≥24h: {'Yes' if track_length >=24 else 'No'}")
    
    stop_reason_labels = {
        0: 'No vortex feature',
        1: 'Vortex merger',
        2: 'Vortex weakening/splitting',
        3: 'Moved out of boundary'
    }
    reason_text = stop_reason_labels.get(header.stop_reason, 'Unknown')
    print(f"  Stop Reason: {reason_text} ({header.stop_reason})")
    
    print(f"\nFirst 3 track points:")
    for i, track in enumerate(block['track'][:3]):
        print(f"  Point {i+1}:")
        print(f"    Time: {track.time}")
        print(f"    Position: {track.lat/10:.1f}°N, {track.lon/10:.1f}°E")
        print(f"    Stream Function: {track.stream_func} (10⁴m²/s)")
        print(f"    Vorticity: {track.vorticity} (10⁻⁵s⁻¹)")
        print(f"    Velocity: {track.velocity/10:.1f} m/s")
    
    print(f"\nLast track point:")
    last_track = block['track'][-1]
    print(f"  Time: {last_track.time}")
    print(f"  Position: {last_track.lat/10:.1f}°N, {last_track.lon/10:.1f}°E")
    print(f"  Stream Function: {last_track.stream_func} (10⁴m²/s)")
    print(f"  Vorticity: {last_track.vorticity} (10⁻⁵s⁻¹)")
    print(f"  Velocity: {last_track.velocity/10:.1f} m/s")