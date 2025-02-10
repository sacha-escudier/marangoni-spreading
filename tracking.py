import trackpy as tp
import matplotlib.pyplot as plt
import numpy as np

def batch(frames, particle_diameter, particle_minmass):
    """
    Given a set of parameters, batch all of the frames with the identified particles into a single structure.

    Args:
        frames (pims.frames): Frames object containing the images.
        particle_diameter (int): Diameter of the particles in pixels.
        particle_minmass (int): Minimum mass of the particles.

    Returns:
        tp.batch: Batch object containing the frames with the identified particles.
    """
    return tp.batch(frames, diameter=particle_diameter, invert=True, minmass=particle_minmass)

def track(batched_frames, frames, particle_diameter, particle_minmass, filter_frame_number):
    """
    
    """

    # Linking particles between frames, and filtering out particles that are not present in enough frames.
    trajectories = tp.link(batched_frames, search_range=15, memory=5) # Particles may not travel more than 15 pixels between frames, and may be missing for 5 frames at most.
    pre_filtered_trajectories = tp.filter_stubs(trajectories, filter_frame_number) # Keep trajectories that only last filter_frame_number of frames

    # Plotting the size vs. mass of the particles.
    plt.figure(1)
    tp.mass_size(pre_filtered_trajectories.groupby('particle').mean()); # Plots size vs. mass. Encourages a recursive iteration of parameter estimation.

    # Filtering the data based on mass, size, and eccentricity.
    filtered_trajectories = pre_filtered_trajectories[((pre_filtered_trajectories['mass'] > particle_minmass) & (pre_filtered_trajectories['size'] < particle_diameter) &
            (pre_filtered_trajectories['ecc'] < 0.2))]
    
    plt.figure(2)
    plt.figure(figsize=(10, 8))
    tp.annotate(filtered_trajectories[filtered_trajectories['frame'] == 0], frames[0]) # Plot the particle tracking of a single frame to assess accuracy.

    # Compare the number of particles in the unfiltered pre-filtered data, and filtered data.
    print('No-filter:', trajectories['particle'].nunique())
    print('Pre-filter:', pre_filtered_trajectories['particle'].nunique())
    print('Filter:', filtered_trajectories['particle'].nunique())

    return filtered_trajectories
    # #################

    # plt.figure(3)
    # tp.plot_traj(t2)

    # d = tp.compute_drift(t2)
    # d.plot()
    # plt.show()

    # tm = tp.subtract_drift(t2.copy(), d)
    # ax = tp.plot_traj(tm)
    # plt.show()

    # particles_per_frame = tm['frame'].value_counts().sort_index()

    # frame_number_array = np.linspace(1, len(particles_per_frame), len(particles_per_frame))
    # y_arr = tm['frame'].value_counts().sort_index()

    # plt.scatter(frame_number_array, y_arr)
    # print(np.std(y_arr) / np.mean(y_arr))
    # print(max(y_arr) - min(y_arr))

    # return y_arr, tm