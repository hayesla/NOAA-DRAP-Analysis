
import numpy as np
import os
import re
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import urllib


def get_data(date, filepath = '/Users/laurahayes/Documents/drap'):

	'''
	function to download the DRAP zip files for a certain data

	Parameters
	----------
	date : datetime.datetime object

	kwargs - filepath : str, what directory to save files to

	Returns
	-------

	Prints the filepath if downloaded

	'''

	url = 'https://www.ngdc.noaa.gov/stp/drap/data/' + date.strftime('%Y/%m/')
	try: 
		file = 'SWX_DRAP20_C_SWPC_'+ date.strftime('%Y%m%d') + '.zip'
		urlpath = os.path.join(url, file)
		urllib.request.urlretrieve(urlpath, os.path.join(filepath, file))

	except:
		file = 'SWX_DRAP20_C_SWPC_'+ date.strftime('%Y%m%d') + '.tar.gz'
		urlpath = os.path.join(url, file)
		urllib.request.urlretrieve(urlpath, os.path.join(filepath, file))

	if os.path.exists(os.path.join(filepath, file)):
		print (os.path.join(filepath, file))
	else:
		print ('didn\' download')



def read_global_files(file_path):

	'''
	function to read the global DRAP txt files and return lat, lon and map data

	Parameters
	----------

	filepath : path to txt file

	Returns
	-------

	latitude : 2D np array 
	longitude : 2D np array
	full_map : 2D np array - map data (degraded freq) at each lat lon


	'''

	#read the data, skipping comments
	data = []
	for lines in open(file_path):
		if not lines.startswith('#'):
			data.append(lines)

	#first line contains the latitute info
	lat = [float(x) for x in data[0].split()]

	#get rest of data
	lon = []
	map_values = []
	for dat in data[2:]:
		#collecting longitude values
		lon.append(float(dat.split()[0]))
		#collecting map values - sometimes **** so need to check
		try:
			val = [float(x) for x in dat.split()[2:]]
		except:
			val = []
			for v in dat.split()[2:]:
				if v == '****':
					val.append(100)
				else:
					val.append(float(v))

		map_values.append(val)
		

	lon.reverse()
	map_values.reverse()


	full_map = np.array(map_values).T
	lats, lons = np.meshgrid(np.array(lon), np.array(lat))	

	return lats, lons, full_map



def plot_global_map(lats, lons, full_map, save_plot = None, title = 'DRAP Model'):
	'''
	function to plot map after txt global file read

	default xlims and ylims over Europe but these can be changed to whatever


	Parameters
	----------

	outputs from read_global_files
	lats : 2D array
	lons : 2D array
	full_map : 2D array

	kwargs save_plot : str. If you want to save plot use kwarg with name of plot to save


	'''

	fig=plt.figure()
	m = Basemap(projection = 'cyl', llcrnrlat=-89,urcrnrlat=89, llcrnrlon=-178,urcrnrlon=178, resolution = 'l')

	levels = np.arange(0, 35,0.1)
	#CS1 = m.contour(lons,lats,full_map,levels,linewidths=0.5,colors='k',latlon=True)
	CS2 = m.contourf(lons,lats,full_map,levels,cmap='afmhot_r', extend='both',latlon=True)
	cbar = m.colorbar(CS2,location = 'bottom') 
	cbar.set_label('Degraded Frequency (MHz)')
	cbar.set_ticks([0, 5, 10, 15, 20, 25, 30])
	m.drawcoastlines()
	m.drawmapboundary()

	m.drawparallels(np.linspace(-90, 90, 25), linewidth = 0.5, labels = [1,0,0,0])
	m.drawmeridians(np.linspace(-180, 180, 25), linewidth = 0.5, labels = [0,0,0,1])

	plt.xlim(-30, 50)

	plt.ylim(35, 77)
	plt.title(title)
	plt.tight_layout()
	
	if save_plot != None:
		plt.savefig(save_plot+'.png')


	plt.show()


