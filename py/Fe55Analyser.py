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

def gaus(x,a,x0,sigma):
  return (a/sigma)*exp(-(x-x0)**2/(2*sigma**2))

def midpoints(hvals):
    hvals_shift=np.append(hvals[1:],0)
#     print(hvals)
#     print(hvals[1:])
#     print(np.append(hvals[1:],0))
    midp=(hvals+hvals_shift)/2.0
    return midp[:-1]

def get_files(directory_path):
    dirpath=directory_path

    files=[f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and 'tiff' in f)]
    files=sorted(files)
    n_files=len(files)
    print ("number of files="+str(n_files))
    return files,n_files

def chosePix(startx_fn,endx_fn,starty_fn,endy_fn,dirpath_fn,files_fn,n_files_fn):
    
    chosenPix=np.array([])
    chosenPixels=np.array([])
    imarray=np.zeros([2800,2400],dtype='float')
    imarraySq=np.zeros([2800,2400],dtype='float')
    for j,file_iter in enumerate(files_fn):
        if(j%10==0):
            print(j,file_iter)


        im=plt.imread(str(dirpath_fn+"/"+file_iter)) #np.fromfile(file_iter,dtype='uint16',sep="")
        im=im.astype('float')
        imarray=imarray+(im/n_files_fn)
        imarraySq=imarraySq+(np.square(im)/n_files_fn)
        chosenPix=np.append(chosenPix,im[starty_fn,startx_fn])
        chosenPixels=np.append(chosenPixels,im[starty_fn:endy_fn,startx_fn:endx_fn])

    std=(imarraySq-np.square(imarray))
    std[std<0]=0
    std=np.sqrt(std)

    return chosenPix, chosenPixels, std

def return_param_BPM(even_odd,hist_val,num):
    if even_odd=="odd":
        eo=1
    else:
        eo=0
    print(even_odd,hist_val)
    histValues=ax[eo,num].hist(df[(df['y_vals']%2==eo)&(df['heights']<1000)][hist_val],bins=45)
    mphist=midpoints(histValues[1])
    meanh=df[(df['y_vals']%2==eo)&(df['heights']<1000)&(df['means']>0)][hist_val].mean()
    stdh=df[(df['y_vals']%2==eo)&(df['heights']<1000)&(df['means']>0)][hist_val].std()
    popt,pcov=curve_fit(gaus,mphist,histValues[0],p0=[35000,meanh,stdh])
    ax[eo,num].plot(histValues[1][:-1],gaus(histValues[1][:-1],*popt),'ro:',label='fit')
    print(popt,meanh,stdh)
#     plt.show()
#     plt.clf()
    return popt[1],popt[2]


def bad_pix_qual(startx_fn,endx_fn,starty_fn,endy_fn,chosenPixels3d_fn):
    means_array_fn=np.zeros([endy_fn-starty_fn,endx_fn-startx_fn],dtype='float')
    stds_array_fn=np.zeros([endy_fn-starty_fn,endx_fn-startx_fn],dtype='float')
    heights_array_fn=np.zeros([endy_fn-starty_fn,endx_fn-startx_fn],dtype='float')
    
    bad_fits_counter=0
    means_fn=np.array([])
    stds_fn=np.array([])
    heights_fn=np.array([])
    x_vals_fn=np.array([])
    y_vals_fn=np.array([])

    for pix_y in range(0,(endy_fn-starty_fn)): #(endy-starty)*(endx-startx)
        for pix_x in range(0,(endx_fn-startx_fn)): #(endy-starty)*(endx-startx)
            badfit=False

            if (pix_x%30==0 and pix_y%30==0):
                print(pix_x,pix_y)
            histValues=plt.hist(chosenPixels3d_fn[:,pix_y,pix_x],bins=45)
            mphist=midpoints(histValues[1])
            meanh=chosenPixels3d_fn[:,pix_y,pix_x].mean()
            stdh=chosenPixels3d_fn[:,pix_y,pix_x].std()
            try:
                popt,pcov=curve_fit(gaus,mphist,histValues[0],p0=[15,meanh,stdh])
            except:
                bad_fits_counter+=1
                popt=[-1,-1,-1]
                badfit=True



            heights_array_fn[pix_y,pix_x]=popt[0]
            means_array_fn[pix_y,pix_x]=popt[1]
            stds_array_fn[pix_y,pix_x]=popt[2]
#             if((pix_x==47) and (pix_y==32)):
#                 plt.plot(histValues[1][:-1],gaus(histValues[1][:-1],*popt),'ro:',label='fit')
#                 plt.show()
            plt.cla()
            plt.clf()
#             print(pix_x,pix_y,popt)
            # if badfit=False:        
            x_vals_fn=np.append(x_vals_fn,pix_x)
            y_vals_fn=np.append(y_vals_fn,pix_y)
            heights_fn=np.append(heights_fn,popt[0])
            means_fn=np.append(means_fn,popt[1])
            stds_fn=np.append(stds_fn,popt[2])

    print("badfits",bad_fits_counter)


    return heights_fn, means_fn, stds_fn, x_vals_fn, y_vals_fn, means_array_fn, stds_array_fn, heights_array_fn


#get files
dirpath=dataset_directory
files, n_files=get_files(dirpath)

#choose pixels for study
#0Rad dam
# startx=1351
# starty=2299
# endx=1400
# endy=2350
# # endx=1450
# # endy=2400

