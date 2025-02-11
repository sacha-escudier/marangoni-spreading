# marangoni-spreading


## Parameters for D=35mm:
last_frame=150
diameter=15
mass=6000
x_c = 875 # determine empirically with ImageJ
y_c = 545 # determine empirically with ImageJ
trajectories = tp.link(
        batched_frames, search_range=particle_diameter, memory=(particle_diameter // 3))

## Parameters for D=60mm:
last_frame = 200
diameter = 11
mass = 2200
x_c = 960 # determine empirically with ImageJ
y_c = 524 # determine empirically with ImageJ
trajectories = tp.link(
        batched_frames, search_range=2, memory=0 )