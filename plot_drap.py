import datetime
import numpy as np  
import os
from plot_drap_functions import read_global_files, plot_global_map

# example to read and plot the global DRAP model for certain time

#time of search
search_time = datetime.datetime.strptime('2013-10-28 12:00', '%Y-%m-%d %H:%M')

#path to where files are kept
base_path = '/Users/laurahayes/Documents/drap/SWX_DRAP20_C_SWPC_'+search_time.strftime('%Y%m%d/')
global_file = 'SWX_DRAP20_C_SWPC_'+search_time.strftime('%Y%m%d%H%M%S')+'_GLOBAL.txt'

#read the data from global file
lat, lon, full_map = read_global_files(os.path.join(base_path, global_file))

#plot the global map and save as 'example.png'
plot_global_map(lat, lon, full_map, title =  'DRAP Model '+search_time.strftime('%Y-%m-%d %H:%M') + 'UT', save_plot = 'example')

