from ultralytics import YOLO
import cv2
import cvzone
import math

def process(image_path: str, mask_path: str) -> int:
    # Paths to the model weights
    model_path = "yolo weights/yolov8x.pt"

    # Load YOLOv8 model
    model = YOLO(model_path)

    # Load the image and mask
    img = cv2.imread(image_path)
    mask = cv2.imread(mask_path)

    if img is None or mask is None:
        raise ValueError("Error loading image or mask. Please check the paths.")

    # Apply the mask to the image
    imgRegion = cv2.bitwise_and(img, mask)

    # Perform object detection
    results = model(imgRegion, stream=True)

    # Initialize counters
    car_count = 0
    motorbike_count = 0
    truck_count = 0
    bus_count = 0

    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck"]

    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
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

            # Count relevant objects
            if currentClass == 'car':
                car_count += 1
            elif currentClass == 'motorbike':
                motorbike_count += 1
            elif currentClass == 'truck':
                truck_count += 1
            elif currentClass == 'bus':
                bus_count += 1

            # Draw bounding boxes and labels
            if currentClass in ['car', 'motorbike', 'truck', 'bus']:
                cvzone.cornerRect(img, (x1, y1, w, h), l=10)
                cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(40, y1)), scale=0.6, thickness=1,
                                   offset=3)

        # Display counts on the image with a black text box
        count_text = f"Cars: {car_count}, Motorbikes: {motorbike_count}, Trucks: {truck_count}, Buses: {bus_count}"
        re = car_count + (motorbike_count * 0.5) + (truck_count * 2) + (bus_count * 2)

        # Calculate text box dimensions based on font size and text length
        font_scale = 1  # Adjust font size as needed
        text_size, _ = cv2.getTextSize(count_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
        text_width, text_height = text_size

        # Define black background rectangle dimensions with some padding
        padding = 10  # Adjust padding as needed
        text_box_x1 = 10  # Adjust text box position if needed
        text_box_y1 = 50 - text_height - padding // 2
        text_box_width = text_width + 2 * padding
        text_box_height = text_height + 2 * padding

        # Draw black background rectangle
        cv2.rectangle(img, (text_box_x1, text_box_y1), (text_box_x1 + text_box_width, text_box_y1 + text_box_height),
                      (0, 0, 0), cv2.FILLED)  # Fill with black color

        # Display count text with white color on top of the black box
        cv2.putText(img, count_text, (text_box_x1 + padding, text_box_y1 + text_height + padding // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2, cv2.LINE_AA)

    # Save the result to a file
    output_image_path="C:/Users/sharv/Downloads/jsx/jsx/sih/src/images/processed_image.png"
    cv2.imwrite(output_image_path, img)
    print(f"Image saved to {output_image_path}")

    # Print counts
    print(count_text)
    print(re)

    # Show the result (optional, remove if running in an environment where display is not supported)
    #cv2.imshow("Image with Detection", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return int(re)

# Example usage
#result = process("images/3.png", "images/3imask.png")
#print(f"Computed result: {result}")