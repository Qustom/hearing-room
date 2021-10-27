import os
import json
import face_recognition
import cv2

NORMALIZED_SIZE = 300
MINIMUM_FACE_DISTANCE_TO_MATCH = 0.6
RECOGNITION_UPSAMPLING = 1
RESIZE_BATCH_SIZE = 16

def resize_to_square(image, size):
    (height, width) = image.shape[:2]

    inter = cv2.INTER_AREA
    if width < size or height < size:
        inter = cv2.INTER_LINEAR


    if height == width:
        return cv2.resize(image, (size, size), interpolation=inter)
    
    if height > width:
        ratio = size / float(height)
        resized_width = int(width * ratio)
        resized_img = cv2.resize(image, (resized_width, size), interpolation=inter)
        pixels_to_add = size - resized_width
        return cv2.copyMakeBorder(resized_img, right=pixels_to_add, top=0,bottom=0,left=0, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])
        

    if height < width:
        ratio = size / float(width)
        resized_height = int(height * ratio)
        resized_img = cv2.resize(image, (size, resized_height), interpolation=inter)
        pixels_to_add = size - resized_height
        return cv2.copyMakeBorder(resized_img, bottom=pixels_to_add, top=0,right=0,left=0, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])

def get_all_encodings_in_folder(faces_folder: str) -> dict:
    filenames = []
    images = []
    file_to_encoding = {}
    for dirpath, _, files in os.walk(faces_folder):
        for file in files:
            if file[-4:] == ".png":
                filenames.append(file)
                img = resize_to_square(face_recognition.load_image_file(os.path.join(dirpath, file)), NORMALIZED_SIZE)
                images.append(img)

    locations = face_recognition.batch_face_locations(images=images, number_of_times_to_upsample=RECOGNITION_UPSAMPLING, batch_size=RESIZE_BATCH_SIZE)
    
    filtered_filenames = []
    filtered_images = []
    filtered_locations = []

    for filename, img, location in zip(filenames, images, locations):
        if location:
            filtered_filenames.append(filename)
            filtered_images.append(img)
            filtered_locations.append(location)
    
    encodings = [face_recognition.face_encodings(img, locs) for img, locs in zip(filtered_images, filtered_locations)]

    single_encodings = [encoding[0] for encoding in encodings]

    for name, encoding in zip(filtered_filenames, single_encodings):
        file_to_encoding[name] = encoding

    return file_to_encoding

def people_video_stitcher(people_file:str, people_folder: str, video_folder: str, video_id: str, matches_folder:str) -> None:
    people_image_intial_data = {}
    people_metadata = []
    people_images_processing = []
    people_images_encodings = []

    # Get the people metadata
    with open(people_file, "r") as f:
        people_metadata = json.loads(f.read())

    # For every person in the people folder
    for person_id in os.listdir(people_folder):
        if people_image_intial_data.get(person_id) is None:
            people_image_intial_data[person_id] = []

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

                people_image_intial_data[person_id] = photo

    batch_locations = face_recognition.batch_face_locations(people_images_processing)

    initial_encodings = [face_recognition.face_encodings(img, loc) for (img, loc) in zip(people_images_processing, batch_locations)]
    
    # Create list of known faces from initial set
    people_encodings = {}

    for key, img_metadata in people_image_intial_data.items():
        people_encodings[key] = initial_encodings[img_metadata["image_id"]]

    # Look at every face in the video folder
    filename_to_encoding = get_all_encodings_in_folder(os.path.join(video_folder, video_id))

    # Setup person to faces dict
    person_to_faces = {}
    for person_name in people_encodings.keys():
        person_to_faces[person_name] = []

    # If it matches, add to matches and known faces
    for face_name, face_encoding in filename_to_encoding.items():

        # Check each person if the face matches them
        person_to_face_distance = {}
        for person_name, person_encodings in people_encodings.items():
            face_distances = face_recognition.face_distance(person_encodings, face_encoding)
            best_face_distance = min(face_distances)
            person_to_face_distance[person_name] = best_face_distance

        # Assign face to person with best distance, above minium req
        best_matching_person = None
        best_matching_distance = 1.0

        for person_name, distance in person_to_face_distance.items():
            if distance <= MINIMUM_FACE_DISTANCE_TO_MATCH:
                if distance < best_matching_distance:
                    best_matching_distance = distance
                    best_matching_person = person_name

        if best_matching_person:
            person_to_faces[best_matching_person].append(face_name)

    
    # Save data to file
    data = {video_id: person_to_faces}
    with open(f"{matches_folder}\{video_id}.json", 'w') as outfile:
        json.dump(data, outfile)


people_video_stitcher(
    r"C:\Users\qustom\source\ai-news-reader\prod_data\people.json",
    r"C:\Users\qustom\source\ai-news-reader\prod_data\people",
    r"C:\Users\qustom\source\ai-news-reader\prod_data\faces",
    "2021041269-April21",
    r"C:\Users\qustom\source\ai-news-reader\prod_data\matches")
