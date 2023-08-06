# required dependency
import cv2
from PoseDetectionModule import MbPoseDetection

cam = cv2.VideoCapture(0)

# import and apply the model you want to try.
# ....

while cam.isOpened():
    success, images = cam.read()

    cv2.imshow("OP", images)
    cv2.waitKey(1)
