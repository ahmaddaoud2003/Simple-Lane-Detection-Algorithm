import cv2
import numpy as np


# Creating coordinates from slope and intercept
def makeCoordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0] #Bottom of the image
    y2 = int(y1*(3/5)) # Slightly lower than the middle
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

# Function to average and extrapolate the detected lines
def averageSlopeIntercept(image, lines):
    left_fit = [] # coordinates of the averaged lines on the left
    right_fit = [] # coordinates of the averaged lines on the right
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = makeCoordinates(image, left_fit_average)
    right_line = makeCoordinates(image, right_fit_average)
    return np.array([left_line, right_line])

# canny edge detection
def canny(image):
    #coverts the image from coloured to gray scale
    gray  = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) 
    # using a gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # shows only the gradient image
    canny = cv2.Canny(blur, 50, 150)
    return canny

# function to display detected lines on a black image
def displayLines(image, lines):
    line_image = np.zeros_like(image) # create an image filled with zeros
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


# Function to create a region of interest (ROI) mask
def regionOfInterest(image):
    height = image.shape[0]
    # creates a polygon with 3 points   
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    # creates a mask with the same dimensions as the image
    mask = np.zeros_like(image)
    # filling the mask with the triangle
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


# Initialize video capture from file
cap = cv2.VideoCapture('video.mp4')

# Get video frame width, height, and frame rate
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_rate = int(cap.get(5))

# Define the codec and create VideoWriter object
out = cv2.VideoWriter('LaneDetection.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), frame_rate,
                      (frame_width, frame_height))

# Process each frame in the video
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    canny_image = canny(frame)  # Apply Canny edge detection to the frame
    cropped_image = regionOfInterest(canny_image)  # Apply region of interest mask
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40,
                            maxLineGap=5)  # Detect lines using Hough transform
    averaged_lines = averageSlopeIntercept(frame, lines)  # Average and extrapolate lines
    line_image = displayLines(frame, averaged_lines)  # Display detected lines on the frame
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)  # Overlay lines on the frame

    # Write the frame into the file 'output_video.avi'
    out.write(combo_image)

    cv2.imshow('Lane Detection', combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()