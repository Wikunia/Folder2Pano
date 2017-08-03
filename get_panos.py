import os,shutil,sys
import cv2
import piexif
import numpy as np
from shutil import copy
from subprocess import call

MANUAL = 1
EXPOSURE_TIME = 33434
F_NUMBER = 33437
EXPOSURE_PROGRAM = 34850
ISO = 34855
FOCAL = 37386

MIN_MATCH_COUNT = 10

directory = sys.argv[1]

def remove_unreasonable_images(d,pano_files):
    """ Remove images in d/ if they are not part of the panorama

    Keyword arguments:
    d -- directory
    pano_files -- list of image files in d
    """
    
    # crop the pano files first for sift speedup
    for file in pano_files:
        copy(directory+file,d)
        img = cv2.imread(d+file)
        res = cv2.resize(img,None,fx=0.1, fy=0.1, interpolation = cv2.INTER_CUBIC)
        cv2.imwrite(d+"small_"+file, res)
    
    # find features for each image
    sift = cv2.xfeatures2d.SIFT_create()
    kps = []
    dess = []
    for i in range(len(pano_files)):
        filename = d+"small_"+pano_files[i]

        img = cv2.imread(filename)  # queryImage

        # find the keypoints and descriptors with SIFT
        kp, des = sift.detectAndCompute(img, None)
        kps.append(kp)
        dess.append(des)

    # get matches between the images
    good_images = [0 for i in range(len(pano_files))]
    for im1_no in range(len(pano_files)):
        for im2_no in range(im1_no+1,len(pano_files)):
            filename1 = d+"small_"+pano_files[im1_no]
            filename2 = d+"small_"+pano_files[im2_no]

            img1 = cv2.imread(filename1)  # queryImage
            img2 = cv2.imread(filename2)  # trainImage

            # find the keypoints and descriptors with SIFT
            kp1, des1 = kps[im1_no], dess[im1_no]
            kp2, des2 = kps[im2_no], dess[im2_no]

            bf = cv2.BFMatcher()
            if des1 is not None and des2 is not None:
                matches = bf.knnMatch(des1, des2, k=2)
                
                try:
                    smt = 0.3
                    while smt <= 4:
                        good = []
                        for coins, n in matches:
                            if coins.distance < smt * n.distance:
                                if coins.queryIdx < len(kp1) and coins.queryIdx < len(kp2):
                                    good.append(coins)
                        if len(good) >= MIN_MATCH_COUNT:
                            break
                        else:
                            smt += 0.1

                    good_images[im1_no] += len(good)
                    good_images[im2_no] += len(good)
                except ValueError:
                    pass

    # remove the cropped photos and the ones which aren't part of the pano        
    reasonable_files = 0        
    for i in range(len(good_images)):
        if good_images[i] < MIN_MATCH_COUNT:
            os.remove(d+pano_files[i])
        else:
            reasonable_files += 1
        os.remove(d+"small_"+pano_files[i])
    
    return True if reasonable_files > 1 else False
        

def check_pano(pano_files):
    # at least two photos are needed
    if len(pano_files) < 2:
        return False
    
    # copy files to current directory using first and last name
    new_dir = "%s-%s/" % (pano_files[0].split(".")[0],pano_files[-1].split(".")[0])
    print(new_dir)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    else:
        if os.path.exists(new_dir[:-1]+".jpg"):
            print("Exists already")
            return
    
    reasonable = remove_unreasonable_images(new_dir,pano_files)   
    # use hugin to actually create the pano
    if reasonable:
        call(['sh','pano.sh',new_dir[:-1]])
    
# get all jpeg files in the directory and sort them
files = [x for x in os.listdir(directory) if x.lower().endswith(".jpg")]
files.sort()
      
last_tags = None 
pano_files = []

"""
    For each file check if it's manual and have the same settings as the one before
    to add it to the current pano. At the end -> check the pano and compute it
"""
for filename in files:
    exif_dict = piexif.load(directory+filename)
    ifd = "Exif"
    if exif_dict[ifd][EXPOSURE_PROGRAM] != MANUAL:
        check_pano(pano_files)
        pano_files = []
        last_tags = None
        continue
        
    tags = [exif_dict[ifd][tag] for tag in [EXPOSURE_TIME,F_NUMBER,ISO,FOCAL]]
    if last_tags is None or np.array_equal(tags,last_tags):
        pano_files.append(filename)
        last_tags = tags
    else:
        check_pano(pano_files)
        pano_files = []
        last_tags = None
            
            

