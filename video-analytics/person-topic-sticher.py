import json
import os

def person_topic_sticher(people_filepath: str, matches_folder: str, timestamp_folder: str, messages_folder: str, topics_folder: str, video_metadata_file: str, output_folder:str):
    # Open data
    
    # Open raw data 
    raw_people_data = []
    raw_matching_data = {}
    raw_timestamp_data = {}
    raw_message_data = {}
    raw_topics_data = []
    raw_video_data = []
    
    with open(people_filepath, "r") as f:
        raw_people_data = json.loads(f.read())

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
            with open(os.path.join(dirpath, file), "r", encoding="utf-16") as f:
                video_id = file.removesuffix(".json")
                raw_string = f.read()
                json_data = json.loads(raw_string)
                raw_message_data[video_id] =  json_data["messages"]

    for dirpath, _, files in os.walk(topics_folder):
        for file in files:
            with open(os.path.join(dirpath, file), "r") as f:
                video_id = file.removesuffix(".json")
                json_data = json.loads(f.read())
                raw_topics_data.append(json_data["topics"])


    with open(video_metadata_file, "r") as f:
        raw_video_data = json.loads(f.read())["videos"]

    # Data to be used
    people_data = {}
    matching_data = {}
    video_person_timestamp = {}
    video_to_message_data = {}
    video_metadata = {}


    # Format person_id => person_data
    for raw_person in raw_people_data:
        people_data[raw_person["id"]] = raw_person

    for raw_vid_meta in raw_video_data:
        video_metadata[raw_vid_meta["id"]] = raw_vid_meta

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
        
        video_person_timestamp[video_id] = person_to_faces


    # Filter Message data
    for video_id, raw_messages in raw_message_data.items():
        messages = []
        for raw_message in raw_messages:
            simple_message = {}
            simple_message["video_id"] = video_id
            simple_message["id"] = raw_message["id"]
            simple_message["start"] = int(raw_message["StartVideoTime"])
            simple_message["end"] = int(raw_message["EndVideoTime"])
            messages.append(simple_message)

        video_to_message_data[video_id] = messages

    # Person to message id

    is_in_msg = lambda time, msg: msg["start"] < time and time <= msg["end"]
    
    person_messages = {}

    for video_id, person_timestamp_data in video_person_timestamp.items():
        video_messages = video_to_message_data[video_id]

        for person, timestamp_data in person_timestamp_data.items():
            for time in timestamp_data:
                for message in video_messages:
                    if is_in_msg(time, message):
                        if person_messages.get(person):
                            person_messages[person].append(message)
                        else:
                            person_messages[person] = [message]

    message_id_to_topic = {}
    for video_topics in raw_topics_data:
        for topic in video_topics:
            for messageId in topic["messageIds"]:
                message_id_to_topic[messageId] = {"topic": topic["text"], "score": topic["score"]}


    person_to_topics = {}
    for person, messages in person_messages.items():
        for message in messages:
            topic = message_id_to_topic.get(message["id"], None)

            if topic:
                personalized_topic = topic.copy()
                personalized_topic["start_time"] = message["start"]
                personalized_topic["video_id"] = message["video_id"]
                if person_to_topics.get(person):
                    person_to_topics[person].append(personalized_topic)
                else:
                    person_to_topics[person] = [personalized_topic]
        
    person_to_topics_refined = {}

    for person_id, topics in person_to_topics.items():

        # Filter 
        topics_filtered = {}
        for topic in topics:
            filter_key = topic["video_id"] + topic["topic"]
            current_topic = topics_filtered.get(filter_key, None)
            if current_topic:
                if current_topic["start_time"] > topic["start_time"]:
                    topics_filtered[filter_key] = topic
            else:
                topics_filtered[filter_key] = topic

        # Add metadata
        topics_refined = []
        for topic in topics_filtered.values():
            metadata = video_metadata[topic["video_id"]]
            topic["video_name"] = metadata["name"]
            topic["url"] = metadata["url"]
            topic["timestamped_url"] = metadata["url"] + "&startStreamAt=" + str(int(topic["start_time"] / 1000))
            topics_refined.append(topic)

        person_to_topics_refined[person_id] = topics_refined

    final_result = []

    for person_id, person_data in people_data.items():
        final_result_row = person_data.copy()
        topics_data = person_to_topics_refined.get(person_id, None)
        if topics_data:
            final_result_row["topics"] = topics_data
            final_result.append(final_result_row)


    # Save data to file
    data = final_result
    with open(f"{output_folder}\\results.json", 'w') as outfile:
        json.dump(data, outfile)
