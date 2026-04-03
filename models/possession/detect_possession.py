import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

video_path = "data/videos/match.mp4"
cap = cv2.VideoCapture(video_path)

# read first frame
ret, frame = cap.read()

if not ret:
    print("Video could not be read")
    exit()

# now frame exists, so we can create the writer
height, width = frame.shape[:2]

out = cv2.VideoWriter(
    "data/videos/possession.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    25,
    (width, height)
)

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    player_centers = []
    ball_center = None

    boxes = results[0].boxes

    for box in boxes:

        cls = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # player
        if cls == 0:
            player_centers.append((cx, cy))
            cv2.circle(frame,(cx,cy),5,(0,255,0),-1)

        # ball
        if cls == 32:
            ball_center = (cx, cy)
            cv2.circle(frame,(cx,cy),6,(0,0,255),-1)

    if ball_center is not None and player_centers:

        distances = []

        for player in player_centers:
            dist = np.linalg.norm(
                np.array(player) - np.array(ball_center)
            )
            distances.append(dist)

        closest_player = player_centers[np.argmin(distances)]

        cv2.line(frame, ball_center, closest_player, (255,0,0),2)

        cv2.putText(
            frame,
            "Possession",
            closest_player,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,0,0),
            2
        )

    out.write(frame)
out.release()
cap.release()
cv2.destroyAllWindows()