import numpy as np
from matplotlib import pylab as plt
import scipy as sp
from os import listdir,path
from os.path import isfile,join,isdir
from scipy.optimize import curve_fit
from scipy.stats import norm
import math
from scipy import asarray as ar,exp
import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--datasetdir', help='foo help')
args = parser.parse_args()
dataset_directory=args.datasetdir
#eg. --datasetdir ../data/Fe-55_0RadDam_40deg/
print("input files ",args.datasetdir)

def get_files(directory_path):
    dirpath=directory_path

    files=[f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and 'tiff' in f)]
    files=sorted(files)
    n_files_fn=len(files)
    print ("number of files="+str(n_files_fn))
    return files,n_files_fn

files, n_files=get_files(dataset_directory)
for j,file_iter in enumerate(files):
    if(j%10==0):
        print(j,file_iter)

    im=plt.imread(str(datasetdir+"/"+file_iter)) #np.fromfile(file_iter,dtype='uint16',sep="")
    plt.imshow(im)
    plt.pause(0.01)