import matplotlib.pyplot as plt
import trackpy as tp
import pims


def plot_parameter(
    directory, particle_diameter, particle_minmass, frame_number=-1
):
    """
    Plots the reference image, annotated image, mass histogram, and subpixel bias for a given frame.

    Args:
        directory (str): Path to the folder containing the frames.
        particle_diameter (int): Approximate diameter of the particles in pixels.
        particle_minmass (int): Minimum 'brightness' of the particles.
        frame_number (int): Index of the frame to analyze.

    Returns:
        pims.Frames: The frames object containing the images
    """

    # Relevant path, CHANGE WITH THE VIDEO YOU WANT TO ANALYZE

    frames = pims.open(directory + "*.jpg")

    # Reference image and annoated image, USE THIS TO DETERMINE WHAT COMBINATION OF DIAMETER AND MINMASS WORKS

    plt.figure(1)
    plt.figure(figsize=(10, 8))
    plt.imshow(frames[frame_number], cmap="gray")
    plt.tight_layout()
    plt.show()

    plt.figure(2)
    plt.figure(figsize=(10, 8))
    f = tp.locate(
        frames[frame_number],
        diameter=particle_diameter,
        invert=True,
        minmass=particle_minmass,
    )  # Tweak this! Always keep invert=True (since particles are very dark)
    tp.annotate(f, frames[frame_number], plot_style={"markersize": 2})
    plt.show()

    # plt.figure(3) # Commented out here, not strictly necessary
    # _, ax = plt.subplots()
    # ax.hist(f["mass"], bins=20)
    # ax.set(xlabel="mass", ylabel="count")

    plt.figure(4)
    tp.subpx_bias(f)

    return frames