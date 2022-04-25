import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML
from matplotlib.animation import ArtistAnimation

from DVSModule.dvs import *

__author__ = "Saulquin Aurélie"
__copyright__ = ""
__credits__ = ["Saulquin Aurélie", "Boulet Pierre", "Elbez Hammouda"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Saulquin Aurélie"
__email__ = "clement.saulquin.etu@univ-lille.fr"
__status__ = "Available"

if __name__ == '__main__':

    # create DVSEvents class
    dvs_event = DVSEvents("../../events20051221T014416 freeway.mat.dat", DVS128(), AERV1(), verbose=0)

    
    # the length of time to generate data for, in seconds and in microseconds
    t_length = 10
    t_length_us = int(1e6 * t_length)

    # init frame variables
    dt_frame_us = 20e3
    t_frames = dt_frame_us * np.arange(int(round(t_length_us / dt_frame_us)))

    fig = plt.figure()
    imgs = []

    # get event from DVSEvent class
    events = dvs_event.getAllData()

    # construct video
    for t_frame in t_frames:

        t0_us = t_frame
        t1_us = t_frame + dt_frame_us

        t = events[:]["t"]  # get time values of all events

        m = (t >= t0_us) & (t < t1_us)
        events_m = events[m]

        # show "off" (0) events as -1 and "on" (1) events as +1
        events_sign = 2.0 * events_m["p"] - 1

        # construct and add frame
        frame_img = np.zeros((dvs_event.height, dvs_event.width))

        frame_img[events_m["y"], events_m["x"]] = events_sign

        img = plt.imshow(frame_img, vmin=-1, vmax=1, animated=True)
        imgs.append([img])

    del dvs_event

    ani = ArtistAnimation(fig, imgs, interval=50, blit=True)
    HTML(ani.to_html5_video())
    plt.show()