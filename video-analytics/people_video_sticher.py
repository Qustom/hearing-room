import os
import face_recognition
import cv2

NORMALIZED_SIZE = 300

def resize_to_square(image, size):
    (height, width) = image.shape[:2]

    if height == width:
        return cv2.resize(image, (size, size), interpolation=cv2.INTER_AREA)
    
    if height > width:
        ratio = size / float(height)
        resized_width = int(width * ratio)
        resized_img = cv2.resize(image, (resized_width, size), interpolation=cv2.INTER_AREA)
        pixels_to_add = size - resized_width
        return cv2.copyMakeBorder(resized_img, right=pixels_to_add, top=0,bottom=0,left=0, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])
        

    if height < width:
        ratio = size / float(width)
        resized_height = int(height * ratio)
        resized_img = cv2.resize(image, (size, resized_height), interpolation=cv2.INTER_AREA)
        pixels_to_add = size - resized_height
        return cv2.copyMakeBorder(resized_img, bottom=pixels_to_add, top=0,right=0,left=0, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])

def people_video_stitcher(people_folder: str, video_folder: str, video_id: str, matches_folder:str) -> None:
    people_images = {}
    people_images_processing = []
    people_images_encodings = []

    # For every person in the people folder
    for person_id in os.listdir(people_folder):
        if people_images.get(person_id) is None:
            people_images[person_id] = []

        for dirpath, _, img_files in os.walk(os.path.join(people_folder, person_id)):
            for img_file in img_files:
                img_filepath = os.path.join(dirpath, img_file)
                image = face_recognition.load_image_file(img_filepath)

                image_id = len(people_images_processing)
                people_images_processing.append(resize_to_square(image, NORMALIZED_SIZE))

                photo = {
                    "filepath": img_filepath,
                    "image_id": image_id
                }

                people_images[person_id].append(photo)

    batch_locations = face_recognition.batch_face_locations(people_images_processing)

    for img, batch_location in zip(people_images_processing, batch_locations):
        print(batch_location)


    # Create list of known faces from initial set

    # Add any existing matches

    # Look at every face in the video folder

    # If it matches, add to matches and known faces
    pass


people_video_stitcher(
    r"C:\Users\qustom\source\ai-news-reader\prod_data\people",
    r"C:\Users\qustom\source\ai-news-reader\prod_data\faces",
    "2021041286-April25",
    r"C:\Users\qustom\source\ai-news-reader\prod_data\matches")
