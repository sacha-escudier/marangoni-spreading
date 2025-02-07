import cv2
import os

def extract_frames(video_path, output_folder, grayscale = False):
    """
    Extracts frames from a video file and saves them as images.

    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Path to the folder where frames will be saved.

    Returns:
        None
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the video file
    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return

    frame_count = 0
    while True:
        # Read the next frame
        ret, frame = video_capture.read()
        
        if not ret:
            break  # Exit the loop when no more frames are available

        # Construct the output file path
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:03d}.jpg")

        # Save the current frame as an image
        if grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(frame_filename, frame)

        print(f"Saved frame {frame_count} as {frame_filename}")

        frame_count += 1

    # Release the video capture object
    video_capture.release()

    print(f"Extraction complete. {frame_count} frames saved in {output_folder}")