#20 rad dam
# startx=950
# starty=370
# endx=1000
# endy=420

#40 rad dam
startx=581
starty=1140
endx=632
endy=1190

chosenPix,chosenPixels,std=chosePix(startx,endx,starty,endy,dirpath,files,n_files)

#make std map, check chosen pix area is in right place
std[starty:endy,startx:endx]=0
plt.figure(figsize=(10,10))
plt.imshow(std,vmin=0,vmax=50)

#reshape chosen pix with frames along axis 0 
chosenPixels3d=chosenPixels.reshape((n_files,(endy-starty),(endx-startx)))
print(chosenPixels3d.shape)

#get bad pixel criteria
heights, means, stds, x_vals, y_vals, means_array, stds_array, heights_array = bad_pix_qual(startx,endx,starty,endy,chosenPixels3d)
fig,ax=plt.subplots(2,3,figsize=(20,10))
df=pd.DataFrame({'x_vals':x_vals, 'y_vals': y_vals, 'heights':heights, 'means':means, 'stds':stds})

even_heights_mean,even_heights_std=return_param_BPM("even","heights",0)
odd_heights_mean,odd_heights_std=return_param_BPM("odd","heights",0)
even_means_mean,even_means_std=return_param_BPM("even","means",1)
odd_means_mean,odd_means_std=return_param_BPM("odd","means",1)
even_stds_mean,even_stds_std=return_param_BPM("even","stds",2)
odd_stds_mean,odd_stds_std=return_param_BPM("odd","stds",2)

#make a mask of pixel means aetc
eo_means_means=np.zeros([endy-starty,endx-startx],dtype='float')
eo_stds_means=np.zeros([endy-starty,endx-startx],dtype='float')
eo_means_stds=np.zeros([endy-starty,endx-startx],dtype='float')
eo_stds_stds=np.zeros([endy-starty,endx-startx],dtype='float')


eo_means_means[::2,:]=even_means_mean
eo_means_means[1::2,:]=odd_means_mean
eo_stds_means[::2,:]=even_stds_mean
eo_stds_means[1::2,:]=odd_stds_mean
eo_means_stds[::2,:]=even_means_std
eo_means_stds[1::2,:]=odd_means_std
eo_stds_stds[::2,:]=even_stds_std
eo_stds_stds[1::2,:]=odd_stds_std

#use mask of means/stds to make bad pixel mask
badpixmask=np.ones([endy-starty,endx-startx])
badpixmask[(means_array>(eo_means_means+5*eo_means_stds))]=-1
badpixmask[(stds_array>eo_stds_means+5*eo_stds_stds)]=-1
badpixmask[(means_array<eo_means_means-5*eo_means_stds)]=-1
badpixmask[(stds_array<eo_stds_means-5*eo_stds_stds)]=-1
plt.imshow(badpixmask)
plt.colorbar()

#make BPM 3D
badpixmask3d=np.tile(badpixmask,(n_files,1))
badpixmask3d=badpixmask3d.reshape(n_files,endy-starty,endx-startx)

#reshape chosen pixels so they are centred on zero with sigma=1
reshaped_CP=np.ones([endy-starty,endx-startx])
reshaped_CP=(chosenPixels3d-means_array)/stds_array
reshaped_CP_BPM=reshaped_CP[badpixmask3d>0]
reshaped_CP_BPM.shape

#plot all pixels on one hist
# fig,ax=plt.subplots(2,1,figsize=(12,4))
# all_hist=ax[0].hist(reshaped_CP_BPM,bins=200,range=(-10,40))

# ax[0].set_xlim(-10,30)
# mphist=midpoints(all_hist[1])
# print(mphist[:41].shape,all_hist[0][:41].shape)
# popt,pcov=curve_fit(gaus,mphist[:41],all_hist[0][:41],p0=[100000,0,1])
# _=ax[0].plot(mphist[:41],gaus(mphist[:41],*popt),'ro:',label='fit')
# print(popt)

# popt2,pcov2=curve_fit(gaus,mphist[90:],all_hist[0][90:],p0=[60,25,1])
# print(popt2) 

# ax[1].plot(mphist[90:],all_hist[0][90:])
# _=ax[1].plot(mphist[90:],gaus(mphist[90:],*popt2),'yo:',label='fit')

with open('../outputpy/fourtydam_neg20.npy', 'wb') as f:
    np.save(f, reshaped_CP_BPM)

#more plots, log scale, fits to noise and Fe55
# fig,ax=plt.subplots(2,1,figsize=(12,9))
# ax[0].set_yscale('log')
# ax[0].set_ylim([10.0,25000])

# all_hist=ax[0].hist(reshaped_CP_BPM,bins=200,range=(-10,40))
# mphist=midpoints(all_hist[1])
# _=ax[0].plot(mphist,gaus(mphist,*popt),'ro:',label='fit')
# _=ax[0].plot(mphist[80:],gaus(mphist[80:],*popt2),'yo:',label='fit')


# sub_hist=ax[1].hist(reshaped_CP_BPM,bins=60,range=(15,40))
# sub_mphist=midpoints(sub_hist[1])
# popt3,pcov3=curve_fit(gaus,sub_mphist,sub_hist[0],p0=[60,25,1])
# print(popt3) 
# _=ax[1].plot(sub_mphist,gaus(sub_mphist,*popt3),'yo:',label='fit')
