# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 12:23:54 2024

@author: SouravMukherjee
"""

import subprocess
import os

wepp_id = 1

# Define the path to the .exe file
exe_path = "C:/Users/souravmukherjee.USDA/Box/external EFR Study_Extreme Precip_DesignFlood/3rd Phase_Geomorphological Assessment/Data/WEPP/Run/wepppy-win-bootstrap.exe"

# Get the directory containing the .exe file
runs_dir = os.path.abspath(os.path.dirname(exe_path))

# Loop through the range of i values (1 to 202)
for i in range(1, 203):
    # Construct the filenames
    slope_filename = f"culvert_hillslope_{i}.slp"
    soil_loss_filename = f"soil_loss_{i}"
    sediment_loss_filename = f"sediment_loss_{i}"
    summary_filename = f"summary_{i}"

    # List of inputs to send to the .exe file
    inputs = [
        'm', 'y', 1, 1, 'n', 2, 'n',
        soil_loss_filename, 'n', 'n', 'n', 'y',
        sediment_loss_filename, 'n', 'n', 'n', 'y',
        summary_filename, 'n', 'n', 'management.man',
        slope_filename, 'climate_hbref_gridmet.cli', 'soil.sol',
        0, 44, 0
    ]

    # Write inputs to a temporary run file
    with open(os.path.join(runs_dir, f'p{i}.run'), 'w') as fp:
        fp.write('\n'.join(str(arg) for arg in inputs))

    # Execute the .exe file
    _run = open(os.path.join(runs_dir, f'p{i}.run'))
    _log = open(os.path.join(runs_dir, f'p{i}.err'), 'w')
    p = subprocess.Popen(os.path.abspath(exe_path), stdin=_run, stdout=_log, stderr=_log, cwd=runs_dir)
    p.wait()
    _run.close()
    _log.close()

    # Read the log file
    log_fn = os.path.join(runs_dir, f'p{i}.err')
    with open(log_fn) as fp:
        print(fp.read())
