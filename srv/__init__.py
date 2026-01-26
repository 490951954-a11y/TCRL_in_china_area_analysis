# -*- coding: utf-8 -*-
"""
TRV (Typhoon Remnant Vortice) Analysis Package
Author: Anonymous
Version: 1.0.0
Description: Parse and analyze TRVs tracking data (1980-2024)
"""

from .trv_parser import TRVParser
from .analysis_utils import print_analysis_results, print_trv_example

__all__ = ['TRVParser', 'print_analysis_results', 'print_trv_example']
__version__ = '1.0.0'