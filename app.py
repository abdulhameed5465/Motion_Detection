import os
import sys
import time
from datetime import datetime

import cv2
import numpy as np

def main(source=0):
    cap = cv2.VideoCapture(source)
    os.makedirs("recordings", exist_ok=True)

    # history = how many frames to learn the background from
    # detectShadows=True marks shadows as grey (127) instead of white (255)
    backsub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40,
                                                 detectShadows=True)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    writer = None
    last_motion = 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 20

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.resize(frame, (800, 600))

        fg = backsub.apply(frame)

        # drop the grey shadow pixels, keep only the confident foreground
        _, fg = cv2.threshold(fg, 200, 255, cv2.THRESH_BINARY)
        fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel, iterations=2)   # remove specks
        fg = cv2.dilate(fg, kernel, iterations=2)                          # fill gaps

        contours, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_now = False
        for c in contours:
            area = cv2.contourArea(c)
            if area < MIN_AREA:
                continue
            motion_now = True
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f"{int(area)} px", (x, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "MOTION" if motion_now else "Clear"
        cv2.putText(frame, f"{stamp}   {status}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 0, 255) if motion_now else (0, 200, 0), 2)

        # --- start / stop recording -------------------------------------
        if motion_now:
            if writer is None:
                fname = datetime.now().strftime("recordings/%Y%m%d_%H%M%S.avi")
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                writer = cv2.VideoWriter(fname, fourcc, fps, (800, 600))
                with open("motion_log.txt", "a") as f:
                    f.write(f"{stamp}  motion detected -> {fname}\n")
                print(f"Recording {fname}")
            last_motion = time.time()

        if writer is not None:
            writer.write(frame)
            if not motion_now and time.time() - last_motion > RECORD_SECONDS:
                writer.release()
                writer = None
                print("Stopped recording")
        # ----------------------------------------------------------------

        cv2.imshow("Security camera", frame)
        cv2.imshow("Foreground mask", fg)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break
        if key == ord('r'):
            backsub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=40,
                                                         detectShadows=True)
            print("Background model reset")

    if writer is not None:
        writer.release()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else 0)
