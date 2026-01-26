# Data Directory

This directory is intended to store TRV (Tropical Cyclone Residual Vortex) CSV data files.

## File Requirements
- File format: CSV
- Time range: 1980-2024
- Time resolution: 1 hour
- Spatial range: 15°N-55°N, 95°E-140°E (within 200km of Chinese mainland)

## File Naming Convention
Recommended: `trv_<start_year><end_year>.csv` (e.g., `trv_1980_2024.csv`)

## Data Format
Each TRV record consists of:
1. Header line (starts with '66666'): flag, intl_code, record_count, sequence_num, china_code, stop_reason, name, start_date
2. Track data lines: time, lat, lon, stream_func, vorticity, velocity

