from obspy.core import read
from obspy.signal.trigger import plot_trigger
from obspy.signal.trigger import classic_sta_lta
import math

data_directory = r'C:\Users\bkarr\Downloads\space_apps_2024_seismic_detection\space_apps_2024_seismic_detection\data\lunar\test\data\S12_GradeB'
test_filename = r'\xa.s12.00.mhz.1970-02-18HR00_evid00016'
mseed_file = f'{data_directory}{test_filename}.mseed'

number = 1.5 * math.pow(10,-9)
trace = read(mseed_file)[0]
df = trace.stats.sampling_rate

cft = classic_sta_lta(trace.data, int(453 * df), int(1510* df))
plot_trigger(trace, cft, 3.1, 2)