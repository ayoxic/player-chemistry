import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

video_path = "data/videos/match.mp4"
cap = cv2.VideoCapture(video_path)

width = int(cap.get(3))
height = int(cap.get(4))
fps = cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter(
    "data/videos/ball_detection.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps if fps > 0 else 25,
    (width, height)
)

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    boxes = results[0].boxes

    for box in boxes:

        cls = int(box.cls[0])

        # class 32 = sports ball
        if cls == 32:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)

            cv2.putText(
                frame,
                "Ball",
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,0,255),
                2
            )

    out.write(frame)

cap.release()
out.release()

print("Ball detection video saved")