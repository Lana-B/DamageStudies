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


fig1,ax1=plt.subplots(2,1,figsize=(5,8))
ax1[0].set_yscale('log')
ax1[1].set_yscale('log')

dirpath="../output_HDR_noMask"
files, n_files=get_files(dirpath)
for j,file_iter in enumerate(files):
    print(j,file_iter)

    noisehist=False
    if("BPM" in file_iter):
        continue

    with open(dirpath+'/'+file_iter,'rb') as f:
        input_data=np.load(f)
        if "noise" in file_iter:
            noisehist=True
            print ("noise")

    print(file_iter[:9]+"BPMOnly.npy")
    with open(dirpath+'/'+file_iter[:9]+"BPMOnly.npy",'rb') as f:
        BPM_data=np.load(f)

    if(noisehist):
        histvals=ax1[0].hist(input_data[BPM_data>0].ravel(),bins=100,histtype='step',label=file_iter[:-4],density=True)


    else:
        histvals=ax1[1].hist(input_data[BPM_data>0].ravel(),bins=100,range=(-10,50),histtype='step',label=file_iter[:-4])


    # maxval= histvals[1][histvals[0].argmax()]
    # input_data=input_data/maxval
    # # plt.clf()
    # _=ax1.hist(input_data,bins=100,range=(-10,40),histtype='step')
ax1[0].set_xlim([-150,400])
# ax1.set_ylim([0.002,0.5])
ax1[0].set_xlabel('Pedestal subtracted ADC')
# ax1.set_xlabel('Sigma')
ax1[0].set_ylabel('Entries')
# ax1[1].set_ylim([1,40000])
# ax1.set_ylim([0.002,0.5])
ax1[1].set_xlabel('Signal/Noise')
# ax1.set_xlabel('Sigma')
ax1[1].set_ylabel('Entries')
# leg = ax1[0].legend(fancybox=True, loc='upper right')
# leg = ax1[1].legend(fancybox=True, loc='upper right')

plt.pause(0.01)
input("pause")