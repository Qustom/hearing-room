import cv2
import face_recognition
import json
import os

# Some variables to speed up processing
# Number of frame skips until processing images
SKIP_FRAME_COUNT = 60 # Higher faster, less data
# How much times to shrink the image for processing
RECOG_RESIZE = 1 # Higher faster, less accurate, Minimum of 1. Whole Number.

def process_video(filename: str, output_folder:str) -> None:
    mov = cv2.VideoCapture(filename)

    if not mov.isOpened():
        print("Failed to open file")
        return

    known_faces = []
    timestamps = {}

    # create a frame on GPU for resizing images
    gpu_frame = cv2.cuda_GpuMat()
    skip_processing = 0

    while True:
        ret_val, frame = mov.read()

        # Quit when no more frames
        if not ret_val:
            break

        # Skip some frames
        if skip_processing == 0:
            skip_processing = SKIP_FRAME_COUNT

            # send frame to GPU for resize
            gpu_frame.upload(frame)
            gpu_small = cv2.cuda.resize(gpu_frame,(0, 0), fx=1/RECOG_RESIZE, fy=1/RECOG_RESIZE)
            small_frame = gpu_small.download()

            # Convert to face_recognition format
            face_frame = small_frame[:, :, ::-1]

            # Get all face positions and encodings in frame
            face_pos = face_recognition.face_locations(face_frame, model="cnn")
            face_encodings = face_recognition.face_encodings(face_frame, face_pos)

            # Check each face found
            for face_encoding, pos in zip(face_encodings, face_pos):
                matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.60)

                # If there are any matches to a previous encoding, then append the timestamp for it
                if any(matches):
                    for index, match in enumerate(matches):
                        if match:
                            timestamps[f"face-{index}"].append(mov.get(cv2.CAP_PROP_POS_MSEC))
                # Otherwise, add tne new encoding to the list, save image to file, and setup timestamping
                else:
                    img_name = f"face-{len(known_faces)}"
                    known_faces.append(face_encoding)
                    img = frame[pos[0]*RECOG_RESIZE: pos[2]*RECOG_RESIZE, pos[3]*RECOG_RESIZE: pos[1]*RECOG_RESIZE]
                    cv2.imwrite(f"{output_folder}/{img_name}.png", img)
                    timestamps[img_name] = [mov.get(cv2.CAP_PROP_POS_MSEC)]
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


process_all(r"C:\Users\qustom\source\ai-news-reader\video-analytics\raw_data", r"C:\Users\qustom\source\ai-news-reader\video-analytics\output")

#process_video(r"C:\Users\qustom\source\ai-news-reader\video-analytics\raw_data\vid.mp4", "output")
