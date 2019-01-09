#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 bily     Huazhong University of Science and Technology
#
# Distributed under terms of the MIT license.
# Pre-set ROI
r"""Generate tracking results for videos using Siamese Model"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path as osp
import sys
import numpy as np
import cv2
from os import listdir
from PIL import Image


# CURRENT_DIR = osp.dirname(__file__)
# sys.path.append(CURRENT_DIR)
import datetime
from SiameseTracker import SiameseTracker


def preprocess(img):
    res = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return res


def postprocess(img):
    res = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return res



def main():
    # debug = 0 , no log will produce
    # debug = 1 , will produce log file
    tracker = SiameseTracker(debug=0)
    tracker_left = SiameseTracker(debug=0)
    time_per_frame = 0
    txtname="record3D.txt"
    index = 0

    if len(sys.argv) <= 1:
        print('[ERROR]: File path error!')
        return

    if sys.argv[1] == "cam1":
        cap = cv2.VideoCapture(1)
        cap.set(3,1920)
        cap.set(4,1080)        
    elif sys.argv[1] == "cam2":
        cap = cv2.VideoCapture(2)
        cap.set(3,1920)
        cap.set(4,1080)
    else:
        cap = cv2.VideoCapture(sys.argv[1])
    if sys.argv[2] == "cam1":
        cap_left = cv2.VideoCapture(1)
        cap_left.set(3,1920)
        cap_left.set(4,1080)
    elif sys.argv[2] == "cam2":
        cap_left = cv2.VideoCapture(2)
        cap_left.set(3,1920)
        cap_left.set(4,1080)
       
    else:
        cap_left = cv2.VideoCapture(sys.argv[2])
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        ret_left,frame_left = cap_left.read()
        cv2.imwrite('tt.jpg',frame)
        frame = preprocess(frame)
        frame_left = preprocess(frame_left)
        cv2.imshow('frame', postprocess(frame))
        cv2.imshow('frame_left', postprocess(frame_left))
        if cv2.waitKey(20000) or 0xFF == ord('o'):
            break

    # select ROI and initialize the model
    #frame=cv2.imread('test.jpg')
    frame=cv2.imread('pattern1.jpg')
    #frame=cv2.imread('tt.jpg')
    frame = preprocess(frame)
    #r = cv2.selectROI(postprocess(frame))
    #cv2.destroyWindow("ROI selector")
    frame_left=cv2.imread('pattern2.jpg')
    #frame_left=cv2.imread('tt.jpg')
    frame_left = preprocess(frame_left)
    #r_left = cv2.selectROI(postprocess(frame_left))
    #cv2.destroyWindow("ROI selector")
    r=(1161, 110, 77, 73)
    #r=(120, 292, 219, 315)
    r_left=(671, 269, 83, 95)
    print('ROI:', r)
    print('ROI_left:', r_left)    
    tracker.set_first_frame(frame, r)
    tracker_left.set_first_frame(frame_left, r_left)

    while True:
    	images=[]
        ret, frame = cap.read()
        ret_left, frame_left = cap_left.read()
        frame = preprocess(frame)
        frame_left = preprocess(frame_left)
        start_time = datetime.datetime.now()
        reported_bbox = tracker.track(frame)
        reported_bbox_left = tracker_left.track(frame_left)
        end_time = datetime.datetime.now()
        ss=str(reported_bbox[0])+","+str(reported_bbox[1])+","+str(reported_bbox[0] + reported_bbox[2])+","+str(reported_bbox[1] + reported_bbox[3])
        if index >10000:
        	index =0
       	index+=1
        context = str(-((reported_bbox[0] + reported_bbox[2])/2-(r[0]+r[2])/2))+" "+str(-((reported_bbox[1] + reported_bbox[3])/2-(r[1]+r[3])/2))+" "+str(-((reported_bbox_left[0] + reported_bbox_left[2])/2-(r_left[0]+r_left[2])/2))+" "+str(-((reported_bbox_left[1] + reported_bbox_left[3])/2-(r_left[1]+r_left[3])/2))+" "+str(index)
        f1 =open(txtname,"w+")
        f1.write(context)
        f1.close()
        #print(context)
        # Display the resulting frame
        # print(reported_bbox)
        cv2.rectangle(frame, (int(reported_bbox[0]), int(reported_bbox[1])),
                      (
                          int(reported_bbox[0]) + int(reported_bbox[2]),
                          int(reported_bbox[1]) + int(reported_bbox[3])),
                      (0, 0, 255), 2)
        cv2.rectangle(frame_left, (int(reported_bbox_left[0]), int(reported_bbox_left[1])),
                      (
                          int(reported_bbox_left[0]) + int(reported_bbox_left[2]),
                          int(reported_bbox_left[1]) + int(reported_bbox_left[3])),
                      (0, 0, 255), 2)

        duration = end_time - start_time
        time_per_frame = 0.9 * time_per_frame + 0.1 * duration.microseconds
        cv2.putText(frame, 'FPS ' + str(round(1e6 / time_per_frame, 1)),
                    (30, 50), 0, 1, (0, 0, 255), 3)
	frame=cv2.resize(frame,(640,320),interpolation=cv2.INTER_CUBIC)
        cv2.imshow('frame', postprocess(frame))
        
        cv2.putText(frame_left, 'FPS ' + str(round(1e6 / time_per_frame, 1)),
                    (30, 50), 0, 1, (0, 0, 255), 3)
	

	frame_left=cv2.resize(frame_left,(640,320),interpolation=cv2.INTER_CUBIC)
        cv2.imshow('frame_left', postprocess(frame_left))       

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
   
   


main()
