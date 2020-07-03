import numpy as np
from matplotlib import pylab as plt
from os import listdir,path
from os.path import isfile,join,isdir
from scipy import ndimage


def get_files(directory_path):
    dirpath=directory_path

    files=[f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and ".npy" in f)]
    files=sorted(files)
    n_files=len(files)
    print ("number of files="+str(n_files))
    return files,n_files




dirpath="../outputpy_noMask"
files, n_files=get_files(dirpath)
fig3,ax3=plt.subplots(1,1,figsize=(10,6))
fig4,ax4=plt.subplots(1,1,figsize=(10,6))

for j,file_iter in enumerate(files):
    print(j,file_iter)

    noisehist=False
    print(file_iter)
    if "noise" in file_iter:
        fig1,ax1=plt.subplots(1,1,figsize=(10,6))
        fig2,ax2=plt.subplots(1,1,figsize=(10,6))
        ax1.set_yscale('log')
        ax2.set_yscale('log')
        with open(dirpath+'/'+file_iter,'rb') as f:
            pedSub_data=np.load(f)
            print(dirpath+'/'+file_iter)

        file_sig=str(file_iter[:-10])+".npy"
        with open(dirpath+'/'+file_sig,'rb') as f:
            sig2noise_data=np.load(f)
            print (dirpath+'/'+file_sig)

        print(pedSub_data[0,1:3,1:5])
        print(sig2noise_data[0,1:3,1:5])


        histvals=ax1.hist(pedSub_data.ravel(),bins=130,range=(-80,700),histtype='step', label="All data")
        histvals=ax2.hist(sig2noise_data.ravel(),bins=120,range=(-40,80),histtype='step', label="All data")
        ax1.set_xlim(-50,700)
        ax2.set_xlim(-40,80)
        kern=np.ones([3,3])
        kern=kern*2
        kern[1,1]=1

        seed=(sig2noise_data[:,:,:]>2.0)*1.0
        print('seed',seed.shape)
        convolved=np.zeros(seed.shape)
        print('conv',convolved.shape)

        for k in range(0,seed.shape[0]):
            convolved_sub = ndimage.convolve(seed[k,:,:], kern)
            # print('conv',convolved_sub.shape)
            convolved[k,:,:]=convolved_sub
        newarr=(convolved==1)*1.0
        newarr=newarr.reshape(seed.shape[0],seed.shape[1],seed.shape[2])

        file_BPM=str(file_iter[:-16])+"BPMOnly.npy"
        with open(dirpath+'/'+file_BPM,'rb') as f:
            badpixmask3d=np.load(f)
            print (dirpath+'/'+file_BPM)

        # pedSub_data_BPM=pedSub_data[badpixmask3d>0]
        # sig2noise_data_BPM=sig2noise_data[badpixmask3d>0]

        ax1.hist(pedSub_data[:,:,:][(newarr==1) & (badpixmask3d>0) & (sig2noise_data>4)].ravel(),bins=130,range=(-80,600), label="Single hits")
        ax2.hist(sig2noise_data[:,:,:][(newarr==1)  & (badpixmask3d>0) & (sig2noise_data>4)].ravel(),bins=120,range=(-50,100), label="Single hits")


        ax1.set_xlabel('Pedestal subtracted ADC',fontsize=18)
        # ax1.set_xlabel('Sigma')
        ax1.set_ylabel('Entries',fontsize=18)
        # ax1[1].set_ylim([1,40000])
        # ax1.set_ylim([0.002,0.5])
        ax2.set_xlabel('Signal / Noise',fontsize=18)
        # ax1.set_xlabel('Sigma')
        ax2.set_ylabel('Entries',fontsize=18)
        ax1.tick_params(axis='x', labelsize=15)
        ax1.tick_params(axis='y', labelsize=15)
        ax2.tick_params(axis='x', labelsize=15)
        ax2.tick_params(axis='y', labelsize=15)

        leg = ax1.legend(fancybox=True, loc='upper right', fontsize=14)
        leg = ax2.legend(fancybox=True, loc='upper right', fontsize=14)
        fig1.savefig("singleHits_pedsub"+file_iter[:-17]+".png")
        fig2.savefig("singleHits_SNR"+file_iter[:-17]+".png")

        # plt.pause(0.01)
        # input("pause")
        # plt.clf()

        if("neg" in file_iter):
            input_data=pedSub_data[:,:,:][(newarr==1) & (badpixmask3d>0) & (sig2noise_data>4)].ravel()
            # if ('0kGy' in file_iter):
                # input_data=input_data*100/82.0
            ax3.hist(input_data,bins=40,range=(0,400), label=file_iter[:-17],histtype='step')
            ax3.set_xlabel('Pedestal subtracted ADC',fontsize=18)
            ax3.set_ylabel('Entries',fontsize=18)
            ax3.tick_params(axis='x', labelsize=15)
            ax3.tick_params(axis='y', labelsize=15)
            ax3.set_xlim(0,400)


            leg = ax3.legend(fancybox=True, loc='upper left', fontsize=14)


        if(file_iter[0]=='0'):
            input_data=pedSub_data[:,:,:][(newarr==1) & (badpixmask3d>0) & (sig2noise_data>4)].ravel()
            # if ('neg' in file_iter):
                # input_data=input_data*100/82.0
            ax4.hist(input_data,bins=40,range=(0,400), label=file_iter[:-17],histtype='step')
            ax4.set_xlabel('Pedestal subtracted ADC',fontsize=18)
            ax4.set_ylabel('Entries',fontsize=18)
            ax4.tick_params(axis='x', labelsize=15)
            ax4.tick_params(axis='y', labelsize=15)
            ax4.set_xlim(0,400)


            leg = ax4.legend(fancybox=True, loc='upper left', fontsize=14)


    else:
        continue
fig3.savefig("singleHits_neg20.png")
fig4.savefig("singleHits_0kGy.png")

    # maxval= histvals[1][histvals[0].argmax()]
    # pedSub_data=pedSub_data/maxval
    # # plt.clf()
    # _=ax1.hist(pedSub_data,bins=100,range=(-10,40),histtype='step')
# # ax1.set_ylim([10,40000])
# # ax1.set_ylim([0.002,0.5])
# ax1.set_xlabel('Pedestal subtracted ADC')
# # ax1.set_xlabel('Sigma')
# ax1.set_ylabel('Entries')
# # ax2.set_ylim([1,40000])
# # ax1.set_ylim([0.002,0.5])
# ax2.set_xlabel('Pedestal subtracted ADC')
# # ax1.set_xlabel('Sigma')
# ax2.set_ylabel('Entries')
# leg = ax1.legend(fancybox=True, loc='upper right')
# leg = ax2.legend(fancybox=True, loc='upper right')
