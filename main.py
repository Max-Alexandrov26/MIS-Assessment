import os
import shutil
from complimentary_functions import generate_footprint_and_overlay,generate_geojson
from model import get_predictions
def main(input_repository):
    # Get predictions from YOLO
    get_predictions(input_repository)
    #Select the latest run 
    number_of_runs = len(os.listdir('YOLO_predictions'))
    if number_of_runs !=1:
        path_to_yolo_images = 'YOLO_predictions\Latest_run'+str(number_of_runs)
        path_to_yolo_labels = 'YOLO_predictions\Latest_run'+str(number_of_runs)+'/labels'
    else:
        path_to_yolo_images = 'YOLO_predictions\Latest_run'
        path_to_yolo_labels = 'YOLO_predictions\Latest_run/labels'
    #generate footprints and overlaid images
    generate_footprint_and_overlay(path_to_yolo_images,path_to_yolo_labels)
    print("Footprint generated for images in: 'footprints'")
    print("Overlay generated for images in: 'overlays'")
    #Make the GEOJSON directory
    json_directory = 'GEOJSON_files'
    if not os.path.exists(json_directory):
            os.makedirs(json_directory)
    else:
            shutil.rmtree(json_directory)
            os.makedirs(json_directory)
    # Process each txt file
    for txt_file in os.listdir(path_to_yolo_labels):
        if txt_file.endswith(".txt"):
            txt_file_path = os.path.join(path_to_yolo_labels, txt_file)
            # Generate GeoJSON
            geojson_output_dir = json_directory+'/'+ txt_file + ".geojson"
            generate_geojson(txt_file_path, geojson_output_dir)
    print("GeoJSON file generated in: 'GEOJSON_files'")


main('halves')
    