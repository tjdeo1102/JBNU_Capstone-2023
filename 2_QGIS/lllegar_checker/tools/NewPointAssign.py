from osgeo import gdal, osr
import os

def add_coordinates_to_output(original_tif_folder, output_tif_folder):
    original_tif_files = [f for f in os.listdir(original_tif_folder) if f.endswith('.tif')]
    output_tif_files = [f for f in os.listdir(output_tif_folder) if f.endswith('.tif')]

    for original_tif_file in original_tif_files:
        original_tif_path = os.path.join(original_tif_folder, original_tif_file)
        
        # Find matching output file based on match
        matching_output_files = [output_file for output_file in output_tif_files if original_tif_file == output_file]
            
        if not matching_output_files:
            # If no matching output file is found, continue to the next original file
            continue

        # Assuming there is only one matching output file, take the first one
        matching_output_file = matching_output_files[0]
        output_tif_path = os.path.join(output_tif_folder, matching_output_file)

        # Open the original TIF file
        original_dataset = gdal.Open(original_tif_path)

        # Open the output TIF file
        output_dataset = gdal.Open(output_tif_path, gdal.GA_Update)

        # Get the geotransform information from the original TIF
        geotransform = original_dataset.GetGeoTransform()

        # Get spatial reference information
        spatial_reference = original_dataset.GetSpatialRef()

        # Check if the output TIF already has geotransform information
        if output_dataset.GetGeoTransform() == (0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
            # If no geotransform information is present, set it using the original TIF's geotransform
            output_dataset.SetGeoTransform(geotransform)
            # Set the new Spatial Reference to the dataset
            output_dataset.SetSpatialRef(spatial_reference)
        

        # Close the datasets
        original_dataset = None
        output_dataset = None
    print("좌표 부여 완료")
