import numpy as np
from matplotlib import pylab as plt
# import scipy as sp
from os import listdir,path
from os.path import isfile,join,isdir

import seaborn as sns
import sklearn.cluster as cluster
import time

sns.set_context('poster')
sns.set_color_codes()
plot_kwds = {'alpha' : 0.9,'s' : 16, 'linewidths':0} #'alpha' : 0.25, 

def plot_clusters(data, algorithm, args, kwds):
    start_time = time.time()
    labels = algorithm(*args, **kwds).fit_predict(data)#, sample_weight=input_weight
    end_time = time.time()
    palette = sns.color_palette('bright', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    # ax[0].scatter(data.T[1],data.T[0],s=12,c='black')
    # ax[0].spines['right'].set_visible(False)
    # ax[0].spines['top'].set_visible(False)
    # ax[0].spines['bottom'].set_visible(False)
    # ax[0].spines['left'].set_visible(False)
    # ax[1].spines['right'].set_visible(False)
    # ax[1].spines['top'].set_visible(False)
    # ax[1].spines['bottom'].set_visible(False)
    # ax[1].spines['left'].set_visible(False)
    ax[0,0].axis('off')
    ax[0,1].axis('off')

    ax[0,1].scatter(data.T[1], data.T[0], c=colors, **plot_kwds) #, **plot_kwds
    # print(**plot_kwds)
    # frame = plt.gca()
    # frame.axes.get_xaxis().set_visible(False)
    # frame.axes.get_yaxis().set_visible(False)
    # print (labels)
    counts = np.bincount(labels[labels>=0])
    # print (counts)
    ax[0,0].set_title(file_iter[8:-4], fontsize=24)
    # ax[0,0].text(-0.5, 0.01, 'Clustering took {:.2f} s'.format(end_time - start_time), fontsize=14)
    ax[0,0].imshow(im,vmin=2,vmax=33,origin='lower')

    yint = range(1,10)

    ax[1,0].set_xticks(yint)


    ax[1,0].hist(counts,range=(0.5,9.5),bins=9)
    fig.tight_layout(pad=0.1)

    return labels

def get_files(directory_path):
    dirpath=directory_path

    files=[f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and ".npy" in f and "seed_loc" in f)]
    files=sorted(files)
    n_files=len(files)
    print ("number of files="+str(n_files))
    return files,n_files


def midpoints(hvals):
    hvals_shift=np.append(hvals[1:],0)
    midp=(hvals+hvals_shift)/2.0
    return midp[:-1]


dirpath="../seedloc"
files, n_files=get_files(dirpath)

for j,file_iter in enumerate(files):
	print(j,file_iter)
	fig,ax=plt.subplots(2,2)#,figsize=(15,4.5)


	with open(dirpath+'/'+file_iter,'rb') as f:
		input_data=np.load(f)

	with open(dirpath+'/seed_weight'+file_iter[8:],'rb') as f:
		input_weight=np.load(f)

	seeds=np.array([])
	# fig2=plt.figure()
	# vals=plt.hist(input_weight,range=(0,75),bins=75)
	# mphist=midpoints(vals[1])
	# print(vals[0][23:],mphist[23:])
	# print('sum',vals[0][23:].sum())
	print((input_data.shape))
	im=np.zeros([51,51])
	for k,row in enumerate(input_data):
		# print(int(input_weight[k]))
		im[row[0],row[1]]=int(input_weight[k])
		if (input_weight[k]>20):
			seeds=np.append(seeds,row)
	# plt.imshow(im,vmax=20)
	# plt.pause(0.01)
	# input('paws')
	print('seeds',seeds,'size',int(len(seeds)/2))
	number_of_seed=int(len(seeds)/2)
	seeds=seeds.reshape(number_of_seed,2)


	labels=plot_clusters(input_data, cluster.DBSCAN, (), {'min_samples':1,'eps':1.45})
	# labels=plot_clusters(input_data, cluster.KMeans, (), {'n_clusters':number_of_seed, 'init':seeds})

	# fig3=plt.figure()
	cluster_sums=np.array([])
	for i in range(0,labels.max()+1):
		# print(input_weight[labels==i].sum())
		cluster_sums=np.append(cluster_sums,input_weight[labels==i].sum())

	# print(cluster_sums)
	ax[1,1].hist(cluster_sums,bins=100,range=(0,200))
	plt.pause(0.01)
	plt.savefig("DBScan_"+file_iter[8:]+".png")
	# input("wait")