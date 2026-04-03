import cv2
import numpy as np
from ultralytics import YOLO
from sklearn.cluster import KMeans

model = YOLO("yolov8n.pt")

video_path = "data/videos/match.mp4"
cap = cv2.VideoCapture(video_path)

colors = []

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    boxes = results[0].boxes.xyxy.cpu().numpy()

    for box in boxes:

        x1, y1, x2, y2 = map(int, box)

        player = frame[y1:y2, x1:x2]

        if player.size == 0:
            continue

        player = cv2.resize(player, (20,40))

        avg_color = player.mean(axis=(0,1))

        colors.append(avg_color)

cap.release()

colors = np.array(colors)

kmeans = KMeans(n_clusters=2)
kmeans.fit(colors)

print("Team colors:")
print(kmeans.cluster_centers_)