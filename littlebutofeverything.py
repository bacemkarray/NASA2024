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


from obspy.core import read
from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import classic_sta_lta
import math


def basemsgraph(mseed_file):
    
    trace = read(mseed_file)[0]
    df = trace.stats.sampling_rate

    cft = classic_sta_lta(trace.data, int(453 * df), int(1510* df))
    plot_trigger(trace, cft, 2.0, 0.4)


# Load the CSV file into a Pandas DataFrame
file_path = "/Volumes/MinhazHardD/space_apps_2024_seismic_detection/data/mars/test/data/XB.ELYSE.02.BHV.2019-05-23HR02_evid0041.csv"
mseed_file = file_path[:len(file_path)-3] + 'mseed'
df = pd.read_csv(file_path)
st = read(mseed_file)

print(df)

# Extract relevant columns: time_rel and velocity
time_rel = df['rel_time(sec)'].values  # Extract the time in seconds
velocity = df['velocity(c/s)'].values  # Extract the velocity in m/s

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

vals = ax2.pcolormesh(t, f, sxx, cmap=cm.jet, vmax=max(tr_times_filt), vmin=0)
print('t',type(t),t[1])
print('f',type(f))
print('sxx',type(sxx))

retarr = []
#sxx is a 2d array where each row is a frequency point and each column is a time point
print('sxx start', len(sxx[0]))
time_occ = []

for i in range(len(sxx)):
    if (np.max(sxx[i])>0.2*math.pow(10,-17)):
        time_occ.append(t[np.argmax(sxx[i])])

time_occ.sort()
print(time_occ)
# for i in range(len(sxx)):
    # print(sxx[i][-1])
    # if np.max(sxx[i])> 4.3*math.pow(10,-17):
    #     print([sxx[i]])
    #     retarr.append([t[i],np.max(sxx[i])])
    # if (sxx[i]>math.pow(10,-34)):
        # print(i)
print('time', len(t))

print(retarr)

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





basemsgraph(mseed_file)

time_occ

time_occret = [time_occ[0]]

for i in range(1,len(time_occ)):
    if (time_occ[i]-time_occ[i-1]<500):
        continue
    else:
        time_occret.append(time_occ[i])

time_occret

time_rel,velocity

velocity = abs(velocity)


for i in range(len(velocity)):
    if (abs(velocity[i])<math.pow(10,-10)):
        velocity[i] = 0




# Plot the time series and spectrogram
fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(2, 1, 1)
# Plot trace
ax.plot(time_rel,velocity)

# Mark detection

ax.legend(loc='upper left')

# Make the plot pretty
ax.set_xlim([min(time_rel),max(time_rel)])
ax.set_ylabel('Velocity (m/s)')
ax.set_xlabel('Time (s)')

nvelocity = []
ntimes = []

num_times = 100

elemvalue = int(len(time_rel)/num_times)

for i in range(num_times):
    dataset = velocity[elemvalue*(i-1):elemvalue*(i)]
    counter =0
    sum=0

    for p in dataset:
        if (p==0):
            continue

        sum += p
        counter +=1
    if (counter == 0):
        nvelocity.append(0)
        ntimes.append(time_rel[i*elemvalue])
        continue
    avg = sum/counter

    nvelocity.append(avg)
    ntimes.append(time_rel[i*elemvalue])

print(nvelocity)
print('time',ntimes)





# Plot the time series and spectrogram
fig = plt.figure(figsize=(10, 10))
ax = plt.subplot(2, 1, 1)
# Plot trace
ax.plot(ntimes,nvelocity)
print(len(ntimes))

# Mark detection

ax.legend(loc='upper left')

# Make the plot pretty
ax.set_xlim([min(ntimes),max(ntimes)])
ax.set_ylabel('Velocity (m/s)')
ax.set_xlabel('Time (s)')

smallest = math.inf

for i in nvelocity:
    if (i<smallest and i!=0):
        smallest = i

div10s = abs(math.ceil(math.log(smallest)/math.log(10)))

print("definitions")

overallaverage = 0

counter = 0
for i in nvelocity:
    if (i == 0):
        continue

    overallaverage += i
    counter +=1

overallaverage = overallaverage/counter

ax.axhline(y=overallaverage,color='green',linewidth=4)


counter=0
for i in nvelocity:
    counter +=1
    if (i>overallaverage):
        print(time_rel[counter*elemvalue])

print(len(ntimes))
print(len(nvelocity))

ntime_occret = [ntimes[0]]

start_val = 0

for i in ntimes:
    if (i>0):
        start_val = i
        break

for i in range(1,len(ntimes)):
    if (ntimes[i]-ntimes[i-1]<1000):
        continue
    else:
        ntime_occret.append(ntimes[i])

ntimes[1]
