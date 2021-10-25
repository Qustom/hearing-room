
        # Load Model
        #model = cv2.dnn.readNetFromCaffe("model/opencv_face_detector.prototxt", 
        #    caffeModel="model/res10_300x300_ssd_iter_140000.caffemodel")

        # Enable Cuda
        #model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        #model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        # Process Frame
        #face_blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0),
        #swapRB = False, crop = False)

        #model.setInput(face_blob)
        #predictions = model.forward()

        # Check all predictions
        #for i in range(0, predictions.shape[2]):
            # Check if the prediction passes the confidence threshold
        #    if predictions[0,0,i,2] > DETECTION_CONFIDENCE:
        #        # Create rectangle if it does, scale normalized pos to window
        #        box = predictions[0,0,i,3:7] * np.array([width, height, width, height])
        #        (left, top, right, bottom) = box.astype("int")
                # Image, Position, color, thickness
        #        cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)