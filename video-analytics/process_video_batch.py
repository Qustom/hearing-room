import cv2
import face_recognition
import json
import os

# Some variables to speed up processing
# Number of frame skips until processing images
SKIP_FRAME_COUNT = 60 # Higher faster, less data

# Size to batch processing
BATCH_SIZE = 16

def process_video(filename: str, output_folder:str) -> None:
    mov = cv2.VideoCapture(filename)

    if not mov.isOpened():
        print("Failed to open file")
        return

    known_faces = []
    timestamps = {}
    batch_face_frames = []
    batch_frames = []
    batch_frame_count = 0
    batch_frame_timestamp = []

    skip_processing = 0

    while mov.isOpened():
        ret_val, frame = mov.read()

        # Quit when no more frames
        if not ret_val:
            break

        # Skip some frames
        if skip_processing == 0:
            skip_processing = SKIP_FRAME_COUNT

            # Convert to face_recognition format
            face_frame = frame[:, :, ::-1]

            batch_face_frames.append(face_frame)
            batch_frames.append(frame)
            batch_frame_timestamp.append(int(mov.get(cv2.CAP_PROP_POS_MSEC)))

            if len(batch_face_frames) == BATCH_SIZE:
                batch_face_locations = face_recognition.batch_face_locations(batch_face_frames, number_of_times_to_upsample=0)

                for batch_frame_number, face_locations in enumerate(batch_face_locations):
                    face_encodings = face_recognition.face_encodings(batch_face_frames[batch_frame_number], face_locations)
                    for pos, face_encoding in zip(face_locations, face_encodings):
                        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.60)

                        # If there are any matches to a previous encoding, then append the timestamp for it
                        if any(matches):
                            for index, match in enumerate(matches):
                                if match:
                                    timestamps[f"face-{index}"].append(batch_frame_timestamp[batch_frame_number])
                        else:
                            img_name = f"face-{len(known_faces)}"
                            known_faces.append(face_encoding)
                            img = batch_frames[batch_frame_number][pos[0]: pos[2], pos[3]: pos[1]]
                            cv2.imwrite(f"{output_folder}/{img_name}.png", img)
                            timestamps[img_name] = [batch_frame_timestamp[batch_frame_number]]
                
                batch_frame_number = 0
                batch_frame_count = 0
                batch_face_frames.clear()
                batch_face_locations.clear()
                batch_frame_timestamp.clear()
                batch_frames.clear()
            batch_frame_count += 1
        else:
            skip_processing -= 1
        print(f"Time (MSEC): {mov.get(cv2.CAP_PROP_POS_MSEC)}")

        if cv2.waitKey(1) == 27:
            break 

    # Save timestamp data to file
    data = {"timestamps": timestamps}
    with open(f"{output_folder}\data.json", 'w') as outfile:
        json.dump(data, outfile)

def process_all(intake_folder: str, output_folder: str) -> None:
    files = os.listdir(intake_folder)
    for file in files:
        output_path = output_folder + "\\" + file.removesuffix(".mp4")
        os.mkdir(output_path)
        process_video(intake_folder + "\\" + file, output_path)
