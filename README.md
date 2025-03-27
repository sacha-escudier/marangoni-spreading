# marangoni-spreading

## Relevevant MetaData:
Black Paramagnetic Polyethylene Microspheres
rho = 1.2 g/cm^3
d = 425 - 500 um

## Parameters for D=35mm:
Depth of fluid = 9.5 mm
last_frame = 150
diameter = 15
mass = 6000
x_c = 875 # determine empirically with ImageJ
y_c = 545 # determine empirically with ImageJ
trajectories = tp.link(
        batched_frames, search_range=particle_diameter, memory=(particle_diameter // 3))
23 pixels / mm

## Parameters for D=60mm:
Depth of fluid = 9.5 mm
last_frame = 200
diameter = 11
mass = 2200
x_c = 960 # determine empirically with ImageJ
y_c = 524 # determine empirically with ImageJ
trajectories = tp.link(
        batched_frames, search_range=2, memory=0 )
13 pixels / mm

## Parameters for D=100mm:
Depth of fluid = 9.5 mm
last_frame = 200
diameter = 11
mass = 2200
x_c = 980 # determine empirically with ImageJ
y_c = 503 # determine empirically with ImageJ
trajectories = tp.link(
        batched_frames, search_range=2, memory=0 )


## Parameters for deep-dish, H (depth) = 4cm/1cm
Diameter = 9.5 +- 0.05 cm
Total height = 4.9 +- 0.05 cm
Depth of fluid = 4 cm/ 1cm (see notebook)