from os import listdir,path
from os.path import isfile,join,isdir
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--datasetdir', help='input dataset directory')
args = parser.parse_args()
dataset_directory=args.datasetdir

def get_files(directory_path):
    dirpath=directory_path

    files=[f for f in listdir(dirpath) if (isfile(join(dirpath, f)) and ".tiff" in f)]
    # files=sorted(files)
    n_files=len(files)
    print ("number of files="+str(n_files))
    return files,n_files

files, n_files=get_files(dataset_directory)

for f in files:
	print(f)
	orig_num=int(f.replace('File_', '').replace('.tiff', ''))
	new_num=f"{orig_num:05d}"
	new_name='File_' + str(new_num) + '.tiff'
	print(dataset_directory+'/'+f,dataset_directory+'/'+new_name)
	# os.rename(dirpath+'/'+f,dirpath+'/'+new_name)
