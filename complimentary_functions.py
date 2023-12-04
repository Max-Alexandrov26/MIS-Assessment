import cv2
import os
import numpy as np
import json


def generate_footprint_and_overlay(image_directory_path,txt_directory_path):
    #Define a fucntion that draws rectangles on a black image with the same coordinates as the predcited building locations
    def draw_boxes(image_size, box_coordinates, output_path):
        # Create a black image
        image = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)
        #extract the YOLO predictions
        for box in box_coordinates:
            class_label,x_center, y_center, box_width, box_height = box
            if class_label in [0, 3]:
                x_min = int((x_center - box_width / 2) * image_size[0])
                y_min = int((y_center - box_height / 2) * image_size[1])
                x_max = int((x_center + box_width / 2) * image_size[0])
                y_max = int((y_center + box_height / 2) * image_size[1])

                # Draw a filled white rectangle on the image. White for buildings, red for rubble
                if class_label == 0:
                    colour = (255,255,255)
                else:
                    colour = (0,0,255)
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), colour, -1)

        # Save the result
        cv2.imwrite(output_path, image)

    def read_box_coordinates(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Extract box coordinates from all lines
        box_coordinates = [list(map(float, line.split())) for line in lines]

        return box_coordinates


    # Output directories for footprints and overlaid images
    footprint_directory = 'footprints'
    overlay_directory = 'overlays'
    if not os.path.exists(footprint_directory):
        os.makedirs(footprint_directory)
    if not os.path.exists(overlay_directory):
        os.makedirs(overlay_directory)

    # Iterate through each TXT file in the directory
    for txt_file in os.listdir(txt_directory_path):
        if txt_file.endswith(".txt"):
            # Read box coordinates from the TXT file
            txt_file_path = os.path.join(txt_directory_path, txt_file)
            txt_file_name = os.path.splitext(os.path.basename(txt_file_path))[0]

      # Search for an image with the same name in the image directory
        for image_file in os.listdir(image_directory_path):
          if image_file.startswith(txt_file_name) and (image_file.lower().endswith('.jpeg') or image_file.lower().endswith('.jpg')):
            # Combine the image file path and the output directory
            image_path = os.path.join(image_directory_path, image_file)

            # Read the image and save it with the desired output name
            image = cv2.imread(image_path)
            image_height, image_width, _ = image.shape
            box_coordinates = read_box_coordinates(txt_file_path)

            # Define the image size
            image_size = (image_width, image_height)

            # Draw filled white or red boxes on a black image
            footprint_path = os.path.join(footprint_directory, txt_file.replace(".txt", "_output.png"))
            draw_boxes(image_size, box_coordinates, footprint_path)
            overlay_path = os.path.join(overlay_directory, txt_file.replace(".txt", "_overlay.png"))
            overlay_images(image_path, footprint_path,overlay_path)


def generate_geojson(yolo_filepath, geojson_filepath):
        with open(yolo_filepath, 'r') as yolo_file:
            yolo_data = yolo_file.readlines()

        features = []

        for line in yolo_data:
            # Extracting class, x_center, y_center, box_width, box_height from YOLO format
            class_id, x_center, y_center, box_width, box_height = map(float, line.strip().split(' '))

            # Check if the class is of interest (class 0 or class 3)
            if class_id in [0, 3]:
                # Converting YOLO coordinates to GeoJSON coordinates
                min_x = x_center - box_width / 2
                min_y = y_center - box_height / 2
                max_x = x_center + box_width / 2
                max_y = y_center + box_height / 2

                # Set damage property based on class
                damage_property = 'none' if class_id == 0 else 'destroyed'
                object = 'building' if class_id == 0 else 'rubble'
                # Creating GeoJSON feature
                feature = {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [min_x, min_y],
                            [max_x, min_y],
                            [max_x, max_y],
                            [min_x, max_y]
                        ]
                    },
                    'properties': {
                        'class': object,
                        'damage': damage_property
                    }
                }

                features.append(feature)

        # Creating GeoJSON feature collection
        geojson_data = {
            'type': 'FeatureCollection',
            'features': features
        }

        # Writing to GeoJSON file
        with open(geojson_filepath, 'w') as geojson_file:
            json.dump(geojson_data, geojson_file, indent=2)

def overlay_images(image_path1, image_path2,output_path, alpha=0.7):
    # Load the two images
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    # Specify the weight for each image in the overlay 
    beta = 1 - alpha

    # Perform the overlay by blending the two images
    overlay = cv2.addWeighted(image1, alpha, image2, beta, 0)

    # Save the result
    cv2.imwrite(output_path, overlay)





