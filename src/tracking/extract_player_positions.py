import cv2
import pandas as pd
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

video_path = "data/videos/match.mp4"
cap = cv2.VideoCapture(video_path)

data = []
frame_id = 0

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    results = model.track(frame, persist=True)

    boxes = results[0].boxes

    if boxes.id is None:
        continue

    ids = boxes.id.cpu().numpy()
    xyxy = boxes.xyxy.cpu().numpy()

    for player_id, box in zip(ids, xyxy):

        x1, y1, x2, y2 = box
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        data.append({
            "frame": frame_id,
            "player_id": int(player_id),
            "x": cx,
            "y": cy
        })

cap.release()

df = pd.DataFrame(data)
df.to_csv("data/player_positions.csv", index=False)

print("Saved player positions dataset")