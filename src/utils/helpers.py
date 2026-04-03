import cv2

def get_video_properties(cap):
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    return width, height, fps