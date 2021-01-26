
import numpy as np
import os
import re
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import urllib

def get_data(date, filepath='/Users/laurahayes/Documents/drap'):
	"""
	Function to download the DRAP zip files for a certain date.

	Parameters
	----------
	date : `~datetime.datetime` 


	Returns
	-------
	The filepath if downloaded.
	"""

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
		print ('didn\'t download')
		return

	return os.path.join(filepath, file)


def read_global_files(file_path):
	"""
	Function to read the global DRAP txt files and return lat, lon and map data

	Parameters
	----------
	filepath : `~str`
		path to txt file

	Returns
	-------

	lats : `~ndarray` 
		2D np.array of latitudes
	lons : `ndarray`
		2D np.array of longitudes
	full_map : `ndarray
		2D np.array - map data (degraded freq) at each lat lon
	"""
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



def plot_global_map(lats, lons, full_map, title="DRAP Model", save_plot=None,):
	"""
	Function to plot map after of DRAP model. 

	Parameters
	----------
	outputs from read_global_files

	lats : `ndarray`
		2D array of latitude values
	lons : `ndarray`
		2D array of longitude values
	full_map : `ndarray`
		2D array of DRAP degraded frequencies.

	title : `~str`, optional
		title of plot, defaults "DRAP Model"
	save_plot : `~str`, optional
		path name of file to save, default None (i.e. doesn't save)
	"""

	fig=plt.figure(figsize=(10, 5))

	ax = fig.add_subplot()

	m = Basemap(projection='cyl', 
				llcrnrlat=-89,urcrnrlat=89, 
				llcrnrlon=-178,urcrnrlon=178, 
				resolution='l', ax=ax)

	levels = np.arange(0, 35,0.1)
	CS2 = m.contourf(lons,lats,full_map,levels,cmap='magma_r', extend='both',latlon=True)
	cbar = m.colorbar(CS2,location='right', size="2%") 
	cbar.set_label('Degraded Frequency (MHz)')
	cbar.set_ticks([0, 5, 10, 15, 20, 25, 30])

	m.drawcoastlines()
	m.drawmapboundary()

	m.drawparallels(np.linspace(-90, 90, 10), linewidth = 0.5, labels = [1,0,0,0])
	m.drawmeridians(np.linspace(-180, 180, 10), linewidth = 0.5, labels = [0,0,0,1])

	ax.set_xlabel("Longitude", labelpad=20)
	ax.set_ylabel("Latitude", labelpad=40)

	ax.set_title(title)
	plt.tight_layout()
	
	if save_plot != None:
		plt.savefig(save_plot+'.png', dpi=200)

	plt.show()

