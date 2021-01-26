import datetime
import numpy as np  
import os
import zipfile
import tarfile
from plot_drap_functions import get_data, read_global_files, plot_global_map


#checks if drap directory exists to save files into, if not makes one
base_path = os.path.expanduser('~/Documents/drap/')
if not os.path.exists(base_path):
	os.makedir(base_path)

#date and time of interest
search_time = '2013-10-28 12:00'
search_time = datetime.datetime.strptime(search_time, '%Y-%m-%d %H:%M')

#path to where the files to be kept - checks if they are there - if not then downloads them

path_to_files = base_path + 'SWX_DRAP20_C_SWPC_'+search_time.strftime('%Y%m%d/')
if not os.path.exists(path_to_files):

	#download zip file from https://www.ngdc.noaa.gov/stp/drap/data/
	zipped_file_name = get_data(search_time, filepath = base_path)
	file_name = zipped_file_name.split('.')[0]

	#unzip the files - some are tar.gz and some are .zip

	if zipped_file_name.endswith('tar.gz'):
		tf = tarfile.open(zipped_file_name)
		tf.extractall(path = file_name)


	elif zipped_file_name.endswith('.zip'):
		zip = zipfile.ZipFile(zipped_file_name)
		zip.extractall(path = file_name)

	else:
		print('somethings wrong')


#name of global file
global_file = 'SWX_DRAP20_C_SWPC_'+search_time.strftime('%Y%m%d%H%M%S')+'_GLOBAL.txt'

#read the data from global file
lat, lon, full_map = read_global_files(os.path.join(path_to_files, global_file))

#plot the global map and save as 'example.png'
plot_global_map(lat, lon, full_map, title='NOAA D-RAP Model '+search_time.strftime('%Y-%m-%d %H:%M') + 'UT', save_plot = 'example')



