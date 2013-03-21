#!/usr/bin/env python2
#-*- coding:utf8 -*-

import cv2
import numpy as np

# instanciate CAM object
cam = cv2.VideoCapture(1)

while 1:
    # get one image for test processing
    _,f = cam.read()

    # get total width
    l = f.shape[1]

    nb_points = 5
    dh = int(f.shape[0]/nb_points)

    bandwidth = int(l*0.05) # 5% of total width

    for h in xrange(nb_points):

        # create mask
        mask_left = np.zeros((f.shape[0],f.shape[1],1), np.uint8)
        mask_right = np.zeros((f.shape[0],f.shape[1],1), np.uint8)

        for i in xrange(dh):
            for j in xrange(bandwidth):
                mask_left[dh*h+i][j] = 1
                mask_right[dh*h+i][l-j-1] = 1

        val_left = cv2.mean(f, mask=mask_left)
        val_right = cv2.mean(f, mask=mask_right)

        cv2.rectangle(f, (0,dh*h), (bandwidth,dh*(h+1)), color=val_left, thickness=-1)
        cv2.rectangle(f, (l-bandwidth,dh*h), (l,dh*(h+1)), color=val_right, thickness=-1)

    cv2.imshow('w1', f)

    if cv2.waitKey(2) == 27:
        break

print('i = '+str(i)) # DEBUG
cv2.destroyAllWindows()
