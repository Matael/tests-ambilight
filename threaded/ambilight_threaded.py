#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# ambilight_threaded.py
#
# Copyright © 2013 Mathieu Gaborit (matael) <mathieu@matael.org>
#
#
# Distributed under WTFPL terms
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

"""
Try to reimplement an ambiligth programme using threaded workers
"""

import cv2
import numpy as np
import threading
from utilities import CycleQueue, Singleton
from Queue import Queue

# instanciate CAM object
cam = cv2.VideoCapture(0)

_,f = cam.read()
l = image_width = f.shape[1]
image_height = f.shape[0]
nb_points = 5
dh = int(f.shape[0]/nb_points)
bandwidth = int(l*0.05) # 5% of total width

masks = []

def enqueue_zones(queue, masks):
    """ Generate zones coordinates and masks and enqueue them

    tuple format :
        (y0, x0, y1, x1, index of masks)

    we have to store masks in another lists as Queue() doesn't
    recognize numpy arrays as valid datatypes

    """

    for h in xrange(nb_points):
        # generate masks
        mask_right = np.zeros((image_height,image_width,1), np.uint8)
        mask_left = np.zeros((image_height,image_width,1), np.uint8)
        for i in xrange(dh):
            for j in xrange(bandwidth):
                mask_left[dh*h+i][j] = 1
                mask_right[dh*h+i][l-j-1] = 1

        prev_len = len(masks)
        masks.append(mask_left)
        masks.append(mask_right)

        # enqueue
        ## left zone
        queue.put(( 0, dh*h, bandwidth, dh*(h+1), prev_len))
        ## right zone
        queue.put(( image_width-bandwidth, dh*h, image_width, dh*(h+1), prev_len+1))

@Singleton
class IMG:
    """ Handle current image """

    def __init__(self):
        self.final_image = None
        self.image = None

    def new_image(self, f):
        self.image = f
        self.final_image = f


class ColorAverageWorker(threading.Thread):

    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue

    def run(self):
        while True:
            zone = self.queue.get()
            color = cv2.mean(IMG.Instance().image, mask=masks[zone[4]])
            self.out_queue.put({'zone': zone,
                                'color': color})
            self.queue.task_done()


class WorkerDraw(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):

        while True:
            point = self.queue.get()
            zone = point['zone']
            cv2.rectangle(IMG.Instance().final_image, (zone[0], zone[1]), (zone[2], zone[3]), color=point['color'], thickness=-1)
            self.queue.task_done()

# init a CycleQueue for zones
zones = CycleQueue()
out_queue = Queue()

def main():
    # enqueue zones
    enqueue_zones(zones, masks)
    zones.lockstate()
    num_workers = 5

    _,f = cam.read()
    IMG.Instance().new_image(f)

    for i in xrange(num_workers):
        t = ColorAverageWorker(zones, out_queue)
        t.start()

    t = WorkerDraw(out_queue)
    t.start()

    while True:
        _,f = cam.read()
        IMG.Instance().new_image(f)

        zones.reinit()

        zones.join()
        out_queue.join()

        cv2.imshow('w1', IMG.Instance().final_image)

        if cv2.waitKey(2) == 27:
            break

if __name__=='__main__':
    main()
