import trackpy as tp
import matplotlib.pyplot as plt
import numpy as np
import tifffile
import os
from PIL import Image
import io


def batch(frames, particle_diameter, particle_minmass, save_video=False, output_path=None):
    """
    Given a set of parameters, batch all of the frames with the identified particles 
    into a single structure. Optionally, save annotated frames as a TIFF stack.

    Args:
        frames (pims.Frames): Frames object containing the images.
        particle_diameter (int): Diameter of the particles in pixels.
        particle_minmass (int): Minimum mass of the particles.
        save_video (bool): Whether to save the annotated frames as a TIFF stack.
        output_path (str): Directory where the annotated frames TIFF will be saved if save_video is True.

    Returns:
        pandas.DataFrame: DataFrame containing the detected particles.
    """
    # Perform batch particle detection (this returns a DataFrame of detections)
    batched_frames = tp.batch(frames, diameter=particle_diameter, invert=True, minmass=particle_minmass)

    if save_video:
        if output_path is None:
            raise ValueError("output_path must be provided if save_video is True.")
        
        annotated_frames = []
        
        # Loop over each frame to annotate it
        for i, frame in enumerate(frames):
            # Filter detections for the current frame.
            current_detections = batched_frames[batched_frames['frame'] == i]
            
            # Create a new figure for the annotation
            fig, ax = plt.subplots(figsize=(10, 8), frameon=False)
            ax.imshow(frame, cmap="gray")
            ax.axis("off")
            
            # Annotate the frame using trackpy.
            # Here we let tp.annotate draw on the provided axis.
            tp.annotate(current_detections, frame, ax=ax, plot_style={"markersize": 4})
            
            # Instead of displaying the figure, save it to an in-memory buffer as PNG.
            buf = io.BytesIO()
            fig.savefig(buf, format="jpg", bbox_inches="tight", pad_inches=0, transparent=True, dpi=500)
            buf.seek(0)
            
            # Load the image from the buffer using PIL and convert it to a NumPy array.
            annotated_img = np.array(Image.open(buf))
            annotated_frames.append(annotated_img)
            
            plt.close(fig)  # Close the figure to free memory.
        
        # Build the output file path and save the annotated frames as a TIFF stack.
        output_file = os.path.join(output_path, "detected_features.tiff")
        tifffile.imwrite(output_file, np.array(annotated_frames))
    
    return batched_frames


def track(
    batched_frames, frames, particle_diameter, particle_minmass, filter_frame_number, save_video=False, output_path=None):
    """
    
    """

    # Linking particles between frames, and filtering out particles that are not present in enough frames.
    trajectories = tp.link(
        batched_frames, search_range=2, memory=0 # For D = 35mm, I had memory=(particle_diameter // 3)
    )  # Particles may not travel more than 15 pixels between frames, and may be missing for 5 frames at most.
    pre_filtered_trajectories = tp.filter_stubs(
        trajectories, filter_frame_number
    )  # Keep trajectories that only last filter_frame_number of frames

    # Plotting the size vs. mass of the particles.
    plt.figure(1)
    tp.mass_size(pre_filtered_trajectories.groupby("particle").mean())
    # Plots size vs. mass. Encourages a recursive iteration of parameter estimation.

    # Filtering the data based on mass, size, and eccentricity.
    filtered_trajectories = pre_filtered_trajectories[
        (
            (pre_filtered_trajectories["mass"] > particle_minmass)
            & (pre_filtered_trajectories["size"] < particle_diameter)
            & (pre_filtered_trajectories["ecc"] < 0.2)
        )
    ]

    plt.figure(2)
    plt.figure(figsize=(10, 8))
    tp.annotate(
        filtered_trajectories[filtered_trajectories["frame"] == 0], frames[0]
    )  # Plot the particle tracking of a single frame to assess accuracy.

    # Compare the number of particles in the unfiltered pre-filtered data, and filtered data.
    print("No-filter:", trajectories["particle"].nunique())
    print("Pre-filter:", pre_filtered_trajectories["particle"].nunique())
    print("Filter:", filtered_trajectories["particle"].nunique())

    if save_video:
        if output_path is None:
            raise ValueError("output_path must be provided if save_video is True.")
        
        annotated_frames = []
        dpi = 500  # Adjust DPI to control the resolution of the saved frames.
        
        # Loop over each frame.
        for i, frame in enumerate(frames):
            # Create a figure sized to match the original frame.
            # (Here we assume frame is a 2D array (grayscale) or 3D with channels.)
            height, width = frame.shape[:2]
            figsize = (width / dpi, height / dpi)
            fig, ax = plt.subplots(figsize=figsize, dpi=dpi, frameon=False)
            ax.axis("off")
            
            # First, show the original frame.
            ax.imshow(frame, cmap="gray", zorder=0)
            
            # For cumulative trajectories up to the current frame,
            # filter trajectories with frame <= i.
            traj_subset = filtered_trajectories[filtered_trajectories["frame"] <= i]
            
            # Plot the cumulative trajectories using trackpy's fast plotting function.
            # We omit the 'frame' argument so that it doesn't overwrite our image.
            tp.plot_traj(traj_subset, ax=ax, plot_style={"markersize": 6, "color": "darkblue"}, frame=None)
            
            # Overlay the current detections (to circle the particles).
            current_detections = filtered_trajectories[filtered_trajectories["frame"] == i]
            if not current_detections.empty:
                tp.annotate(current_detections, frame, ax=ax, plot_style={"markersize": 2})
            
            # Save the figure to an in-memory buffer.
            buf = io.BytesIO()
            fig.savefig(buf, format="jpg", bbox_inches="tight", pad_inches=0, transparent=True, dpi=dpi)
            buf.seek(0)
            annotated_img = np.array(Image.open(buf))
            annotated_frames.append(annotated_img)
            plt.close(fig)
        
        # Save the list of annotated frames as a TIFF stack.
        output_file = os.path.join(output_path, "detected_trajectories.tiff")
        tifffile.imwrite(output_file, np.array(annotated_frames))
    
    return filtered_trajectories
