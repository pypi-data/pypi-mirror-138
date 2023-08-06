import cv2 as cv
import numpy as np
import os

def import_data_cube(path):
    """
    ########## HSTI_import ##########
    This function takes an HSTI numpy array and exports it as individual .ppm
    images to a folder given by folder_name.
    """

    impath = path + 'images/capture/'

    try:
        number_of_image_files = sum([ '.ppm' in s for s in os.listdir(impath)])

        steps = np.linspace(0,number_of_image_files*10-10,number_of_image_files)

        imgs = np.zeros((768,1024,len(steps)))

        for idx,i in enumerate(steps):
            imgs[:,:,idx] = cv.imread(impath+'step'+str(int(i)) + '.ppm',cv.IMREAD_ANYDEPTH)
        imgs = np.rot90(imgs,1)
    except:
        print('Path should be directory containing the \'images\' directory.')

    return imgs
