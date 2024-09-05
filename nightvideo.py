from ultralytics import YOLO
import cv2
import cvzone
import math
import time

def process_frame(frame: cv2.Mat, mask: cv2.Mat, model) -> (cv2.Mat, bool):
    # Apply the mask to the frame
    imgRegion = cv2.bitwise_and(frame, mask)

    # Perform object detection
    results = model(imgRegion)

    # Initialize counters
    car_count = 0
    motorbike_count = 0
    truck_count = 0
    bus_count = 0

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck"]
    vehicle_detected = False

    for result in results:
        boxes = result.boxes

        for box in boxes:
            # Extract bounding box coordinates
            bbox = box.xyxy[0].tolist()
            if len(bbox) < 4:
                print(f"Unexpected bbox length: {len(bbox)}")
                continue

            x1, y1, x2, y2 = bbox
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100

            # Class name
            cls = int(box.cls[0])
            if 0 <= cls < len(classNames):
                currentClass = classNames[cls]
            else:
                print(f"Class index out of range: {cls}")
                continue

            # Count relevant objects and set vehicle detected flag
            if currentClass == 'car':
                car_count += 1
                vehicle_detected = True
            elif currentClass == 'motorbike':
                motorbike_count += 1
                vehicle_detected = True
            elif currentClass == 'truck':
                truck_count += 1
                vehicle_detected = True
            elif currentClass == 'bus':
                bus_count += 1
                vehicle_detected = True

            # Draw bounding boxes and labels
            if currentClass in ['car', 'motorbike', 'truck', 'bus']:
                cvzone.cornerRect(frame, (x1, y1, w, h), l=10)
                cvzone.putTextRect(frame, f'{currentClass} {conf}', (max(0, x1), max(40, y1)), scale=0.6, thickness=1, offset=3)

    # Display counts on the frame
    count_text = f"Cars: {car_count}, Motorbikes: {motorbike_count}, Trucks: {truck_count}, Buses: {bus_count}"
    cv2.putText(frame, count_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    return frame, vehicle_detected

def process_video(frame_skip: int = 12) -> None:
    video_path = "Videos/nightvideo.mp4"
    mask_path = "images/5mask.png"
    model_path = "yolo weights/yolov8x.pt"
    # Load YOLO model
    model = YOLO(model_path)

    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    # Load the mask
    mask = cv2.imread(mask_path)
    if mask is None:
        print("Error loading mask. Please check the path.")
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process every nth frame
        if frame_count % frame_skip == 0:
            start_time = time.time()
            frame, vehicle_detected = process_frame(frame, mask, model)
            end_time = time.time()
            print(f"Processing time for frame {frame_count}: {end_time - start_time:.2f} seconds")

            if vehicle_detected:
                print("Vehicle detected!")
                # Pause the video until a key is pressed
                cv2.imshow('Video Frame', frame)
                cv2.waitKey(0)  # Wait for a key press to continue
            else:
                cv2.imshow('Video Frame', frame)
                cv2.waitKey(1)  # Display the frame and wait briefly

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

process_video()