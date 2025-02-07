import matplotlib.pyplot as plt
import trackpy as tp
import pims


def parameter_estimation(
    directory, particle_diameter, particle_minmass, frame_number=-1
):

    # Relevant path, CHANGE WITH THE VIDEO YOU WANT TO ANALYZE

    frames = pims.open(directory + "*.jpg")

    # Reference image and annoated image, USE THIS TO DETERMINE WHAT COMBINATION OF DIAMETER AND MINMASS WORKS

    plt.figure(1)
    plt.figure(figsize=(10, 8))
    plt.imshow(frames[frame_number], cmap="gray")
    plt.tight_layout()
    plt.show()

    plt.figure(2)
    f = tp.locate(
        frames[frame_number],
        diameter=particle_diameter,
        invert=True,
        minmass=particle_minmass,
    )  # Tweak this! Always keep invert=True (since particles are very dark)
    plt.figure(figsize=(10, 8))
    tp.annotate(f, frames[frame_number], plot_style={"markersize": 2})

    plt.figure(3)
    fig, ax = plt.subplots()
    ax.hist(f["mass"], bins=20)
    ax.set(xlabel="mass", ylabel="count")

    plt.figure(4)
    tp.subpx_bias(f)
