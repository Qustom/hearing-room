import os
import face_recognition

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
                people_images_processing.append(image)

                photo = {
                    "filepath": img_filepath,
                    "image_id": image_id
                }

                people_images[person_id].append(photo)

    locations = face_recognition.batch_face_locations(people_images_processing)
    people_images_encodings = map(lambda img, loc: face_recognition.face_encodings(img, loc), zip(people_images_processing, locations))

    print(people_images_encodings)

    # Create list of known faces from initial set

    # Add any existing matches

    # Look at every face in the video folder

    # If it matches, add to matches and known faces
    pass


people_video_stitcher(
    r"C:\Users\qustom\source\ai-news-reader\video-analytics\people",
    r"C:\Users\qustom\source\ai-news-reader\video-analytics\output",
    "2021041286-April25",
    r"C:\Users\qustom\source\ai-news-reader\video-analytics\matches")
