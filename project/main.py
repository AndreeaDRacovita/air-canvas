import numpy as np
import cv2

width = 640
height = 480
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, width)
cap.set(4, height)
cap.set(10, 150)

mask_colors = {
    "Orange": [0, 130, 130, 34, 255, 255],
    "Blue": [105, 155, 35, 125, 255, 255],
    "Green": [25, 56, 0, 87, 255, 255],
    "Red": [162, 164, 115, 178, 255, 255]
}

bgr_colors = {
    "Orange": (0, 140, 255),
    "Blue": (255, 144, 30),
    "Green": (0, 128, 0),
    "Red": (0, 0, 255)
}

# x, y, color
painting_points = []


def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w//2, y


def find_color(img, mask_colors):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in mask_colors:
        lower = np.array(mask_colors[color][0:3])
        upper = np.array(mask_colors[color][3:6])
        mask = cv2.inRange(img_hsv, lower, upper)
        x, y = get_contours(mask)
        if x != 0 and y != 0:
            painting_points.append([x, y, color])


def draw_on_canvas(painting_points):
    for point in painting_points:
        cv2.circle(imgResult, (point[0], point[1]), 15, bgr_colors[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    find_color(img, mask_colors)
    draw_on_canvas(painting_points)
    cv2.imshow("Virtual Paint", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
