import trackpy as tp
import matplotlib.pyplot as plt

def batch(frames, particle_diameter, particle_minmass):
    f = tp.batch(frames[:], diameter=particle_diameter, invert=True, minmass=particle_minmass)
    return f

def track(f, particle_diameter, particle_minmass, filter_frame_number):
    """

    """

    # Linking particles between frames, and filtering out particles that are not present in enough frames.
    t = tp.link(f, 15, memory=5) # Particles may not travel more than 15 pixels between frames, and may be missing for 5 frames at most.
    t1 = tp.filter_stubs(t, filter_frame_number) # Keep trajectories that only last filter_frame_number of frames

    # Compare the number of particles in the unfiltered and filtered data.
    print('Before:', t['particle'].nunique())
    print('After:', t1['particle'].nunique())

    # Plotting the size vs. mass of the particles.
    plt.figure(1)
    tp.mass_size(t1.groupby('particle').mean()); # convenience function -- just plots size vs. mass

    # Filtering the data based on mass, size, and eccentricity.
    t2 = t1[((t1['mass'] > particle_minmass) & (t1['size'] < 15) &
            (t1['ecc'] < 0.2))]
    plt.figure(2)
    plt.figure(figsize=(10, 8))
    tp.annotate(t2[t2['frame'] == 0], frames[0])