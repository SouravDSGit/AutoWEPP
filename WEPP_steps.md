# WEPP Watershed Processing Tool (Optimized Docker Implementation)

This tool provides a complete workflow for processing watershed data using the Water Erosion Prediction Project (WEPP) model. It automates the preparation of geospatial inputs, runs the WEPP model through Wine in Docker, and processes the outputs into GIS-ready formats.

## Overview

The tool takes geospatial data representing a watershed (hillslopes, streams, soils, land cover, and elevation) and performs the following:

1. Processes each data source into WEPP-compatible input files
2. Fetches climate data for each hillslope location using PyGridMET
3. Runs the Windows version of WEPP through Wine in Docker
4. Parses the model outputs
5. Returns the results as GeoDataFrames with erosion metrics attached to the original geometries

## Optimized Docker Implementation

This tool is designed to run in a Docker container with performance optimizations for processing large watersheds:

- Ubuntu Linux as the base operating system
- Wine for running the Windows version of WEPP
- 8GB memory allocation for large datasets
- 4 CPU cores for parallel processing
- Named volumes for better I/O performance
- Tmpfs in-memory filesystem for temporary files
- Increased shared memory (2GB) for improved performance
- Python with optimized geospatial libraries

### Key Environment Variables

The Docker container sets up these environment variables:

- `WEPP_PATH`: Path to the WEPP executable inside the container
- `WINE_PATH`: Path to the Wine executable for running Windows programs

## Workflow

### 1. Initial Setup

- Creates the necessary directory structure for inputs, outputs, and intermediates
- Reads in all geospatial data (shapefiles and rasters)
- Ensures all data are in the same coordinate reference system
- Sets default date ranges for climate data if not provided

### 2. Climate Data Acquisition

For each hillslope:

- Determines the centroid coordinates of the hillslope
- Uses PyGridMET to fetch gridded climate data for those coordinates
- Downloads key climate variables: precipitation, temperature, humidity, wind speed, solar radiation
- Converts GridMET data to WEPP climate file format including:
  - Monthly statistics (mean precipitation, wet day probability, temperature range)
  - Temperature and precipitation distributions

### 3. Hillslope Processing (Parallelized)

The tool can process multiple hillslopes in parallel using a thread pool:

```python
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = {}
    for idx, hillslope in hillslopes.iterrows():
        futures[executor.submit(process_single_hillslope, ...)] = idx

    for future in concurrent.futures.as_completed(futures):
        # Process results
```

For each hillslope:

- Identifies the corresponding channel segment
- Processes DEM data to extract slope profile information:
  - Clips the DEM to the hillslope boundary
  - Calculates length and average slope
  - Creates WEPP slope input file
- Analyzes soil data:
  - Identifies soils intersecting with the hillslope
  - Determines dominant soil by area
  - Extracts soil properties (texture, sand/clay percentage, organic matter)
  - Creates WEPP soil input file
- Processes land cover data:
  - Clips NLCD raster to hillslope boundary
  - Identifies dominant land cover class
  - Maps NLCD classes to WEPP management types
  - Creates appropriate WEPP management file based on land cover type

### 4. Running WEPP Model

For each hillslope:

- Creates a complete WEPP input file that references:
  - Slope file
  - Soil file
  - Management file
  - Climate file
  - Output destinations
  - Simulation parameters
- Executes the WEPP model via subprocess using Wine:
  ```python
  subprocess.run([wine_path, wepp_path], stdin=infile, stdout=subprocess.PIPE)
  ```
- Captures and logs any errors
- Organizes output files by hillslope and channel

### 5. Output Processing

- Parses WEPP output files to extract key results
- Processes hillslope and channel results separately
- Handles both regular outputs and time series data

### 6. Results Integration with GIS

- Reads original watershed boundaries
- Adds result columns to the GeoDataFrames
- Performs spatial joins to associate hillslopes and channels with parent watersheds
- Calculates aggregate statistics for each watershed
- Saves results as GeoPackage files that can be opened in GIS software

### 7. Summary Report Generation

- Creates CSV summary files for hillslopes, channels, and watersheds
- Calculates watershed-level statistics
- Generates a comprehensive text report with all key findings

## Optimized Storage Configuration

The Docker setup uses three different storage mechanisms for optimal performance:

1. **Bind Mounts for Code**: Application code is mounted directly from the host for easy development

   ```yaml
   volumes:
     - ./:/app
     - ./utils:/app/utils
   ```

2. **Named Volume for Data**: Persistent data uses a Docker volume for better I/O performance

   ```yaml
   volumes:
     - wepp_data:/app/data
   ```

3. **Tmpfs for Temporary Files**: Fast in-memory filesystem for processing files
   ```yaml
   volumes:
     - type: tmpfs
       target: /app/data/temp
       tmpfs:
         size: 2g
   ```

## Data Requirements

- **Hillslope Shapefile**: Polygons representing hillslope boundaries
- **Stream Shapefile**: Lines representing the stream network
- **Soil Shapefile**: Polygons with soil properties from GSSURGO or similar
- **NLCD Raster**: Land cover classification raster
- **DEM Raster**: Digital Elevation Model
- **Watershed Shapefile**: Polygons delimiting watershed boundaries
- **WEPP Executable**: Windows version of WEPP (run through Wine)

## Output Products

- **GeoDataFrames**: Three GeoDataFrames containing the original geometries with erosion results
- **GeoPackage Files**: GIS-ready files with erosion results attached as attributes
- **CSV Summaries**: Summary statistics for hillslopes, channels, and watersheds
- **WEPP Output Files**: Raw WEPP output files for detailed analysis
- **Summary Report**: Text report with key findings and watershed statistics

## Processing Details

The tool handles several complex processes behind the scenes:

- **Hillslope-Channel Association**: Automatically matches hillslopes to their corresponding channels
- **Climate Data Processing**: Converts gridded climate data to WEPP's specific format
- **Land Cover Classification**: Maps NLCD classes to appropriate WEPP management parameters
- **Soil Property Extraction**: Identifies and extracts relevant soil properties for erosion modeling
- **Error Handling**: Manages WEPP execution errors and provides meaningful feedback
- **Spatial Integration**: Performs spatial operations to associate results with their geographic context
- **Wine Integration**: Handles running Windows executables in Linux through Wine
- **Parallel Processing**: Distributes work across multiple CPU cores for faster execution

## Performance Monitoring and Tuning

You can monitor the performance of the WEPP processing with:

```bash
docker stats culvert-web-app
```

If processing is still slow, you can:

1. Increase memory allocation in `docker-compose.yml`
2. Adjust the number of worker threads based on your CPU cores
3. Ensure the most intensive operations (raster clipping, file I/O) use the optimized storage locations
4. Consider streaming large files instead of loading them entirely into memory

This workflow allows for efficient, automated watershed-scale erosion modeling with minimal manual intervention, producing GIS-ready outputs that can be immediately visualized and analyzed, all within a consistent and optimized Docker environment.
