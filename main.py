import argparse
import time
import cv2 as cv
import mss
import numpy as np
import pyautogui

from models import ImageEvaluator, ImageTransformer

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--show", action="store_true", help="show real-time images")
args = parser.parse_args()
show = args.show

transformer = ImageTransformer(width=1920, height=1080)
evaluator = ImageEvaluator(show=show)
monitor = transformer.monitor

with mss.mss() as sct:
    while True:
        target_area = np.array(sct.grab(monitor))
        transformed = transformer.polar_transform(target_area)
        diff = evaluator.compute_difference(transformed)

        if show:
            cv.imshow("Target Area", target_area)
            cv.imshow("Transformed", transformed)
            cv.imshow("Detected", evaluator.drawed_img)

        if diff <= 10:
            time.sleep(0.03)
            pyautogui.mouseUp(button='left')

        if cv.waitKey(25) & 0xFF == ord("q"):
            cv.destroyAllWindows()
            break
