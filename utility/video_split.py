import cv2

# Open the video file
video = cv2.VideoCapture('IMG_6625.mov')

# Initialize frame counter
count = 0

# Loop through each frame in the video
while True:
    if count % 15 != 0:
        video.read()
        count += 1
        continue
    # Read the next frame
    ret, frame = video.read()

    # If there are no more frames, break out of the loop
    if not ret:
        break

    # Save the frame as a JPEG image
    cv2.imwrite(f'./mov1/frame{count//15}.jpg', frame)

    # Increment the frame counter
    count += 1

# Release the video file
video.release()
