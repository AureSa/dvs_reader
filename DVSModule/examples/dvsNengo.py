#!/usr/bin/env python

""" Example of use DVSProcess to send data to nengo neural network"""

import nengo
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

class macam(CameraFam)

if __name__ == '__main__':
    
    pool = (1, 1)

    gain = 101

    t_length = 10
    t_length_us = int(1e6 * t_length)

    with nengo.Network() as net:

        # create dvs process and give process to nengo sim
        
        # Read Bloc method
        # dvs_process = DVSProcess("../../events20051221T014416 freeway.mat.dat", DVS128(), AERV1(), verbose=1, channel_last=True, pool=pool, read_type=ReadType.BLOC)  
        
        # Read Flow method
        dvs_process = DVSProcess("../../events20051221T014416 freeway.mat.dat", DVS128(), AERV1(), 
        verbose=1, channel_last=True, pool=pool, read_type=ReadType.FLOW)

        u = nengo.Node(dvs_process)

        ensembles = [
            nengo.Ensemble(
                dvs_process.height * dvs_process.width,
                1,
                neuron_type=nengo.SpikingRectifiedLinear(),
                gain = nengo.dists.Choice([gain]),
                bias = nengo.dists.Choice([0])
            )
            for _ in range(dvs_process.polarity)
        ]

        for k, e in enumerate(ensembles):
            u_channel = u[k :: dvs_process.polarity]
            nengo.Connection(u_channel, e.neurons, transform=1.0 / np.prod(pool))

        probes = [nengo.Probe(e.neurons) for e in ensembles]

    with nengo.Simulator(net) as sim:
        sim.run(t_length)

    ## uncomment this section to see input spike 
    sim_t = sim.trange()
    shape = (len(sim_t), dvs_process.height, dvs_process.width)
    output_spikes_neg = sim.data[probes[0]].reshape(shape) * sim.dt
    output_spikes_pos = sim.data[probes[1]].reshape(shape) * sim.dt

    # get output video (see ex_dvsevents.py for more explanation) 
    dt_frame = 0.01
    t_frames = dt_frame * np.arange(int(round(t_length / dt_frame)))

    fig = plt.figure()
    imgs = []
    for t_frame in t_frames:
        t0 = t_frame
        t1 = t_frame + dt_frame
        m = (sim_t >= t0) & (sim_t < t1)

        frame_img = np.zeros((dvs_process.height, dvs_process.width))
        frame_img -= output_spikes_neg[m].sum(axis=0)
        frame_img += output_spikes_pos[m].sum(axis=0)
        frame_img = frame_img / np.abs(frame_img).max()

        img = plt.imshow(frame_img, vmin=-1, vmax=1, animated=True)
        imgs.append([img])

    ani = ArtistAnimation(fig, imgs, interval=50, blit=True)
    HTML(ani.to_html5_video())
    plt.show()