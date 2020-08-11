import numpy as np
from matplotlib import pylab as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import matplotlib.cm as cm

from os import listdir,path
from os.path import isfile,join,isdir

def gaus(x,a,x0,sigma):
  return (a/sigma)*exp(-(x-x0)**2/(2*sigma**2))

def midpoints(hvals):
    hvals_shift=np.append(hvals[1:],0)

    midp=(hvals+hvals_shift)/2.0
    return midp[:-1]

def get_files(directory_path):
    dirpath=directory_path

    files=[f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and ".npy" in f)]
    files=sorted(files)
    n_files=len(files)
    print ("number of files="+str(n_files))
    return files,n_files


# fig1,ax1=plt.subplots(2,1,figsize=(10,8))
# ax1.set_yscale('log')
# ax2.set_yscale('log')
fig1,ax1=plt.subplots(1,1,figsize=(10,6))
fig2,ax2=plt.subplots(1,1,figsize=(11,5))
ax1.set_yscale('log')
# ax2.set_yscale('log')
ax1.grid(True)
ax2.grid(True)

dirpath="../outputpy"
files, n_files=get_files(dirpath)

noise_std=np.array([])
dataset_label=np.array([])
noise_std_unc=np.array([])

colors = iter(cm.gist_ncar(np.linspace(0, 1,6)))


for j,file_iter in enumerate(files):
    print(j,file_iter)

    noisehist=False
    if (("_pedsub_BPM" in file_iter) and ("neg20" in file_iter)): #("20" in file_iter)
        with open(dirpath+'/'+file_iter,'rb') as f:
            input_data=np.load(f)

        # if (("noise" not in file_iter) and ("BPM" not in file_iter) and ("Mask" not in file_iter) and (file_iter[0]=='0')): #("20" in file_iter)
        # if (("noise" in file_iter) and ("Mask" not in file_iter)):
            noisehist=True
            print ("noise")

    if(noisehist):
        colorChoice=next(colors)

        histVals=ax1.hist(input_data.ravel(),bins=25,range=(190,320),histtype='step',label=file_iter.split('_')[0],color=colorChoice,linewidth=2)
        mphist=midpoints(histVals[1])

        # popt,pcov=curve_fit(gaus,mphist,histVals[0],p0=[100000,0,10])
        # ax1.plot(mphist,gaus(mphist,*popt),color=colorChoice,linestyle="--")

        print(histVals[0][11:].max(),histVals[0][11:].argmax())
        peak_max=histVals[0][11:].argmax()+11
        print('max',peak_max)
        try:
            popt2,pcov2=curve_fit(gaus,mphist[peak_max-2:peak_max+13],histVals[0][peak_max-2:peak_max+13],p0=[2600,250,20])
        except:
            popt2=[1,1,1]
        print(popt2)
        ax1.plot(mphist,gaus(mphist,*popt2),color=colorChoice,linestyle="dotted")
        noise_std=np.append(noise_std,popt2[1])
        noise_std_unc=np.append(noise_std_unc,np.sqrt(np.diag(pcov2))[2])

        dataset_label=np.append(dataset_label,file_iter.split('_')[0])
    # else:
    #     histvals=ax2.hist(input_data,bins=120,range=(-40,80),histtype='step',label=file_iter[:-4])


    # maxval= histvals[1][histvals[0].argmax()]
    # input_data=input_data/maxval
    # # plt.clf()
    # _=ax1.hist(input_data,bins=100,range=(-10,40),histtype='step')
ax1.tick_params(axis='x', labelsize=15)
ax1.tick_params(axis='y', labelsize=15)
ax2.tick_params(axis='x', labelsize=15)
ax2.tick_params(axis='y', labelsize=15)
ax1.set_ylim([10,1000])
# ax1.set_xlim([-100,130])
# ax1.set_ylim([0.002,0.5])
ax1.set_xlabel('ADU', fontsize=18)
# ax1.set_xlabel('Sigma')
ax1.set_ylabel('Entries', fontsize=18)
# ax2.scatter(dataset_label,noise_std)
ax2.errorbar(dataset_label,noise_std,marker='.',yerr=noise_std_unc,linestyle="None")

# ax1.set_xlim([0,42])
# ax2.set_xlabel('Datasets', fontsize=18)
# ax1.set_xlabel('Sigma')
ax2.set_ylabel("ADU", fontsize=18)
# ax1.set_ylim([0.002,0.5])
# ax2.set_xlabel('Pedestal subtracted ADC')
# ax1.set_xlabel('Sigma')
# ax2.set_ylabel('Entries')
leg = ax1.legend(fancybox=True, loc='lower left', fontsize=14)
# leg = ax2.legend(fancybox=True, loc='upper right')

fig1.savefig("pedsubfit-signalpeakfit.png")
fig2.savefig("signalPeak.png")

plt.pause(0.01)
input("pause")