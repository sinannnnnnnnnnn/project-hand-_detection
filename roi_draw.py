import cv2

drawing = False
roi = None
start_point = (0, 0)


def mouse_callback(event, x, y, flags, param):
    global drawing, roi, start_point

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        roi = (start_point[0], start_point[1], x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi = (start_point[0], start_point[1], x, y)


def draw_roi(frame):

    global roi

    if roi is not None:

        x1, y1, x2, y2 = roi

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 0, 0),
            2
        )

    return frame


def get_roi():
    return roi


def reset_roi():
    global roi
    roi = None