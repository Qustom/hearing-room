import json
import os

def person_topic_sticher(people_filepath: str, matches_folder: str, timestamp_folder: str, messages_folder: str):
    # Open data
    
    # Open raw data 
    raw_people_data = []
    raw_matching_data = {}
    raw_timestamp_data = {}
    raw_message_data = {}
    
    with open(people_filepath, "r") as f:
        people_data = json.loads(f.read())

    for dirpath, _, files in os.walk(matches_folder):
        for file in files:
            with open(os.path.join(dirpath, file), "r") as f:
                raw_matching_data |= json.loads(f.read())

    timestamp_directories = os.listdir(timestamp_folder)

    for directory in timestamp_directories:
        for dirpath, _, files in os.walk(os.path.join(timestamp_folder, directory)):
            for file in files:
                if file[-5:] == ".json":
                    with open(os.path.join(dirpath, file), "r") as f:
                        raw_timestamp_data[directory] = json.loads(f.read())["timestamps"]

    for dirpath, _, files in os.walk(messages_folder):
        for file in files:
            with open(os.path.join(dirpath, file), "r") as f:
                if file == "2021041286-April25.json":
                    video_id = file.removesuffix(".json")
                    json_data = json.loads(f.read())
                    raw_message_data[video_id] =  json_data["messages"]
    

    # Data to be used
    people_data = {}
    matching_data = {}
    video_person_face_timestamp = {}
    video_to_message_data = {}


    # Format person_id => person_data
    for raw_person in raw_people_data:
        people_data[raw_person["id"]] = raw_person

    # Format and filter video_id => person_id => face_ids
    for video_id, raw_data in raw_matching_data.items():
        filtered_data = {}
        for person_name, faces in raw_data.items():
            filtered_faces = [face.removesuffix(".png") for face in faces]

            if faces:
                filtered_data[person_name] = filtered_faces

        matching_data[video_id] = filtered_data

    # Fold timestamp data into matching data
    for video_id, person_to_face_data in matching_data.items():
        timestamped_faces = raw_timestamp_data[video_id]

        person_to_faces = {}
        for person, faces in person_to_face_data.items():
            faces_to_timestamp = []
            for face in faces:
                faces_to_timestamp += timestamped_faces[face]
            faces_to_timestamp.sort()
            person_to_faces[person] = faces_to_timestamp
        
        video_person_face_timestamp[video_id] = person_to_faces


    # Filter Message data
    for video_id, raw_messages in raw_message_data.items():
        messages = []
        for raw_message in raw_messages:
            simple_message = {}
            simple_message["id"] = raw_message["id"]
            simple_message["start"] = raw_message["StartVideoTime"]
            simple_message["end"] = raw_message["EndVideoTime"]
            messages.append(simple_message)

        video_to_message_data[video_id] = messages

    # Person to message id
    
    
        


    print(video_to_message_data)

        

        



    # Get their video->faces->timestamps

    # Open each transcript
    
    # Create timespans->messages->topics

    # Find timestamps in timespans

    # Stitch people to topics

    pass


person_topic_sticher(
    r"C:\Users\qustom\source\ai-news-reader\prod_data\people.json",
    r"C:\Users\qustom\source\ai-news-reader\prod_data\matches",
    r"C:\Users\qustom\source\ai-news-reader\prod_data\faces",
    r"C:\Users\qustom\source\ai-news-reader\prod_data\messages"
)