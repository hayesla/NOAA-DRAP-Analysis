# NOAA D-Region Absorption Prediction (D-RAP) Product 

 This repository contains Python code for downloading, reading and plotting the NOAA D-Region Absorption Prediction (D-RAP) Product.
 See more here on [NOAA site](https://www.swpc.noaa.gov/products/d-region-absorption-predictions-d-rap)
 
 The code to download and plot the D-RAP model at a certain time is given in `example_download_and_plot_drap.py`
 
 You can change the time of interest change within the file by changing the `search_time` e.g.:
``` python
 
 search_time = '2013-10-28 12:00'
 
```
 
The output of running this example script will be to download the data from the time of interest and plot D-RAP model over the globe, which shows the HF absoption caused by space weather effects. The resulted map shows the highest frequency affected by absorption of 1dB cause by solar activity (flares) affecting the D-region of the ionosphere. An example of the above date is plotted here:
 
 ![alt text](example.png)
 
 
