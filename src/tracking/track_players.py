import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

video_path = "data/videos/match.mp4"
cap = cv2.VideoCapture(video_path)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

out = cv2.VideoWriter(
    "data/videos/tracked.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps if fps > 0 else 25,
    (width, height)
)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO tracking
    results = model.track(frame, persist=True)

    annotated_frame = results[0].plot()

    out.write(annotated_frame)

cap.release()
out.release()

print("Tracking video saved to data/videos/tracked.mp4")