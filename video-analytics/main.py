import cv2
import face_recognition
import json

SKIP_FRAME_COUNT = 10
RECOG_RESIZE = 2

def process_video(filename: str) -> None:
    mov = cv2.VideoCapture(filename)

    if not mov.isOpened():
        print("Failed to open file")
        return

    known_faces = []
    timestamps = []

    # create a frame on GPU for images
    gpu_frame = cv2.cuda_GpuMat()
    skip = SKIP_FRAME_COUNT

    while True:
        ret_val, frame = mov.read()

        # Quit when no more frames
        if not ret_val:
            break

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
                        timestamps[index].append(mov.get(cv2.CAP_PROP_POS_MSEC))
            # Otherwise, add tne new encoding to the list, save image to file, and setup timestamping
            else:
                known_faces.append(face_encoding)
                img = frame[pos[0]*RECOG_RESIZE: pos[2]*RECOG_RESIZE, pos[3]*RECOG_RESIZE: pos[1]*RECOG_RESIZE]
                cv2.imwrite(f"output/face-{len(known_faces)}.png", img)
                timestamps.append([mov.get(cv2.CAP_PROP_POS_MSEC)])
            
        print(mov.get(cv2.CAP_PROP_POS_MSEC))

        if cv2.waitKey(1) == 27:
            break 

    # Save timestamp data to file
    data = {"timestamps": timestamps}
    with open(r"output\data.txt", 'w') as outfile:
        json.dump(data, outfile)

process_video(r"C:\Users\qustom\source\ai-news-reader\video-analytics\raw_data\pexal.mp4")
