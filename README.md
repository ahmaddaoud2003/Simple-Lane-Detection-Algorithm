# Simple Lane Detection Algorithm

This is a basic implementation of a **Lane Detection System** using **OpenCV** for self-driving or autonomous vehicles. The algorithm identifies lanes on the road, which is essential for vehicle navigation and autonomy.

This project uses video input to detect lanes in real time. It's based on image processing techniques, and OpenCV is the core library used for detecting edges, lines, and applying transformations to identify the lane.

### Why Lane Detection?
Lane detection is crucial for autonomous vehicles to maintain a safe and accurate path while driving. This simple algorithm demonstrates a fundamental approach to solving this problem.
## Features
- Detects lanes in real-time from a video feed.
- Utilizes **Canny edge detection**, **Hough transform**, and **Region of Interest (ROI)** to detect lanes accurately.
- Written in **Python** using **OpenCV**.

## How It Works

The algorithm processes the video in the following steps:
1. **Preprocessing**: Convert the image to grayscale and apply Gaussian blur.
2. **Edge Detection**: Use Canny edge detection to detect edges.
3. **Region of Interest**: Focus on the area where lanes are likely to appear.
4. **Line Detection**: Use Hough Line Transform to detect straight lines that represent lanes.
5. **Lane Overlay**: Finally, overlay the detected lanes on the original image.

Here’s a visualization of the algorithm in action:

![Lane Detection Example](https://github.com/ahmaddaoud2003/Simple-Lane-Detection-Algorithm/assets/145913339/2ea1eeb7-6ac4-4f13-b90a-a3dab2fc0e41)


The video used in the code was obtained from Kagg;e:
[Lane Detection Video Dataset](https://www.kaggle.com/datasets/dpamgautam/video-file-for-lane-detection-project)
