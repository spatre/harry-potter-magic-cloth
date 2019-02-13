import cv2
import numpy as np
import time


# Capture the background frame to create the invisibility effect
def bg_capture(capture):

    # Allowing the webcam to stabilize
    time.sleep(3)
    bg_frame = 0
    i = 0

    # Looping so as to capture a stable frame from the webcam
    while i < 25:
        ret, bg_frame = capture.read()
        i += 1

    bg_frame = cv2.flip(bg_frame, 1)

    return bg_frame


# Generate masks based on color input
def color_detect(frame, color):

    mask = None

    if color == 'red':
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        mask_red_1 = cv2.inRange(frame, lower_red, upper_red)

        lower_red = np.array([170, 120, 70])
        upper_red = np.array([180, 255, 255])
        mask_red_2 = cv2.inRange(frame, lower_red, upper_red)

        mask = mask_red_1 + mask_red_2

    elif color == 'blue':
        lower_blue = np.array([110, 50, 70])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(frame, lower_blue, upper_blue)

    elif color == 'green':
        lower_green = np.array([50, 50, 70])
        upper_green = np.array([70, 255, 255])
        mask = cv2.inRange(frame, lower_green, upper_green)

    return mask


# Generates a Real-Time magic cloak effect if you are wearing an appropriate color
def magic_cloak(capture, background, color):

    while True:

        ret, img_capture = capture.read()

        # Inverting the frame
        img_capture = cv2.flip(img_capture, 1)

        # converting from BGR to HSV color space
        hsv = cv2.cvtColor(img_capture, cv2.COLOR_BGR2HSV)

        # Getting the color mask
        mask = color_detect(hsv, color)

        # morph_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        morph_mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

        # Isolating the cloak from the frame by creating an inverted mask
        cloak_mask = cv2.bitwise_not(morph_mask)

        # Segmenting the cloak out of the frame by bitwise and using the inverted mask
        output_1 = cv2.bitwise_and(img_capture, img_capture, mask=cloak_mask)

        # Generating background pixels over the cloak region
        output_2 = cv2.bitwise_and(background, background, mask=morph_mask)

        # Generating the final output ( Weights can be adjusted for transparency as required)
        final_frame = cv2.addWeighted(output_1, 1, output_2, 1, 0)

        # Displaying the final frame
        cv2.imshow("Sorcery", final_frame)

        # Press 'Return/Enter' Key to exit
        if cv2.waitKey(1) == 13:
            break


# Main function starts here
def main():

    cap = cv2.VideoCapture(0)
    color = 'red'  # change colors to 'red', 'blue', or 'green' to detect accordingly
    back_ground = bg_capture(cap)
    magic_cloak(cap,back_ground, color)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
