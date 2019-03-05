#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Dec 20 17:39 2016

@author: Denis Tome'
"""

import __init__
import sys

from lifting import PoseEstimator
from lifting.utils import draw_limbs
from lifting.utils import plot_pose

import cv2
import matplotlib.pyplot as plt
from os.path import dirname, realpath

DIR_PATH = dirname(realpath(__file__))
PROJECT_PATH = realpath(DIR_PATH + '/..')
IMAGE_FILE_PATH = PROJECT_PATH + '/data/images/test_image.png'
SAVED_SESSIONS_DIR = PROJECT_PATH + '/data/saved_sessions'
SESSION_PATH = SAVED_SESSIONS_DIR + '/init_session/init'
PROB_MODEL_PATH = SAVED_SESSIONS_DIR + '/prob_model/prob_model_params.mat'


def main(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # conversion to rgb

    # create pose estimator
    image_size = image.shape

    pose_estimator = PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)

    # load model
    pose_estimator.initialise()

    # estimation
    pose_2d, visibility = pose_estimator.estimate(image)
    
    # close model
    pose_estimator.close()

    # Show 2D and 3D poses
    # print pose_2d
    # display_results(image, pose_2d, visibility)
    if len(pose_2d) == 0:
        return []
    return pose_2d[0]   


def display_results(in_image, data_2d, joint_visibility ):
    """Plot 2D and 3D poses for each of the people in the image."""
    plt.figure()
    draw_limbs(in_image, data_2d, joint_visibility)
    plt.imshow(in_image)
    cv2.waitKey(3)
    plt.axis('off')

    # Show 3D poses
    # for single_3D in data_3d:
    #     # or plot_pose(Prob3dPose.centre_all(single_3D))
    #     plot_pose(single_3D)

    plt.show()


def swap_list(mylist):
    if len(mylist) == 0:
        return mylist
    result = []
    for i in range(len(mylist)):
        result.append([mylist[i][1],mylist[i][0]])
    # print(type(mylist), type(result))
    # convert list to openpose standard
    list_convert = [0, 1, 2, 5, 8, 11, 3, 4, 6, 7, 9, 10, 12, 13]
    converted = []
    for i in range(len(mylist)):
        converted.append(result[list_convert[i]])
    return converted



def run_predict_pose(obj, w, h):
    ske = []
    print(len(obj))
    for i in range(len(obj)):
        # print(i+50)
        tmp = main(obj[i])
        # print tmp
        # print "swaped"
        tmp = swap_list(tmp)
        # print tmp
        # print "done"
        ske.append(tmp)
    print "predicted"
    return ske


if __name__ == '__main__':
    sys.exit(main())
