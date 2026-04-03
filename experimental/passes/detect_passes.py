import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO

model = YOLO("yolov8m.pt")

video_path = "data/videos/match.mp4"
cap = cv2.VideoCapture(video_path)

current_holder = None
hold_frames = 0
MIN_HOLD = 3   # lower for safety

passes = []
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
    classes = boxes.cls.cpu().numpy()

    player_centers = []
    player_ids = []
    ball_center = None

    for pid, box, cls in zip(ids, xyxy, classes):

        x1, y1, x2, y2 = box
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # players (NO FILTER NOW)
        if cls == 0:
            player_centers.append((cx, cy))
            player_ids.append(int(pid))

        # ball
        if cls == 32:
            ball_center = np.array([cx, cy])

    # fallback if ball missing
    if ball_center is None:
        h, w = frame.shape[:2]
        ball_center = np.array([w // 2, h // 2])

    if not player_centers:
        continue

    # find closest player
    distances = [
        np.linalg.norm(ball_center - np.array(p))
        for p in player_centers
    ]

    closest_index = np.argmin(distances)
    current_player = player_ids[closest_index]

    # -------------------------
    # possession logic
    # -------------------------
    if current_holder == current_player:
        hold_frames += 1

    else:
        if current_holder is not None and hold_frames >= MIN_HOLD:
            passes.append({
                "frame": frame_id,
                "passer": current_holder,
                "receiver": current_player
            })

        current_holder = current_player
        hold_frames = 1

cap.release()

df = pd.DataFrame(passes)
df.to_csv("data/passesf.csv", index=False)

print(f"✅ Pass dataset saved with {len(df)} passes")