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
alldirs_dir=args.datasetdir
#eg. --datasetdir ../data/Fe-55_0RadDam_40deg/
print("input files ",args.datasetdir)

def gaus(x,a,x0,sigma):
  return (a/sigma)*exp(-(x-x0)**2/(2*sigma**2))

def midpoints(hvals):
    hvals_shift=np.append(hvals[1:],0)

    midp=(hvals+hvals_shift)/2.0
    return midp[:-1]

def get_dirs(directory_path):
    dirpath=directory_path

    dirs=[f for f in listdir(dirpath) if '.' not in f]
    dirs=sorted(dirs)
    n_dirs=len(dirs)
    print(dirs)

    print ("number of dirs="+str(n_dirs))
    return dirs,n_dirs

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

    for j,file_iter in enumerate(files_fn):
        if(j%10==0):
            print(j,file_iter)


        im=plt.imread(str(dirpath_fn+"/"+file_iter)) #np.fromfile(file_iter,dtype='uint16',sep="")
        im=im.astype('float')

        # chosenPix=np.append(chosenPix,im[starty_fn,startx_fn])
        chosenPixels=np.append(chosenPixels,im[starty_fn:endy_fn,startx_fn:endx_fn])


    return chosenPix, chosenPixels

def return_param_BPM(even_odd,hist_val,num):
    if even_odd=="odd":
        eo=1
    else:
        eo=0
    # print(even_odd,hist_val)
    # I know this is stupid having the df outside the function but I don't have time to fix it rn
    histValues=plt.hist(df[(df['y_vals']%2==eo)&(df['heights']<1000)][hist_val],bins=45)
    mphist=midpoints(histValues[1])
    meanh=df[(df['y_vals']%2==eo)&(df['heights']<1000)&(df['means']>0)][hist_val].mean()
    stdh=df[(df['y_vals']%2==eo)&(df['heights']<1000)&(df['means']>0)][hist_val].std()
    popt,pcov=curve_fit(gaus,mphist,histValues[0],p0=[35000,meanh,stdh])
    # plt.plot(histValues[1][:-1],gaus(histValues[1][:-1],*popt),'ro:',label='fit')
    # print(popt,meanh,stdh)
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

            binwidth=7
            # histValues=plt.hist(chosenPixels3d_fn[:,pix_y,pix_x],bins=45)
            singlePix=chosenPixels3d_fn[:,pix_y,pix_x]
            histValues=plt.hist(singlePix,bins=np.arange(min(singlePix), max(singlePix) + binwidth, binwidth))

            mphist=midpoints(histValues[1])
            # meanh=chosenPixels3d_fn[:,pix_y,pix_x].mean()
            meanArgMax=histValues[0].argmax()
            meanh=mphist[meanArgMax]
            # meanh=mphist[histValues[0].argmax()]

            stdh=chosenPixels3d_fn[:,pix_y,pix_x].std()
            try:
                popt,pcov=curve_fit(gaus,mphist[:meanArgMax+2],histValues[0][:meanArgMax+2],p0=[15,meanh,stdh])
            except:
                bad_fits_counter+=1
                popt=[-1,-1,-1]
                badfit=True


            heights_array_fn[pix_y,pix_x]=popt[0]
            means_array_fn[pix_y,pix_x]=popt[1]
            stds_array_fn[pix_y,pix_x]=popt[2]
#             if((pix_x==47) and (pix_y==32)):
                # arr=np.arange(min(singlePix),mphist[histValues[0].argmax()+2],2)

#                 plt.plot(arr,gaus(arr,*popt),'r-.',label='fit')
#                 plt.show()
            plt.cla()
            # plt.clf()
            # print(pix_x,pix_y,popt)
            # print(np.sqrt(np.diag(pcov2)))

            # if badfit=False:        
            x_vals_fn=np.append(x_vals_fn,pix_x)
            y_vals_fn=np.append(y_vals_fn,pix_y)
            heights_fn=np.append(heights_fn,popt[0])
            means_fn=np.append(means_fn,popt[1])
            stds_fn=np.append(stds_fn,popt[2])

    print("badfits",bad_fits_counter)


    return heights_fn, means_fn, stds_fn, x_vals_fn, y_vals_fn, means_array_fn, stds_array_fn, heights_array_fn


