import pymysql
import cv2
import numpy as np
from ultralytics import YOLO

# Database connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'raghu14',
    'database': 'my_database'
}

def create_table():
    # Connect to MySQL server
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Create a table to store image data
            create_table_query = """
            CREATE TABLE IF NOT EXISTS images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_data LONGBLOB NOT NULL,
                description TEXT UNIQUE,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            
            
            create_table_query1 = """
            CREATE TABLE IF NOT EXISTS data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                total_defects_in_cam_1 INT,
                total_defects_in_cam_2 INT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """
            cursor.execute(create_table_query1)
            # Commit the changes
            connection.commit()
            print("Table for storing image and data created successfully.")

    finally:
        # Close the connection
        connection.close()

def delete_oldest_images():
    # Connect to MySQL server
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Count the total number of images
            count_query = "SELECT COUNT(*) FROM images"
            cursor.execute(count_query)
            total_images = cursor.fetchone()[0]

            # If there are more than 500 images, delete the oldest ones
            if total_images > 500:
                # Calculate how many images need to be deleted
                images_to_delete = total_images - 500
                
                # Delete the oldest images
                delete_query = """
                DELETE FROM images 
                ORDER BY updated_at ASC 
                LIMIT %s
                """
                cursor.execute(delete_query, (images_to_delete,))
                
                # Commit the changes
                connection.commit()
                print(f"Deleted {images_to_delete} oldest images.")

    finally:
        # Close the connection
        connection.close()

def upload_image(image_frame, description):
    # Connect to MySQL server
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # Encode the image frame to a JPEG format in memory
            _, buffer = cv2.imencode('.jpg', image_frame)
            image_data = buffer.tobytes()

            # Insert or update image data and description into the table
            insert_query = """
            INSERT INTO images (image_data, description)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                image_data = VALUES(image_data),
                updated_at = CURRENT_TIMESTAMP;
            """
            cursor.execute(insert_query, (image_data, description))
            
            # Commit the changes
            connection.commit()
            print("Image uploaded successfully.")

            # Delete oldest images if there are more than 500
            delete_oldest_images()

    finally:
        # Close the connection
        connection.close()

def retrieve_image(description, output_path):
    # Connect to MySQL server
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Retrieve the image data based on the description
            select_query = "SELECT image_data FROM images WHERE description = %s"
            cursor.execute(select_query, (description,))
            result = cursor.fetchone()

            if result:
                # Save the retrieved image to a file 
                with open(output_path, 'wb') as file:
                    file.write(result[0])
                print(f"Image retrieved and saved to {output_path}.")
            else:
                print("No image found with the given description.")

    finally:
        # Close the connection
        connection.close()
        
        
def upload_data(total_defective_bearings_per_sec_1,total_defective_bearings_per_sec_2): 
    
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:

            insert_query = """
            INSERT INTO data (total_defects_in_cam_1 , total_defects_in_cam_2)
            VALUES (%s , %s)
            ON DUPLICATE KEY UPDATE
                updated_at = CURRENT_TIMESTAMP;
                
            """
            cursor.execute(insert_query, ( total_defective_bearings_per_sec_1 , total_defective_bearings_per_sec_2))
            
            # Commit the changes
            connection.commit()
            print("Image uploaded successfully.")

            # Delete oldest images if there are more than 500
            delete_oldest_images()

    finally:
        # Close the connection
        connection.close()


# Example usage to create the table

# Example usage to upload an image and maintain the last 500 images
# image_frame = ...  # Your image frame from OpenCV
# description = 'Sample image description'
# upload_image(image_frame, description)

# Example usage to retrieve and save an image
# output_image_path = 'retrieved_image.jpg'  # Replace with the desired output path
# retrieve_image(description, output_image_path)
