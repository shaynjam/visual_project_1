import cv2
import numpy as np

chars = np.asarray(list(" .:-=+*#%@"))
cap = cv2.VideoCapture(0)
ret, prev = cap.read()
prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
while True:
    return_val, frame = cap.read()
    if return_val == False:
        print("camera cant be accessed")
        break
    flipped_frame = cv2.flip(frame, 1)

    frame_2 = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
    frame_3 = cv2.resize(frame_2, (200, 80), interpolation=cv2.INTER_NEAREST)

    prev_2 = cv2.resize(prev_gray, (200, 80), interpolation=cv2.INTER_NEAREST)

    diff_image = cv2.absdiff(frame_3, prev_2)

    retu, diff_image_resized = cv2.threshold(
        diff_image, 25, maxval=255, type=cv2.THRESH_TOZERO
    )

    diff_image_resized = cv2.convertScaleAbs(diff_image_resized, alpha=1.5)
    colour_small = cv2.resize(flipped_frame, (200, 80), interpolation=cv2.INTER_NEAREST)
    colour_small = cv2.convertScaleAbs(colour_small, alpha=1.5)
    rows, cols = frame_3.shape

    final_pixel = ((diff_image_resized / 255) * (len(chars) - 1)).astype(int)
    final_frame = chars[final_pixel]
    output_str = "\n".join("".join(row) for row in final_frame)
    print("\033[H" + output_str, end="", flush=True)

    prev_gray = frame_2

    cv2.imshow("sigma", frame_3)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