#get files
dirs, n_dirs=get_dirs(alldirs_dir)
for dirpath in dirs:
    print (dirpath)
    files, n_files=get_files(alldirs_dir+'/'+dirpath)
    damage=dirpath.split('_')[1][:-6]
    temperature=dirpath.split('_')[2]
    print(damage,temperature)
    dirpath=alldirs_dir+'/'+dirpath
    #choose pixels for study
    #0Rad dam
    if damage=='0':

        startx=1351
        starty=2299
        endx=1400
        endy=2350
    # # endx=1450
    # # endy=2400

    #20 rad dam
    elif damage=='20':
        startx=950
        starty=370
        endx=1000
        endy=420

    #40 rad dam
    elif damage=='40':
        startx=581
        starty=1140
        endx=632
        endy=1190

    elif damage=='50':
        startx=581
        starty=308 #330
        endx=632
        endy=358 #380

    chosenPix,chosenPixels=chosePix(startx,endx,starty,endy,dirpath,files,n_files)

    #make std map, check chosen pix area is in right place
    # std[starty:endy,startx:endx]=0
    # plt.figure(figsize=(10,10))
    # plt.imshow(std,vmin=0,vmax=50)

    #reshape chosen pix with frames along axis 0 
    chosenPixels3d=chosenPixels.reshape((n_files,(endy-starty),(endx-startx)))
    # print(chosenPixels3d.shape)

    #get bad pixel criteria
    heights, means, stds, x_vals, y_vals, means_array, stds_array, heights_array = bad_pix_qual(startx,endx,starty,endy,chosenPixels3d)
    # fig,ax=plt.subplots(2,3,figsize=(20,10))
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
    # plt.imshow(badpixmask)
    # plt.colorbar()

    #make BPM 3D
    badpixmask3d=np.tile(badpixmask,(n_files,1))
    badpixmask3d=badpixmask3d.reshape(n_files,endy-starty,endx-startx)

    #reshape chosen pixels so they are centred on zero with sigma=1
    reshaped_CP=np.ones([endy-starty,endx-startx])
    reshaped_CP=((chosenPixels3d-means_array)/stds_array)
    reshaped_CP_BPM=reshaped_CP[badpixmask3d>0]

    reshaped_CP_noise=np.ones([endy-starty,endx-startx])
    reshaped_CP_noise=(chosenPixels3d-means_array) #/stds_array
    reshaped_CP_BPM_noise=reshaped_CP_noise[badpixmask3d>0]

    print(reshaped_CP.shape)
    print(reshaped_CP[0,0:4,0:4])
    print(reshaped_CP_noise.shape)
    print(reshaped_CP_noise[0,0:4,0:4])
    print(reshaped_CP_noise[:,5,3].std(),stds_array[5,3])
    # plt.clf()
    # plt.hist(reshaped_CP_noise[:,5,3])
    # plt.pause(0.01)
    # input("pasue")


    with open('../outputpy/'+damage+'kGy'+temperature+'C_rawdata.npy', 'wb') as f:
        np.save(f, chosenPixels3d)

    with open('../outputpy/'+damage+'kGy'+temperature+'C_meansarray.npy', 'wb') as f:
        np.save(f, means_array)

    with open('../outputpy/'+damage+'kGy'+temperature+'C_stds_array.npy', 'wb') as f:
        np.save(f, stds_array)

    with open('../outputpy/'+damage+'kGy'+temperature+'C_BPMOnly.npy', 'wb') as f:
        np.save(f, badpixmask3d)

    with open('../outputpy/'+damage+'kGy'+temperature+'C_pedsub_stddiv_BPM.npy', 'wb') as f:
        np.save(f, reshaped_CP_BPM)

    with open('../outputpy/'+damage+'kGy'+temperature+'C__pedsub_stddiv_noMask.npy', 'wb') as f:
        np.save(f, reshaped_CP)

    with open('../outputpy/'+damage+'kGy'+temperature+'C_pedsub_noMask.npy', 'wb') as f:
        np.save(f, reshaped_CP_noise)

    with open('../outputpy/'+damage+'kGy'+temperature+'C_pedsub_BPM.npy', 'wb') as f:
        np.save(f, reshaped_CP_BPM_noise)

    # seed=(reshaped_CP[12,:,:]>3)*1.0
    # # subseed=seed[1:-1,1:-1]
    # # seed_loc=np.argwhere(subseed>0.5)+[1,1]
    # seed_loc=np.argwhere(seed>0.5)
    sample_weights=reshaped_CP[17,:,:][reshaped_CP[17,:,:]>3.0]
    seed_loc=np.argwhere(reshaped_CP[17,:,:]>3.0)
    with open('../seedloc/seed_loc'+damage+'kGy'+temperature+'C.npy','wb')as f:
        np.save(f,seed_loc)
    with open('../seedloc/seed_weight'+damage+'kGy'+temperature+'C.npy','wb')as f:
        np.save(f,sample_weights)

    sample_weights_noise=reshaped_CP_noise[17,:,:][reshaped_CP_noise[17,:,:]>100.0]
    seed_loc_noise=np.argwhere(reshaped_CP_noise[17,:,:]>100.0)
    with open('../seedloc/seed_loc'+damage+'kGy'+temperature+'C_noise.npy','wb')as f:
        np.save(f,seed_loc_noise)
    with open('../seedloc/seed_weight'+damage+'kGy'+temperature+'C_noise.npy','wb')as f:
        np.save(f,sample_weights_noise)


