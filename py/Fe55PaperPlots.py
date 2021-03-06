import numpy as np
from matplotlib import pylab as plt
from os import listdir,path
from os.path import isfile,join,isdir
import matplotlib.cm as cm

def get_files(directory_path):
    dirpath=directory_path

    files=[f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and ".npy" in f)]
    files=sorted(files)
    n_files=len(files)
    print ("number of files="+str(n_files))
    return files,n_files


fig1,ax1=plt.subplots(1,1,figsize=(10,6))
fig2,ax2=plt.subplots(1,1,figsize=(10,6))
ax1.set_yscale('log')
ax2.set_yscale('log')
ax1.grid(True)
ax2.grid(True)
 
colors = iter(cm.gist_ncar(np.linspace(0, 1, 8)))

dirpath="../outputpy"
files, n_files=get_files(dirpath)
for j,file_iter in enumerate(files):
    print(j,file_iter)

    if (("_pedsub_BPM" in file_iter) and ('40deg' not in file_iter) and ('20deg' not in file_iter)):
        with open(dirpath+'/'+file_iter,'rb') as f:
            input_data=np.load(f)
            colorchoice=next(colors)
            if('neg20' in file_iter):
                lstyle='-.'
            else:
                lstyle='-'
            histvals=ax1.hist(input_data,bins=100,range=(-100,650),histtype='step',linestyle=lstyle,label=file_iter[:-4],color=colorchoice)

    # elif ("_pedsub_stddiv_BPM" in file_iter and (file_iter[0]!='0')):
    #     with open(dirpath+'/'+file_iter,'rb') as f:
    #         if('neg20' in file_iter):
    #             print(input_data.shape)

    #             input_data=np.load(f)
    #             histvals=ax2.hist(input_data,bins=200,range=(-5,65),histtype='step',label=file_iter[:-4],color=colorchoice)
    #             print(input_data.shape)  

    else:
        continue
        # histvals=ax2.hist(input_data,bins=100,range=(-40,80),histtype='step',label=file_iter[:-4],density=True)


    # maxval= histvals[1][histvals[0].argmax()]
    # input_data=input_data/maxval
    # # plt.clf()
    # _=ax1.hist(input_data,bins=100,range=(-10,40),histtype='step')
ax1.set_ylim([10,70000])
ax1.set_xlim([-100,600])
# ax2.set_xlim([-20,60])
# ax2.set_ylim([0.0001,0.5])

ax1.tick_params(axis='x', labelsize=15)
ax1.tick_params(axis='y', labelsize=15)
ax2.tick_params(axis='x', labelsize=15)
ax2.tick_params(axis='y', labelsize=15)
ax1.set_xlabel('Pedestal subtracted ADC',fontsize=18)
# ax1.set_xlabel('Sigma')
ax1.set_ylabel('Normalised Entries',fontsize=18)
# ax1.set_ylim([0.002,0.5])
ax2.set_xlabel('Signal / Noise',fontsize=18)
# ax1.set_xlabel('Sigma')
ax2.set_ylabel('Normalised Entries',fontsize=18)
leg = ax1.legend(fancybox=True, loc='upper right', fontsize=14)
leg = ax2.legend(fancybox=True, loc='upper right', fontsize=14)
fig1.savefig("pedsub.png")
fig2.savefig("pedsubnoisediv.png")

plt.pause(0.01)
input("pause")