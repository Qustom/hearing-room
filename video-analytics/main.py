import face_recognition
import cv2

def process_video(filename: str) -> None:
    mov = cv2.VideoCapture(filename)

    if not mov.isOpened():
        print("Failed to open file")
        return

    cv2.namedWindow('Video Life2Coding',cv2.WINDOW_AUTOSIZE)
    while True:
        ret_val, frame = mov.read()

        # Quit when no more frames
        if not ret_val:
            break

        # Convert to face_recognition format
        face_frame = frame[:, :, ::-1]

        # Get all face positions in frame
        face_pos = face_recognition.face_locations(face_frame, model="cnn")

        # Draw rectangles around faces
        for top, right, bottom, left in face_pos:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.imshow('Video Life2Coding', frame)
        
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


process_video("/home/qustom/source/ai-news-reader/video-analytics/raw_data/vid.mp4")