import numpy as np
from matplotlib import pylab as plt
from os import listdir,path
from os.path import isfile,join,isdir

def get_files(directory_path):
    dirpath=directory_path

    files=[f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and ".npy" in f)]
    files=sorted(files)
    n_files=len(files)
    print ("number of files="+str(n_files))
    return files,n_files


fig1,ax1=plt.subplots(1,1,figsize=(10,10))
ax1.set_yscale('log')

dirpath="../outputpy"
files, n_files=get_files(dirpath)

for j,file_iter in enumerate(files):
    print(j,file_iter)

    with open(dirpath+'/'+file_iter,'rb') as f:
        input_data=np.load(f)
    histvals=ax1.hist(input_data,bins=100,range=(-10,40),histtype='step',density=True,label=file_iter[:-4])
    ax1.set_ylim([0.002,0.5])
    # maxval= histvals[1][histvals[0].argmax()]
    # input_data=input_data/maxval
    # # plt.clf()
    # _=ax1.hist(input_data,bins=100,range=(-10,40),histtype='step')
leg = plt.legend(fancybox=True, loc='center')

plt.pause(0.01)
input("pause")