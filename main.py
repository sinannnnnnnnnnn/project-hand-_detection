import cv2

from hand_detector import HandDetector
from roi_draw import *

cap = cv2.VideoCapture(0)

detector = HandDetector()

cv2.namedWindow("Hand Detection ROI")
cv2.setMouseCallback("Hand Detection ROI", mouse_callback)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame, hands = detector.detect_hands(frame)

    roi = get_roi()

    hands_inside = 0

    if roi is not None:

        x1, y1, x2, y2 = roi

        # Ensure correct coordinates
        left = min(x1, x2)
        right = max(x1, x2)
        top = min(y1, y2)
        bottom = max(y1, y2)

        for hand in hands:

            hx1, hy1, hx2, hy2 = hand

            cx = (hx1 + hx2) // 2
            cy = (hy1 + hy2) // 2

            # Draw center point
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            if left <= cx <= right and top <= cy <= bottom:
                hands_inside += 1

        # Change rectangle color
        if hands_inside > 0:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 3)

    # Display status
    if hands_inside > 0:
        cv2.putText(
            frame,
            "HAND DETECTED",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )
    else:
        cv2.putText(
            frame,
            "NO HAND",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    cv2.putText(
        frame,
        f"Hands Inside Box : {hands_inside}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Press R to redraw box | Q to Quit",
        (20, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow("Hand Detection ROI", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):
        reset_roi()

    elif key == ord('q'):
        break

cap.release()    
cv2.destroyAllWindows()