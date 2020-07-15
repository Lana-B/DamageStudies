import numpy as np
from matplotlib import pylab as plt
from os import listdir,path
from os.path import isfile,join,isdir
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp

def get_files(directory_path):
    dirpath=directory_path

    files=[f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and ".npy" in f)]
    files=sorted(files)
    n_files=len(files)
    print ("number of files="+str(n_files))
    return files,n_files

def midpoints(hvals):
    hvals_shift=np.append(hvals[1:],0)

    midp=(hvals+hvals_shift)/2.0
    return midp[:-1]

def gaus(x,a,x0,sigma):
  return (a/sigma)*exp(-(x-x0)**2/(2*sigma**2))


dirpath="../outputpy"
files, n_files=get_files(dirpath)
for j,file_iter in enumerate(files):
    print(j,file_iter)
    
    noisehist=False

    with open(dirpath+'/'+file_iter,'rb') as f:
        if ("rawdata" in file_iter):
            fig0,ax0=plt.subplots(1,1,figsize=(10,6))
            fig1,ax1=plt.subplots(1,1,figsize=(10,6))
            fig2,ax2=plt.subplots(1,1,figsize=(10,6))
            fig3,ax3=plt.subplots(1,1,figsize=(10,6))
            fig4,ax4=plt.subplots(1,1,figsize=(16,6))
            # ax1.set_yscale('log')
            # ax2.set_yscale('log')
            ax0.grid(True)
            ax1.grid(True)
            ax2.grid(True)
            ax3.grid(True)
            ax4.grid(True)
            input_data=np.load(f)
            noisehist=True
            print ("noise")
            print(input_data.shape)

            print(len(input_data))
            # try:
            #     input_data=input_data.reshape(100,int(len(input_data)/100))

            # except:
            #     continue

        else: 
            continue
    # for i in range(0,40):
    singlePix=input_data[:,4,13]

    binwidth=7
    histValues=ax0.hist(singlePix,bins=np.arange(min(singlePix), max(singlePix) + binwidth, binwidth),histtype='step',label=file_iter[:-4])
    mphist=midpoints(histValues[1])
    meanArgMax=histValues[0].argmax()
    meanh=mphist[meanArgMax]
    # print(meanh-70,meanh+70)
    stdh=singlePix.std()
    # print(meanh,stdh)
    popt2,pcov2=curve_fit(gaus,mphist[:histValues[0].argmax()+2],histValues[0][:histValues[0].argmax()+2],p0=[15,meanh,stdh])
    print('1',popt2)
    print(np.sqrt(np.diag(pcov2)))
    arr=np.arange(min(singlePix),mphist[histValues[0].argmax()+2],2)
    print(min(singlePix),mphist[histValues[0].argmax()+2],arr)
    _=ax0.plot(arr,gaus(arr,*popt2),'r-.',label='fit')

    histValues=ax1.hist(singlePix,range=(meanh-70,meanh+70),bins=20,histtype='step',color='red',label=file_iter[:-4])    
    mphist=midpoints(histValues[1])
    meanArgMax=histValues[0].argmax()
    meanh=mphist[meanArgMax]
    # print(meanh-70,meanh+7)
    stdh=singlePix.std()
    # print(meanh,stdh)
    popt2,pcov2=curve_fit(gaus,mphist,histValues[0],p0=[15,meanh,stdh])
    print('2',popt2)
    _=ax1.plot(mphist[:histValues[0].argmax()+5],gaus(mphist[:histValues[0].argmax()+5],*popt2),'yo:',label='fit')
    secondSinglePix=singlePix[singlePix<popt2[1]+4*popt2[2]]

    histValues=ax2.hist(secondSinglePix,range=(meanh-70,meanh+70),bins=20,histtype='step',label=file_iter[:-4])
    mphist=midpoints(histValues[1])
    meanh=mphist[histValues[0].argmax()]
    stdh=secondSinglePix.std()
    # print(meanh,stdh)
    popt2,pcov2=curve_fit(gaus,mphist,histValues[0],p0=[15,meanh,stdh])
    print('3',popt2)
    _=ax2.plot(mphist[:histValues[0].argmax()+5],gaus(mphist[:histValues[0].argmax()+5],*popt2),'yo:',label='fit')

    thirdSinglePix=secondSinglePix[secondSinglePix<popt2[1]+4*popt2[2]]

    histValues=ax3.hist(thirdSinglePix,range=(meanh-70,meanh+70),bins=20,histtype='step',label=file_iter[:-4])
    mphist=midpoints(histValues[1])
    meanh=mphist[histValues[0].argmax()]
    stdh=thirdSinglePix.std()
    # print(meanh,stdh)
    popt2,pcov2=curve_fit(gaus,mphist,histValues[0],p0=[15,meanh,stdh])
    print('4',popt2)
    _=ax3.plot(mphist[:histValues[0].argmax()+5],gaus(mphist[:histValues[0].argmax()+5],*popt2),'yo:',label='fit')

    xvals=np.arange(1,101)
    pedsub=singlePix-popt2[1]
    pedsub2=np.copy(pedsub)
    pedsub2[pedsub2<0]=0
    err=np.sqrt(pedsub2*0.2)+11
    ax4.errorbar(xvals,singlePix,yerr=err,linestyle=":",marker='o')

#     if(noisehist):
#         histvals=ax1.hist(input_data,bins=100,range=(-100,650),histtype='step',label=file_iter[:-4])


#     else:
#         histvals=ax2.hist(input_data,bins=100,range=(-40,80),histtype='step',label=file_iter[:-4],density=True)


#     # maxval= histvals[1][histvals[0].argmax()]
#     # input_data=input_data/maxval
#     # _=ax1.hist(input_data,bins=100,range=(-10,40),histtype='step')
# # ax1.set_ylim([10,40000])
# ax1.set_xlim([-100,600])
# ax2.set_xlim([-20,60])
    ax0.tick_params(axis='x', labelsize=15)
    ax0.tick_params(axis='y', labelsize=15)
    ax4.tick_params(axis='x', labelsize=15)
    ax4.tick_params(axis='y', labelsize=15)
    ax0.set_xlabel('ADU',fontsize=18)
# # ax1.set_xlabel('Sigma')
    ax0.set_ylabel('Entries',fontsize=18)
# ax2.set_ylim([0.00001,0.5])
# # ax1.set_ylim([0.002,0.5])
    ax4.set_xlabel('Frame number',fontsize=18)
# # ax1.set_xlabel('Sigma')
    ax4.set_ylabel('ADU',fontsize=18)
# leg = ax1.legend(fancybox=True, loc='upper right', fontsize=14)
# leg = ax2.legend(fancybox=True, loc='upper right', fontsize=14)
    fig0.savefig("rawdatahist.png")
# fig2.savefig("pedsubnoisediv.png")


    fig4.savefig("singlePix.png")
    plt.pause(0.01)
    input("pause")
    plt.cla()

    # fig1.cla()
    # fig2.cla()
