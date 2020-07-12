import numpy as np

def colorPicker(prob):
    rgb = np.array([])
    # White
    if prob < 0:
        rgb = np.array([255, 255, 255])
    # Green
    elif 0 <= prob < 10:
        rgb = np.array([0, 255, 0])
    # Light Green
    elif 10 <= prob < 20:
        rgb = np.array([150, 255, 0])
    # Yellow
    elif 20 <= prob < 30:
        rgb = np.array([255, 255, 0])
    # Orange Yellow
    elif 30 <= prob < 40:
        rgb = np.array([255, 190, 0])
    # Orange
    elif 40 <= prob < 50:
        rgb = np.array([255, 255/2, 0])
    # red
    elif 50 <= prob <= 100:
        rgb = np.array([255, 0, 0])
    return rgb
