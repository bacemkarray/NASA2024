# Import libraries
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import math
from scipy import signal
from matplotlib import cm


from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import classic_sta_lta
import math


def basemsgraph(mseed_file):

    number = 1.5 * math.pow(10,-9)
    trace = read(mseed_file)[0]
    df = trace.stats.sampling_rate

    cft = classic_sta_lta(trace.data, int(453 * df), int(1510* df))
    plot_trigger(trace, cft, 3.1, 2)


# Load the CSV file into a Pandas DataFrame
file_path = "/Volumes/MinhazHardD/space_apps_2024_seismic_detection/data/lunar/test/data/S12_GradeB/xa.s12.00.mhz.1970-03-30HR00_evid00020.csv"
mseed_file = file_path[:len(file_path)-3] + 'mseed'
df = pd.read_csv(file_path)
st = read(mseed_file)

# Extract relevant columns: time_rel and velocity
time_rel = df['time_rel(sec)'].values  # Extract the time in seconds
velocity = df['velocity(m/s)'].values  # Extract the velocity in m/s

# Convert the data to a NumPy array (if needed)
time_rel = np.array(time_rel)
velocity = np.array(velocity)


running_avg = 0
counter = 0



# Set the minimum frequency
minfreq = 0.5
maxfreq = 1.0


st = read(mseed_file)
tr = st.traces[0].copy()
tr_times = tr.times()
tr_data = tr.data

# Start time of trace (another way to get the relative arrival time using datetime)
starttime = tr.stats.starttime.datetime


# Going to create a separate trace for the filter data
st_filt = st.copy()
st_filt.filter('bandpass',freqmin=minfreq,freqmax=maxfreq)
tr_filt = st_filt.traces[0].copy()
tr_times_filt = tr_filt.times()
tr_data_filt = tr_filt.data
#THESE ARE THE NEW DATA TO BE GRAPHED
f, t, sxx = signal.spectrogram(tr_data_filt, tr_filt.stats.sampling_rate,axis=-1)



# Plot the time series and spectrogram
fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(2, 1, 1)
# Plot trace
ax.plot(tr_times_filt,tr_data_filt)

# Mark detection

ax.legend(loc='upper left')

# Make the plot pretty
ax.set_xlim([min(tr_times_filt),max(tr_times_filt)])
ax.set_ylabel('Velocity (m/s)')
ax.set_xlabel('Time (s)')


ax2 = plt.subplot(2, 1, 2)

vals = ax2.pcolormesh(t, f, sxx, cmap=cm.jet, vmax=5e-17, vmin=0)
print('t',type(t),t[1])
print('f',type(f))
print('sxx',type(sxx))

#sxx is a 2d array where each row is a frequency point and each column is a time point
print('sxx start', len(sxx[0]))
time_occ = []

for i in range(len(sxx)):
    if (np.max(sxx[i])>0.2*math.pow(10,-17)):
        time_occ.append(t[np.argmax(sxx[i])])

time_occ.sort()
print(time_occ)

ax2.set_xlim([min(tr_times_filt),max(tr_times_filt)])

ax2.set_xlabel(f'Time (Day Hour:Minute)', fontweight='bold')

ax2.set_ylabel('Frequency (Hz)', fontweight='bold')
# for i in t:
#     print(t)
for i in range(len(time_occ)):
    pairlist = time_occ[i]
    ax2.axvline(x = time_occ[i], color='red',label='Rel. Arrival')

ax.axvline(x= time_occ[-1], color='red',label='Rel. Arrival')
ax.axvline(x= time_occ[0], color='red',label='Rel. Arrival')


cbar = plt.colorbar(vals, orientation='horizontal')
cbar.set_label('Power ((m/s)^2/sqrt(Hz))', fontweight='bold')

from obspy.signal.invsim import cosine_taper
from obspy.signal.filter import highpass
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset

# Sampling frequency of our trace
df = tr.stats.sampling_rate

# How long should the short-term and long-term window be, in seconds?
sta_len = 120
lta_len = 600

# Run Obspy's STA/LTA to obtain a characteristic function
# This function basically calculates the ratio of amplitude between the short-term 
# and long-term windows, moving consecutively in time across the data
cft = classic_sta_lta(tr_data, int(sta_len * df), int(lta_len * df))

# Plot characteristic function
fig,ax = plt.subplots(1,1,figsize=(12,3))
ax.plot(tr_times,cft)

ax.set_xlim([min(tr_times),max(tr_times)])
ax.set_xlabel('Time (s)')
ax.set_ylabel('Characteristic function')
